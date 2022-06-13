import os
import shutil

from s0_dataset import log, DSTree


def clean_dir(path):
    """clean old dirs."""
    if os.path.exists(path):
        shutil.rmtree(path)


def stages_control(stageControl):
    """
    Run UAV-Mosaic Pipeline.

    :param stageControl:
    """
    tree = DSTree.tree
    # start
    if stageControl["s1"]:
        log.logINFO("#########################Stage1: run Struct from Motion pipeline############################")
        clean_dir(tree.sfmDIR)
        from s1_sfm import s1_main
        s1_main.runSfM()
    else:
        log.logINFO("Skip s1.")

    if stageControl["s2"]:
        log.logINFO("#########################Stage2: run Point Cloud density and visualization###################")
        clean_dir(tree.denseDIR)
        from s2_density import s2_main
        s2_main.dense_visual()
    else:
        log.logINFO("Skip s2.")

    if stageControl["s3"]:
        log.logINFO("#########################Stage3: filter the dense point cloud###############################")
        clean_dir(tree.filterpointsDIR)
        from s3_filter import s3_main
        s3_main.filter_pointcloud()
    else:
        log.logINFO("Skip s3.")

    if stageControl["s4"]:
        log.logINFO("#########################Stage4: georeferencing the model###################################")
        clean_dir(tree.georeferencingDIR)
        from s4_georeferencing import s4_main
        s4_main.georeferencing()
    else:
        log.logINFO("Skip s4.")

    if stageControl["s5"]:
        log.logINFO("#########################Stage5: generating dsm/dtm#########################################")
        clean_dir(tree.dsmDIR)
        from s5_dsm import s5_main
        s5_main.generate_dsm()
    else:
        log.logINFO("Skip s5.")

    if stageControl["s6"]:
        log.logINFO("#########################Stage6: creating meshes###########################################")
        clean_dir(tree.meshingDIR)
        from s6_meshing import s6_main
        s6_main.create_mesh()
    else:
        log.logINFO("Skip s6.")

    if stageControl["s7"]:
        log.logINFO("#########################Stage7: texturing meshes##########################################")
        clean_dir(tree.texturingDIR)
        from s7_texturing import s7_main
        s7_main.texturing_model()
    else:
        log.logINFO("Skip s7.")

    if stageControl["s8"]:
        log.logINFO("#########################Stage8: orthophoto###############################################")
        clean_dir(tree.orthoDIR)
        from s8_orthophoto import s8_main
        s8_main.create_ortho()
    else:
        log.logINFO("Skip s8.")
