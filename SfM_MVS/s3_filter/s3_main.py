import os, time
from ..s0_dataset import DSParameter, log, DSTree


def filter_pointcloud():
    """
    filter a point cloud from last step, i.e: dense
    """
    st = time.time()
    tree = DSTree.tree
    args = DSParameter.args
    if not os.path.exists(tree.filterpointsDIR):
        os.makedirs(tree.filterpointsDIR)

    from ..s3_filter.filter_func import filterpc
    log.logINFO("Start filter point cloud stage...")
    filterpc(tree.pdal, tree.densePC, tree.filteredPC, standard_deviation=args.pc_filter, sample_radius=args.pc_sample,
             max_concurrency=args.max_concurrency)
    log.logINFO("s3 cost time: " + str(int(time.time() - st)) + " s.")
