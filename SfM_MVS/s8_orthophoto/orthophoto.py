import os
from s0_dataset import DSTree, DSParameter, log
from s0_dataset.runCMD import run
from s1_sfm import exif_info
from s8_orthophoto import ortho_funcs

tree = DSTree.tree
args = DSParameter.args


def ortho_pipeline(ortho_dir, textured_model, kwargs, geoinfo, orthophoto_vars, bounds_file_path):
    """
    Run orthophoto pipeline.
    :param ortho_dir:
    :param textured_model:
    :param kwargs:
    :param geoinfo:
    :param orthophoto_vars:
    :param bounds_file_path:
    """
    corners = os.path.join(ortho_dir, tree.orthophoto_corners)
    ortho = os.path.join(ortho_dir, tree.orthophoto_render)
    log_path = os.path.join(ortho_dir, tree.ortho_log)
    model = textured_model + ".obj"
    kwargs.update({'log': log_path, 'ortho': ortho, 'corners': corners, 'models': model})
    # run odm_orthophoto
    cmd = ('{bin} -inputFiles {models} -logFile {log} -outputFile {ortho} -resolution {res} '
           '-outputCornerFile {corners}'.format(**kwargs))
    run(cmd, "Run orthophoto, create orhto photo from textured model...")

    # georef the orthophoto
    render = os.path.join(ortho_dir, tree.orthophoto_render)
    tif = os.path.join(ortho_dir, tree.orthophoto_tif)
    if geoinfo['is_georeferenced']:
        ortho_funcs.geo_ortho(tree.gdal_translate, geoinfo, corners, render, tif, log_path, orthophoto_vars)
        ortho_funcs.crop(tree.gdalwarp, bounds_file_path, tif, orthophoto_vars, warp_options=['-dstalpha'])
        ortho_funcs.generate_png(tree.gdal_translate, tif)
    else:
        log.logWARNING("The reconstruction is not georefed.")
        if os.path.exists(render):
            ortho_funcs.add_pseudo_georeferencing(render)
            log.logINFO("Renaming %s --> %s" % (render, tif))
            os.rename(render, tif)
        else:
            log.logWARNING("Could not generate an orthophoto (it did not render)")


def create_orthophoto():
    """
    create orhtophoto from textured models.
    """
    if not os.path.exists(tree.orthoDIR):
        os.makedirs(tree.orthoDIR)

    geoinfo = exif_info.gpsinfo_dict
    bounds_file_path = tree.gpkgfile
    # orthophoto definitions
    kwargs = {
        'bin': tree.ortho_bin,
        'res': args.ortho_resol
    }
    # orthophoto vars
    orthophoto_vars = {
        'TILED': 'YES', 'COMPRESS': args.orthophoto_compression,
        'PREDICTOR': '2' if args.orthophoto_compression in ['LZW', 'DEFLATE'] else '1',
        'BIGTIFF': 'IF_SAFER', 'BLOCKXSIZE': 512, 'BLOCKYSIZE': 512,
        'NUM_THREADS': args.max_concurrency
    }

    if args.mesh3d:
        if not os.path.exists(tree.ortho3dDIR):
            os.makedirs(tree.ortho3dDIR)
        ortho_pipeline(tree.ortho3dDIR, tree.textured3d, kwargs, geoinfo, orthophoto_vars, bounds_file_path)
    if args.mesh25d:
        if not os.path.exists(tree.ortho25dDIR):
            os.makedirs(tree.ortho25dDIR)
        ortho_pipeline(tree.ortho25dDIR, tree.textured25d, kwargs, geoinfo, orthophoto_vars, bounds_file_path)
