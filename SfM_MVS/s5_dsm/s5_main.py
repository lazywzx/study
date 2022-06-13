import os, time
from ..s0_dataset import log, DSTree


def generate_dsm():
    """
    Generating dsm and/or dtm.
    """
    st = time.time()
    tree = DSTree.tree
    if not os.path.exists(tree.dsmDIR):
        os.makedirs(tree.dsmDIR)

    from ..s5_dsm.dem_proc import dem_process
    log.logINFO("Start generating dsm...")
    dem_process(tree.dsmDIR, tree.georeferencing_model, tree.dem_model, tree.gpkgfile, tree.resultDIR)
    log.logINFO("s5 cost time: " + str(int(time.time() - st)) + " s.")
