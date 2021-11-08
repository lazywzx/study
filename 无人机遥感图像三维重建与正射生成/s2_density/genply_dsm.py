import os
import numpy as np
from ..s0_dataset import log, DSParameter
from ..s5_dsm.dem_func import create_dem


def create_output(vertices, colors, filename):
    """
    Function to create point cloud file.

    :param vertices:
    :param colors:
    :param filename:
    """
    colors = colors.reshape(-1, 3)
    vertices = np.hstack([vertices.reshape(-1, 3), colors])
    np.savetxt(filename, vertices, fmt='%f %f %f %d %d %d')     # 必须先写入，然后利用write()在头部插入ply header
    ply_header = '''ply\nformat ascii 1.0\nelement vertex %(vert_num)d\nproperty float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n'''

    with open(filename, 'r+') as f:
        old = f.read()
        f.seek(0)
        f.write(ply_header % dict(vert_num=len(vertices)))
        f.write(old)


def config_data(infile, output_file):
    """
    config some data.

    :param infile:
    :param output_file:
    """
    # Define name for output file
    data = np.load(infile)
    points = data['points']
    colors = data['colors']
    create_output(points, colors, output_file)


def gen_ply(indir, outdir):
    """
    gen point cloud from depthmap.

    :param indir:
    :param outdir:
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    filelist = os.listdir(indir)
    log.logINFO("Creating point clouds from depthmaps...")
    for file in filelist:
        name1, ext1 = os.path.splitext(file)
        name2, ext2 = os.path.splitext(name1)
        if ext2 == '.pruned':
            name3, ext3 = os.path.splitext(name2)
            name4, ext4 = os.path.splitext(name3)
            filepath = os.path.join(indir, file)
            outfile = os.path.join(outdir, name4 + ".ply")
            config_data(filepath, outfile)
    log.logINFO("Done!")


def gen_dsm(indir, outdir):
    """
    gen dsm from point cloud.

    :param indir:
    :param outdir:
    """
    args = DSParameter.args
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    filelist = os.listdir(indir)
    log.logINFO("Creating DSMs from separate PCs...")
    for file in filelist:
        filepath = os.path.join(indir, file)
        name, ext = os.path.splitext(file)
        create_dem(filepath, name, output_type='max', radiuses=list(map(str, [0.03, 0.06, 0.12])), outdir=outdir,
                   resolution=0.04, max_workers=max(1, args.max_concurrency - 1))

    log.logINFO("Done!")
