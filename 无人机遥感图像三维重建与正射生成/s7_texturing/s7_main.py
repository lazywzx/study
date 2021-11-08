import time
from ..s0_dataset import log


def texturing_model():
    """
    create textured models.
    """
    st = time.time()
    log.logINFO("Start texturing meshing models...")
    from ..s7_texturing import texturing
    texturing.textur_process()
    log.logINFO("s7 cost time: " + str(int(time.time() - st)) + " s.")
