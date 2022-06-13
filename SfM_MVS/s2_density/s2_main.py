import shutil, os, sys, time
from ..s0_dataset import log, DSTree, DSParameter


def dense_visual():
    """
    density point cloud and visualization
    """
    st = time.time()
    tree = DSTree.tree
    args = DSParameter.args
    # check dirs
    if not os.path.exists(tree.sfmDIR):
        log.logERROR("The SfM DIR is not existed! Can not process.")
        sys.exit()
    elif os.path.exists(tree.input_images):
        shutil.move(tree.input_images, os.path.join(tree.sfmDIR, 'images'))
    if not os.path.exists(tree.denseDIR):
        os.makedirs(tree.denseDIR)

    from ..s2_density import genply_dsm, export_ortho
    from ..s2_density.density_visualization import dense_recon, flight_track, draw_matches, feature_vis, plot_density
    log.logINFO("Start run density process...")
    dense_recon(tree.opensfm, tree.sfmDIR)
    # move to result
    shutil.move(tree.merged_ply, tree.densePC)

    log.logINFO("Visualization some files...This will take a while.")
    if args.vis_track:
        flight_track(tree.osfm_exif, tree.osfm_flight)
    if args.vis_matche:
        draw_matches(tree.plot_matches, tree.sfmDIR)
        # move to result
        shutil.move(tree.osfm_plot_tracks, tree.osfm_plot_matches)  # move to result

    shutil.move(os.path.join(tree.sfmDIR, 'images'), tree.input_images) # move back
    if args.vis_feature:
        feature_vis(tree.osfm_features, tree.input_images, tree.osfm_draw_feat)

    # gen pc from dmap
    if args.exp_ply:
        genply_dsm.gen_ply(os.path.dirname(tree.merged_ply), os.path.join(tree.resultDIR, "separate_pcs"))

    # gen dsm from pc
    if args.exp_dsm:
        genply_dsm.gen_dsm(os.path.join(tree.resultDIR, "separate_pcs"), os.path.join(tree.resultDIR, "separate_dsm"))
    # export orthos from pc
    if args.exp_ortho:
        # export_ortho.ortho_ply(os.path.join(tree.resultDIR, "separate_pcs"), os.path.join(tree.resultDIR, "separate_ortho"))
        export_ortho.ortho_ply(tree.denseDIR, tree.resultDIR)

    # plot sparse and dense pc's density
    if args.plot_den:
        plot_density(tree.osfm_recon, os.path.join(tree.resultDIR, "density_sparse_PC.png"))
        plot_density(tree.densePC, os.path.join(tree.resultDIR, "density_dense_PC.png"))

    log.logINFO("s2 cost time: " + str(int(time.time() - st)) + " s.")
