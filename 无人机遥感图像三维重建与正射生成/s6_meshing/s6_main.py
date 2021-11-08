import time
from ..s0_dataset import DSParameter, log


def create_mesh():
    """
    create meshes.
    """
    st = time.time()
    args = DSParameter.args
    from ..s6_meshing.meshing import meshing_func
    log.logINFO("Start creating meshes...")
    meshing_func(args.mesh3d, args.mesh25d, args.mesh_octree_depth, args.mesh_size, max(1, args.max_concurrency - 3))
    log.logINFO("s6 cost time: " + str(int(time.time() - st)) + " s.")
