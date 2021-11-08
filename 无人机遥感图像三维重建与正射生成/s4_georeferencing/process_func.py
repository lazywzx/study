from ..s0_dataset import log, DSTree
from ..s0_dataset.runCMD import run
from ..s4_georeferencing import cropper
from ..s1_sfm import exif_info


def georef_process(crop, pc_path, geo_model_path):
    """
    Georeferencing the point cloud and crop it.

    :param crop:
    :param pc_path:
    :param geo_model_path:
    :return:
    """
    tree = DSTree.tree
    gd = exif_info.gpsinfo_dict
    cmd = ('%s translate -i %s -o %s' % (tree.pdal, pc_path, geo_model_path))
    stages = ["ferry"]
    params = ['--filters.ferry.dimensions=" => UserData"', '--writers.las.compression="lazip"']

    if gd['is_georeferenced']:
        stages.append("transformation")
        params += [
            '--filters.transformation.matrix="1 0 0 %s 0 1 0 %s 0 0 1 0 0 0 0 1"' % (gd['utm_east_offset'], gd['utm_north_offset']),
            '--writers.las.offset_x=%s' % gd['utm_east_offset'],
            '--writers.las.offset_y=%s' % gd['utm_north_offset'],
            '--writers.las.offset_z=0',
            '--writers.las.a_srs="%s"' % gd['proj4']
        ]
        cmd = cmd + ' ' + ' '.join(stages) + ' ' + ' '.join(params) + ' > /dev/null 2>&1'
        run(cmd, "Georeferencing the model.")

        if crop > 0:
            log.logINFO("Calculating cropping area and generating bounds shapefile from point cloud...")
            decimation_step = 40
            cropper.create_bounds_gpkg(geo_model_path, crop, decimation_step=decimation_step)
    else:
        cmd = cmd + ' ' + ' '.join(stages) + ' ' + ' '.join(params) + ' > /dev/null 2>&1'
        run(cmd, "Georeferencing the model (non-georeferenced).")
