import time
from ..s0_dataset import log


def create_ortho():
    """
    create orthophotos.
    """
    st = time.time()
    log.logINFO("Start creating orthophotos...")
    from ..s8_orthophoto import orthophoto
    orthophoto.create_orthophoto()
    log.logINFO("s8 cost time: " + str(int(time.time() - st)) + " s.")
