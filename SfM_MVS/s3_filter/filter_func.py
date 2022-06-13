import shutil, os
from s0_dataset import log
from s0_dataset.runCMD import run
from s0_dataset.parallel import parallel_map
from .split_merge import split, fast_merge_ply, ply_info, related_file_path


def filter_one_pc(pdalbin, input_point_cloud, output_point_cloud, standard_deviation=2.5, meank=16, sample_radius=0):
    """
    filter one pointcloud in single threshold

    :param input_point_cloud:
    :param output_point_cloud:
    :param standard_deviation:
    :param meank:
    :param sample_radius:
    """
    info = ply_info(input_point_cloud)
    dims = "x=float,y=float,z=float,"
    if info['has_normals']:
        dims += "nx=float,ny=float,nz=float,"
    dims += "red=uchar,blue=uchar,green=uchar"
    if info['has_views']:
        dims += ",views=uchar"

    filters = []

    if sample_radius > 0:
        filters.append('sample')

    if standard_deviation > 0 and meank > 0:
        filters.append('outlier')

    if len(filters) > 0:
        filters.append('range')

    # Process point cloud (or a point cloud submodel) in a single step
    filterArgs = {'bin': pdalbin, 'inputFile': input_point_cloud, 'outputFile': output_point_cloud,
                  'stages': " ".join(filters), 'dims': dims}

    cmd = ("{bin} translate -i {inputFile} -o {outputFile} {stages} --writers.ply.sized_types=false "
           "--writers.ply.storage_mode='little endian' --writers.ply.dims=\"{dims}\" ").format(**filterArgs)

    if 'sample' in filters:
        cmd += "--filters.sample.radius={} ".format(sample_radius)
    if 'outlier' in filters:
        cmd += ("--filters.outlier.method='statistical' --filters.outlier.mean_k={} "
                "--filters.outlier.multiplier={} ").format(meank, standard_deviation)
    if 'range' in filters:
        # Remove outliers
        cmd += "--filters.range.limits='Classification![7:7]' "

    run(cmd, "Filter a pc.")


def parallel_process(pdalbin, input_point_cloud, output_point_cloud, standard_deviation, meank, sample_radius,
                     max_concurrency, VERTEX_THRESHOLD):
    """
    parallel process multiple pointcloud files

    :param input_point_cloud:
    :param output_point_cloud:
    :param standard_deviation:
    :param meank:
    :param sample_radius:
    :param max_concurrency:
    :param VERTEX_THRESHOLD:
    """
    info = ply_info(input_point_cloud)
    dims = "x=float,y=float,z=float,"
    if info['has_normals']:
        dims += "nx=float,ny=float,nz=float,"
    dims += "red=uchar,blue=uchar,green=uchar"
    if info['has_views']:
        dims += ",views=uchar"

    partsdir = os.path.join(os.path.dirname(output_point_cloud), "parts")
    point_cloud_submodels = split(pdalbin, input_point_cloud, partsdir, "part.ply", capacity=VERTEX_THRESHOLD, dims=dims)

    def run_filter(pcs):
        # Recurse
        filter_one_pc(pdalbin, pcs['path'], related_file_path(pcs['path'], postfix="_filtered"),
                      standard_deviation=standard_deviation, meank=meank, sample_radius=sample_radius)

    # Filter
    parallel_map(run_filter, [{'path': p} for p in point_cloud_submodels], max_concurrency)
    # Merge
    filtered_pcs = [related_file_path(pcs, postfix="_filtered") for pcs in point_cloud_submodels]
    # merge_ply(filtered_pcs, output_point_cloud, dims)
    fast_merge_ply(filtered_pcs, output_point_cloud)
    log.logINFO("Successfully merge the pcs!")
    if os.path.exists(partsdir):
        shutil.rmtree(partsdir, ignore_errors=True)
        log.logINFO("Remove the tmp dir and files.")


def filterpc(pdalbin, input_point_cloud, output_point_cloud, standard_deviation=2.5, meank=16,
             sample_radius=0, max_concurrency=1):
    """
    Filters a point cloud
    :param input_point_cloud:
    :param output_point_cloud:
    :param standard_deviation:
    :param meank:
    :param sample_radius:
    :param verbose:
    :param max_concurrency:
    """
    if (standard_deviation <= 0 or meank <= 0) and sample_radius <= 0:
        shutil.copy(input_point_cloud, output_point_cloud)
        log.logINFO("Do not need to filter the pc, skip this step.")
        return

    info = ply_info(input_point_cloud)
    VERTEX_THRESHOLD = 250000
    ss = max_concurrency > 1 and info['vertex_count'] > VERTEX_THRESHOLD * 2
    if ss:
        log.logINFO("The pc is too large, it should be split. Vertex count: " + str(info['vertex_count']))
        parallel_process(pdalbin, input_point_cloud, output_point_cloud, standard_deviation, meank, sample_radius,
                         max_concurrency, VERTEX_THRESHOLD)
    else:
        log.logINFO("The pc can be processed by one step.")
        filter_one_pc(pdalbin, input_point_cloud, output_point_cloud, standard_deviation, meank, sample_radius)
