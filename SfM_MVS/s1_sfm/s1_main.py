import os, time, shutil, sys, json
from ..s0_dataset import log, DSTree


def runSfM():
    """
    run Struct from Motion pipeline
    """
    st = time.time()
    tree = DSTree.tree
    if not os.path.exists(tree.sfmDIR):
        os.makedirs(tree.sfmDIR)
        if not os.path.exists(tree.input_images):
            log.logERROR("Dir images/ is not existed!")
            sys.exit()
        else:
            from ..s1_sfm import sfm_pl, exif_info
            shutil.move(tree.input_images, os.path.join(tree.sfmDIR, 'images'))

            log.logINFO("Start run Struct from Motion...")
            # gps info
            gpsinfo = exif_info.gpsinfo_dict
            exif_overrides = gpsinfo['exif']  # write override exif file

            with open(tree.osfm_exif_override, 'w') as f:
                f.write(json.dumps(exif_overrides))

            # pipeline
            sfm_pl.osfm_pipeline(gpsinfo, tree.config_yaml, tree.opensfm, tree.sfmDIR)
            shutil.move(tree.osfm_sparse, tree.osfm_recon) # move to result
            shutil.move(os.path.join(tree.sfmDIR, 'images'), tree.input_images)  # move back to root path
            log.logINFO("s1 cost time: " + str(int(time.time() - st)) + " s.")
