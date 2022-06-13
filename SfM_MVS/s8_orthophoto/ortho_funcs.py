import os, osr
from psutil import virtual_memory
from osgeo import gdal
from osgeo.gdalconst import GA_Update
from s0_dataset import log
from s0_dataset.runCMD import run


def crop(crop_bin, gpkg_path, geotiff_path, gdal_options, warp_options=[]):
    """
    crop orthophoto.

    :param crop_bin:
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

    kwargs = {'bin': crop_bin, 'gpkg_path': gpkg_path,
              'geotiffInput': original_geotiff, 'geotiffOutput': geotiff_path,
              'options': ' '.join(map(lambda k: '-co {}={}'.format(k, gdal_options[k]), gdal_options)),
              'warpOptions': ' '.join(warp_options), 'max_memory': max(5, (100 - virtual_memory().percent) * 0.5)}

    run('{bin} -cutline {gpkg_path} -crop_to_cutline {options} {warpOptions} {geotiffInput} {geotiffOutput} '
        '--config GDAL_CACHEMAX {max_memory}% > /dev/null 2>&1'.format(**kwargs))


def generate_png(gdal_translate, orthophoto_file, output_file=None, outsize=None):
    """
    generating orthophoto for png format.

    :param gdal_translate:
    :param orthophoto_file:
    :param output_file:
    :param outsize:
    """
    if output_file is None:
        base, ext = os.path.splitext(orthophoto_file)
        output_file = base + '.png'

    # See if we need to select top three bands
    bandparam = ""
    gtif = gdal.Open(orthophoto_file)
    if gtif.RasterCount > 4:
        bandparam = "-b 1 -b 2 -b 3 -a_nodata 0"

    osparam = ""
    if outsize is not None:
        osparam = "-outsize %s 0" % outsize

    log.logINFO("Generating orthophoto for PNG format...")
    run('%s -of png %s %s %s %s --config GDAL_CACHEMAX %s%% > /dev/null 2>&1'
        % (gdal_translate, orthophoto_file, output_file, osparam, bandparam, max(5, (100 - virtual_memory().percent) * 0.5)))


def geo_ortho(gdal_bin, geoinfo, corners, render, tif, log_file, ortho_vars):
    """
    Create georeferenced GeoTiff

    :param gdal_bin:
    :param geoinfo:
    :param corners:
    :param render:
    :param tif:
    :param log:
    :param ortho_vars:
    """
    if geoinfo['is_georeferenced']:
        ulx = uly = lrx = lry = 0.0
        with open(corners) as f:
            for lineNumber, line in enumerate(f):
                if lineNumber == 0:
                    tokens = line.split(' ')
                    if len(tokens) == 4:
                        ulx = float(tokens[0]) + float(geoinfo['utm_east_offset'])
                        lry = float(tokens[1]) + float(geoinfo['utm_north_offset'])
                        lrx = float(tokens[2]) + float(geoinfo['utm_east_offset'])
                        uly = float(tokens[3]) + float(geoinfo['utm_north_offset'])

        kwargs = {'gdal_bin': gdal_bin, 'ulx': ulx, 'uly': uly, 'lrx': lrx, 'lry': lry,
                  'vars': ' '.join(['-co %s=%s' % (k, ortho_vars[k]) for k in ortho_vars]),
                  'proj': geoinfo['proj4'],
                  'input': render, 'output': tif, 'log': log_file,
                  'max_memory': max(5, (100 - virtual_memory().percent) * 0.5)
                  }

        cmd = ('{gdal_bin} -a_ullr {ulx} {uly} {lrx} {lry} {vars} -a_srs \"{proj}\" '
               '--config GDAL_CACHEMAX {max_memory}% --config GDAL_TIFF_INTERNAL_MASK YES {input} {output} > {log}'.format(**kwargs))
        run(cmd, "Creating GeoTIFF...")


def add_pseudo_georeferencing(geotiff):
    """
    add pseudo georeferencing for orthophoto

    :param geotiff:
    """
    try:
        log.logINFO("Adding pseudo georeferencing (raster should show up at the equator) to %s" % geotiff)
        dst_ds = gdal.Open(geotiff, GA_Update)
        srs = osr.SpatialReference()
        srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        srs.ImportFromProj4('+proj=utm +zone=30 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
        dst_ds.SetProjection( srs.ExportToWkt() )
        dst_ds.SetGeoTransform( [ 0.0, 0.1, 0.0, 0.0, 0.0, -0.1 ] )
    except Exception as e:
        log.logWARNING("Cannot add psuedo georeferencing to %s (%s), skipping..." % (geotiff, str(e)))
