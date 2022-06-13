import time, os, sys
from src.s0_dataset import log, DSTree
from src.stages import stages_control

st = time.time()
tree = DSTree.tree
# remove log
if os.path.exists(tree.logpath):
    os.remove(tree.logpath)
# check path
if not os.path.exists(tree.root_path):
    log.logERROR("ROOT path is not existed! EXIT")
    sys.exit()
if not os.path.exists(tree.resultDIR):
    os.makedirs(tree.resultDIR)

# control dict
stageControl = {
    "s1": True,
    "s2": True,
    "s3": True,
    "s4": True,
    "s5": True,
    "s6": True,
    "s7": True,
    "s8": True
}

log.logINFO("Start UAV-based imagery ortho and mosaic...")
stages_control(stageControl)
log.logINFO("Run successfully! Pipeline is over.")
if os.path.exists("./dem2mesh.txt"):
    os.remove("./dem2mesh.txt")
log.logINFO("Total time: " + str(int((time.time() - st) / 60.0)) + " m.")
