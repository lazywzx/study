import os, time, shutil
from s0_dataset import DSParameter, log, DSTree


def georeferencing():
    """
    georeferencing the model
    """
    st = time.time()
    tree = DSTree.tree
    args = DSParameter.args
    if not os.path.exists(tree.georeferencingDIR):
        os.makedirs(tree.georeferencingDIR)

    from s4_georeferencing.process_func import georef_process
    log.logINFO("Start georef point cloud stage...")
    georef_process(args.crop, tree.filteredPC, tree.georeferencing_model)
    shutil.copyfile(tree.georeferencing_model, tree.densePC_geo)
    log.logINFO("s4 cost time: " + str(int(time.time() - st)) + " s.")
