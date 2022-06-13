import subprocess
from ..s0_dataset import log


def run(cmd, info=None, ret=False):
    """
    run command in shell, and out some info

    :param cmd:
    :param info:
    :param ret:
    """
    if info is not None:
        log.logINFO(info + " CMD: " + cmd)
    p = subprocess.Popen(cmd, shell=True)
    retcode = p.wait()
    if ret:
        if not retcode:
            log.logINFO("Run successfully!")
        else:
            log.logERROR("Run failed!")
