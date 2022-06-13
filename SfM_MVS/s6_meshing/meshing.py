import os
from ..s0_dataset import DSTree, log
from ..s0_dataset.runCMD import run
from ..s5_dsm.dem_func import create_dem

tree = DSTree.tree


def clean_mesh(outMeshDirty, outMesh, maxVertexCount):
    """
    Cleanup and reduce vertex count.

    :param outMeshDirty:
    :param outMesh:
    :param maxVertexCount:
    """
    cleanupArgs = {'bin': tree.clean_mesh, 'outfile': outMesh, 'infile': outMeshDirty, 'max_vertex': maxVertexCount}
    cmd = ('{bin} -inputFile {infile} -outputFile {outfile} -removeIslands -decimateMesh {max_vertex}'.format(**cleanupArgs))
    run(cmd, "Cleanup and reduce vertex count.")


def create_3dmesh(inPointCloud, outMesh, depth=11, samples=1.0, maxVertexCount=200000, pointWeight=4.0, threads=1):
    """
    create 3d mesh from point cloud.

    :param inPointCloud:
    :param outMesh:
    :param depth:
    :param samples:
    :param maxVertexCount:
    :param pointWeight:
    :param threads:
    """
    mesh_path, mesh_filename = os.path.split(outMesh)
    basename, ext = os.path.splitext(mesh_filename)
    outMeshDirty = os.path.join(mesh_path, "{}.dirty{}".format(basename, ext))
    # Run PoissonRecon
    poissonReconArgs = {'bin': tree.poisson_recon, 'outfile': outMeshDirty, 'infile': inPointCloud, 'depth': depth,
                        'samples': samples, 'pointWeight': pointWeight, 'threads': threads}
    cmd = ('{bin} --in {infile} --out {outfile} --depth {depth} --pointWeight {pointWeight} --samplesPerNode {samples} '
           '--threads {threads} --linearFit > /dev/null 2>&1'.format(**poissonReconArgs))
    run(cmd, "Run PoissonRecon...")

    clean_mesh(outMeshDirty, outMesh, maxVertexCount)
    os.remove(outMeshDirty)


def create_25dmesh(inDSM, outMesh, maxVertexCount=200000, available_cores=None):
    """
    create 2.5d mesh from dsm.

    :param inDSM:
    :param outMesh:
    :param maxVertexCount:
    :param available_cores:
    """
    mesh_path, mesh_filename = os.path.split(outMesh)
    basename, ext = os.path.splitext(mesh_filename)
    outMeshDirty = os.path.join(mesh_path, "{}.dirty{}".format(basename, ext))

    # Run dem2mesh, lower maxConcurrency if it fails.
    while True:
        try:
            kwargs = {'bin': tree.dem2mesh, 'outfile': outMeshDirty, 'infile': inDSM, 'maxVertexCount': maxVertexCount,
                      'maxConcurrency': available_cores}
            cmd = ('{bin} -inputFile {infile} -outputFile {outfile} -maxTileLength 2000 -maxVertexCount {maxVertexCount} '
                   '-maxConcurrency {maxConcurrency} > /dev/null 2>&1'.format(**kwargs))
            run(cmd, "Run Dem2Mesh...")
            break
        except Exception as e:
            available_cores = int(available_cores / 2)
            if available_cores >= 1:
                log.logWARNING("dem2mesh failed, retrying with lower concurrency.")
            else:
                raise e

    clean_mesh(outMeshDirty, outMesh, maxVertexCount)
    os.remove(outMeshDirty)


def meshing_func(mesh3d, mesh25d, octree_depth, mesh_size, cores):
    """
    create meshes.

    :param mesh3d:
    :param mesh25d:
    :param octree_depth:
    :param mesh_size:
    :param cores:
    """
    if not os.path.exists(tree.meshingDIR):
        os.makedirs(tree.meshingDIR)
    if mesh3d:
        log.logINFO("Creating 3D mesh from filtered point cloud...")
        create_3dmesh(tree.filteredPC, tree.mesh3d, depth=octree_depth, maxVertexCount=mesh_size, threads=cores)
    if mesh25d:
        log.logINFO("Creating DSM for 2.5 D mesh...")
        tmpdir = os.path.join(tree.meshingDIR, 'dsm_tmp')
        os.makedirs(tmpdir)
        create_dem(tree.filteredPC, 'mesh_dsm', output_type='max', radiuses=list(map(str, [0.03, 0.06, 0.12])), outdir=tmpdir,
                   resolution=0.04, max_workers=5)

        log.logINFO("Creating 2.5D mesh from DSM...")
        create_25dmesh(os.path.join(tree.meshingDIR, 'dsm_tmp', 'mesh_dsm.tif'), tree.mesh25d,
                       maxVertexCount=mesh_size, available_cores=cores)
