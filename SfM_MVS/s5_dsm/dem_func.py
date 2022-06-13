from asyncio import FastChildWatcher
import os, math, rasterio, numpy, tempfile, json
from scipy import ndimage
from psutil import virtual_memory
from s0_dataset import log, DSTree
from s0_dataset.runCMD import run
from s0_dataset.parallel import parallel_map
from . import pdal
from .ground_rectification.rectify import run_rectification

tree = DSTree.tree


def median_smoothing(geotiff_path, output_path, smoothing_iterations=1):
    """
    Apply median smoothing
    :param geotiff_path:
    :param output_path:
    :param smoothing_iterations:
    """
    # log.logINFO('Starting smoothing...')

    with rasterio.open(geotiff_path) as img:
        nodata = img.nodatavals[0]
        dtype = img.dtypes[0]
        arr = img.read()[0]

        # Median filter (careful, changing the value 5 might require tweaking) the lines below.
        # There's another numpy function that takes care of these edge cases, but it's slower.
        for i in range(smoothing_iterations):
            # log.logINFO("Smoothing iteration %s" % str(i + 1))
            arr = ndimage.median_filter(arr, size=5, output=dtype)

        # Fill corner points with nearest value
        if arr.shape >= (4, 4):
            arr[0][:2] = arr[1][0] = arr[1][1]
            arr[0][-2:] = arr[1][-1] = arr[2][-1]
            arr[-1][:2] = arr[-2][0] = arr[-2][1]
            arr[-1][-2:] = arr[-2][-1] = arr[-2][-2]

        # Median filter leaves a bunch of zeros in nodata areas
        locs = numpy.where(arr == 0.0)
        arr[locs] = nodata

        # write output
        with rasterio.open(output_path, 'w', **img.profile) as imgout:
            imgout.write(arr, 1)


def get_extent(input_point_cloud):
    """
    get the extent of input point cloud.
    :param input_point_cloud:
    :return: bounds
    """
    fd, json_file = tempfile.mkstemp(suffix='.json')
    os.close(fd)

    fallback = False
    has_bbox = True
    if input_point_cloud.lower().endswith(".ply"):
        fallback = True
        run('{0} info {1} > {2}'.format(tree.pdal, input_point_cloud, json_file), "Run pdal info.")

    try:
        if not fallback:
            cmd = '{0} info --summary {1} > {2}'.format(tree.pdal, input_point_cloud, json_file)
            run(cmd, "Run pdal info summary.")
    except:
        fallback = True
        run('{0} info {1} > {2}'.format(tree.pdal, input_point_cloud, json_file), "Run pdal info.")

    with open(json_file, 'r') as f:
        result = json.loads(f.read())
        if not fallback:
            summary = result.get('summary')
            bounds = summary.get('bounds')
        else:
            try:
                stats = result.get('stats')
                bbox = stats.get('bbox')
                native = bbox.get('native')
                bounds = native.get('bbox')
            except:
                # 有的点云没有输出bbox，手动创建
                # 不对，没有输出是因为数据有误，非常离谱
                bounds = {}
                has_bbox = False
                """
                bounds = {}
                stats = result.get('stats')
                statistic = result.get('statistic')
                bounds["maxx"] = statistic[0].get('maximum')
                bounds["minx"] = statistic[0].get('maximum')
                bounds["maxy"] = statistic[1].get('maximum')
                bounds["miny"] = statistic[1].get('maximum')
                bounds["maxz"] = statistic[2].get('maximum')
                bounds["minz"] = statistic[2].get('maximum')
                """
                

    return bounds, has_bbox


def create_dem(input_point_cloud, dem_type, output_type='max', radiuses=['0.56'], outdir='', resolution=0.1,
               max_workers=1, max_tile_size=4096, decimation=None):
    """
    Create DEM.
    :param input_point_cloud:
    :param dem_type:
    :param output_type:
    :param radiuses:
    :param outdir:
    :param resolution:
    :param max_workers:
    :param max_tile_size:
    :param decimation:
    """
    extent, hb = get_extent(input_point_cloud)
    if not hb:
        return
    
    log.logINFO("Point cloud bounds are [minx: %s, maxx: %s] [miny: %s, maxy: %s]" % (
        extent['minx'], extent['maxx'], extent['miny'], extent['maxy']))
    ext_width = extent['maxx'] - extent['minx']
    ext_height = extent['maxy'] - extent['miny']

    w, h = (int(math.ceil(ext_width / float(resolution))), int(math.ceil(ext_height / float(resolution))))
    # Set a floor, no matter the resolution parameter
    RES_FLOOR = 64
    if w < RES_FLOOR and h < RES_FLOOR:
        prev_w, prev_h = w, h
        if w >= h:
            w, h = (RES_FLOOR, int(math.ceil(ext_height / ext_width * RES_FLOOR)))
        else:
            w, h = (int(math.ceil(ext_width / ext_height * RES_FLOOR)), RES_FLOOR)

        floor_ratio = prev_w / float(w)
        resolution *= floor_ratio
        radiuses = [str(float(r) * floor_ratio) for r in radiuses]

        log.logWARNING("Really low resolution DEM requested %s will set floor at %s pixels. Resolution changed to %s. "
                       "The scale of this reconstruction might be off." % ((prev_w, prev_h), RES_FLOOR, resolution))

    final_dem_pixels = w * h

    num_splits = int(max(1, math.ceil(math.log(math.ceil(final_dem_pixels / float(max_tile_size * max_tile_size))) / math.log(2))))
    num_tiles = num_splits * num_splits
    # log.logINFO("DEM resolution is %s, max tile size is %s, will split DEM generation into %s tiles" % (
    #     (h, w), max_tile_size, num_tiles))

    tile_bounds_width = ext_width / float(num_splits)
    tile_bounds_height = ext_height / float(num_splits)

    tiles = []
    for r in radiuses:
        minx = extent['minx']
        for x in range(num_splits):
            miny = extent['miny']
            if x == num_splits - 1:
                maxx = extent['maxx']
            else:
                maxx = minx + tile_bounds_width

            for y in range(num_splits):
                if y == num_splits - 1:
                    maxy = extent['maxy']
                else:
                    maxy = miny + tile_bounds_height

                filename = os.path.join(os.path.abspath(outdir), '%s_r%s_x%s_y%s.tif' % (dem_type, r, x, y))
                tiles.append({'radius': r, 'bounds': {'minx': minx, 'maxx': maxx, 'miny': miny, 'maxy': maxy}, 'filename': filename})

                miny = maxy
            minx = maxx

    # Sort tiles by increasing radius
    tiles.sort(key=lambda t: float(t['radius']), reverse=True)

    def process_tile(q):
        d = pdal.json_gdal_base(q['filename'], output_type, q['radius'], resolution, q['bounds'])
        if dem_type == 'dtm':
            d = pdal.json_add_classification_filter(d, 2)
        if decimation is not None:
            d = pdal.json_add_decimation_filter(d, decimation)

        pdal.json_add_readers(d, [input_point_cloud])
        pdal.run_pipeline(d)

    # parallel processing
    # log.logINFO("This step will take a while, please wait minutes...")
    parallel_map(process_tile, tiles, max_workers)

    output_file = "%s.tif" % dem_type
    output_path = os.path.abspath(os.path.join(outdir, output_file))

    # Create virtual raster
    tiles_vrt_path = os.path.abspath(os.path.join(outdir, "tiles.vrt"))
    cmd = '%s %s %s > /dev/null 2>&1' % (tree.gdalbuildvrt, tiles_vrt_path, ' '.join(map(lambda t: t['filename'], tiles)))
    cmd_info = "Create virtual raster."
    run(cmd)

    merged_vrt_path = os.path.abspath(os.path.join(outdir, "merged.vrt"))
    geotiff_tmp_path = os.path.abspath(os.path.join(outdir, 'tiles.tmp.tif'))
    geotiff_small_path = os.path.abspath(os.path.join(outdir, 'tiles.small.tif'))
    geotiff_small_filled_path = os.path.abspath(os.path.join(outdir, 'tiles.small_filled.tif'))
    geotiff_path = os.path.abspath(os.path.join(outdir, 'tiles.tif'))

    max_memory = max(5, (100 - virtual_memory().percent) * 0.5)

    # Build GeoTIFF
    kwargs = {'translate': tree.gdal_translate, 'fillnodata': tree.gdal_fillnodata, 'max_memory': max_memory,
              'threads': max_workers if max_workers else 'ALL_CPUS', 'tiles_vrt': tiles_vrt_path,
              'merged_vrt': merged_vrt_path, 'geotiff': geotiff_path, 'geotiff_tmp': geotiff_tmp_path,
              'geotiff_small': geotiff_small_path, 'geotiff_small_filled': geotiff_small_filled_path}

    cmd = '{translate} -co NUM_THREADS={threads} -co BIGTIFF=IF_SAFER --config GDAL_CACHEMAX {max_memory}% ' \
          '{tiles_vrt} {geotiff_tmp} > /dev/null 2>&1'.format(**kwargs)
    cmd_info = "Convert to GeoTIFF."
    run(cmd)

    # Scale to 10% size
    cmd = '{translate} -co NUM_THREADS={threads} -co BIGTIFF=IF_SAFER --config GDAL_CACHEMAX {max_memory}% ' \
          '-outsize 10% 0 {geotiff_tmp} {geotiff_small} > /dev/null 2>&1'.format(**kwargs)
    cmd_info = "Scale to 10% size."
    run(cmd)

    # Fill scaled
    cmd = '{fillnodata} -co NUM_THREADS={threads} -co BIGTIFF=IF_SAFER --config GDAL_CACHEMAX {max_memory}% ' \
          '-b 1 -of GTiff {geotiff_small} {geotiff_small_filled} > /dev/null 2>&1'.format(**kwargs)
    cmd_info = "Fill scaled."
    run(cmd)

    cmd = '%s -resolution highest -r bilinear %s %s %s > /dev/null 2>&1' % (
        tree.gdalbuildvrt, merged_vrt_path, geotiff_small_filled_path, geotiff_tmp_path)
    cmd_info = "Merge filled scaled DEM with unfilled DEM using bilinear interpolation."
    run(cmd)

    cmd = '{translate} -co NUM_THREADS={threads} -co TILED=YES -co BIGTIFF=IF_SAFER -co COMPRESS=DEFLATE ' \
          '--config GDAL_CACHEMAX {max_memory}% {merged_vrt} {geotiff} > /dev/null 2>&1'.format(**kwargs)
    cmd_info = "Run translate."
    run(cmd)

    median_smoothing(geotiff_path, output_path)
    # clean disk
    for cleanup_file in [geotiff_path, tiles_vrt_path, merged_vrt_path, geotiff_small_path,
                         geotiff_small_filled_path, geotiff_tmp_path]:
        if os.path.exists(cleanup_file):
            os.remove(cleanup_file)
    for t in tiles:
        if os.path.exists(t['filename']):
            os.remove(t['filename'])


def crop(gpkg_path, geotiff_path, gdal_options, warp_options=[]):
    """
    Cropping the dem model.
    :param gpkg_path:
    :param geotiff_path:
    :param gdal_options:
    :param warp_options:
    """
    log.logINFO("Cropping %s" % geotiff_path)
    path, filename = os.path.split(geotiff_path)
    basename, ext = os.path.splitext(filename)

    original_geotiff = os.path.join(path, "{}.original{}".format(basename, ext))
    os.rename(geotiff_path, original_geotiff)

    max_memory = max(5, (100 - virtual_memory().percent) * 0.5)

    kwargs = {'gdalwarp': tree.gdalwarp, 'gpkg_path': gpkg_path, 'geotiffInput': original_geotiff, 'geotiffOutput': geotiff_path,
              'options': ' '.join(map(lambda k: '-co {}={}'.format(k, gdal_options[k]), gdal_options)),
              'warpOptions': ' '.join(warp_options), 'max_memory': max_memory}

    cmd = '{gdalwarp} -cutline {gpkg_path} -crop_to_cutline {options} {warpOptions} {geotiffInput} {geotiffOutput} ' \
          '--config GDAL_CACHEMAX {max_memory}% > /dev/null 2>&1'.format(**kwargs)
    run(cmd, "Cropping dem.")


def rectify(lasFile, reclassify_threshold=5, min_area=750, min_points=500):
    tempLasFile = os.path.join(os.path.dirname(lasFile), 'tmp.las')
    # Convert LAZ to LAS
    cmd = ' '.join([tree.pdal, 'translate', '-i %s' % lasFile, '-o %s' % tempLasFile, '> /dev/null 2>&1'])
    run(cmd, "Convert LAZ to LAS.")

    log.logINFO("Rectifying...")
    run_rectification(input=tempLasFile, output=tempLasFile, debug=False, reclassify_plan='median',
                      reclassify_threshold=reclassify_threshold, extend_plan='surrounding',
                      extend_grid_distance=5, min_area=min_area, min_points=min_points)

    # Convert LAS to LAZ
    cmd = ' '.join([tree.pdal, 'translate', '-i %s' % tempLasFile, '-o %s' % lasFile, '> /dev/null 2>&1'])
    run(cmd, "Convert LAS to LAZ.")
    os.remove(tempLasFile)
