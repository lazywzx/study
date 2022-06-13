import os, shutil
from ..s0_dataset import DSParameter, log
from ..s5_dsm import dem_func, pdal


def dem_process(dem_root_path, model_input, dem_output, bounds_file_path, result_path):
    """
    DEM processing, pc_classify, create dem and crop them.

    :param dem_root_path:
    :param model_input:
    :param dem_output:
    :param bounds_file_path:
    :param result_path:
    """
    args = DSParameter.args
    if args.pc_classify:
        pc_classify_marker = os.path.join(dem_root_path, 'pc_classify.txt')
        log.logINFO("Classifying {} using Simple Morphological Filter".format(model_input))
        pdal.run_pdaltranslate_smrf(model_input, dem_output, args.smrf_scalar, args.smrf_slope, args.smrf_threshold, args.smrf_window)

        with open(pc_classify_marker, 'w') as f:
            f.write('Classify: smrf\n')
            f.write('Scalar: {}\n'.format(args.smrf_scalar))
            f.write('Slope: {}\n'.format(args.smrf_slope))
            f.write('Threshold: {}\n'.format(args.smrf_threshold))
            f.write('Window: {}\n'.format(args.smrf_window))

    if args.pc_rectify:
        dem_func.rectify(dem_output)

    products = []
    if args.dsm:
        products.append('dsm')
    if args.dtm:
        products.append('dtm')
    if len(products) == 0:
        log.logERROR("Parameter Error! Exit.")
        return None

    radius_steps = [(args.dem_resolution / 100.0) / 2.0]
    for _ in range(args.dem_gapfill_steps - 1):
        radius_steps.append(radius_steps[-1] * 2) # 2 is arbitrary

    for product in products:
        dem_func.create_dem(dem_output, product, output_type='idw' if product == 'dtm' else 'max',
                            radiuses=list(map(str, radius_steps)), outdir=dem_root_path,
                            resolution=args.dem_resolution / 100.0, decimation=args.dem_decimation,
                            max_workers=args.max_concurrency)

        dem_geotiff_path = os.path.join(dem_root_path, "{}.tif".format(product))
        if args.crop > 0:
            # Crop DEM
            dem_vars = {'TILED': 'YES', 'COMPRESS': 'DEFLATE', 'BLOCKXSIZE': 512, 'BLOCKYSIZE': 512,
                        'BIGTIFF': 'IF_SAFER', 'NUM_THREADS': args.max_concurrency}
            dem_func.crop(bounds_file_path, dem_geotiff_path, dem_vars)
        shutil.copyfile(dem_geotiff_path, os.path.join(result_path, "{}.tif".format(product)))
