import os
from ..s0_dataset import log
from ..s0_dataset.runCMD import run


def related_file_path(input_file_path, prefix="", postfix="", replace_base=None):
    """
    :return related path

    :param input_file_path:
    :param prefix:
    :param postfix:
    :param replace_base:
    """
    path, filename = os.path.split(input_file_path)
    basename, ext = os.path.splitext(filename)

    if replace_base is not None:
        basename = replace_base

    return os.path.join(path, "{}{}{}{}".format(prefix, basename, postfix, ext))


def ply_info(input_ply):
    """
    Read PLY header, check if point cloud has normals

    :param input_ply:
    :return:
    """
    has_normals = False
    has_views = False
    vertex_count = 0

    with open(input_ply, 'r', errors='ignore') as f:
        line = f.readline().strip().lower()
        i = 0
        while line != "end_header":
            line = f.readline().strip().lower()
            props = line.split(" ")
            if len(props) == 3:
                if props[0] == "property" and props[2] in ["nx", "normalx", "normal_x"]:
                    has_normals = True
                if props[0] == "property" and props[2] in ["views"]:
                    has_views = True
                elif props[0] == "element" and props[1] == "vertex":
                    vertex_count = int(props[2])
            i += 1
            if i > 100:
                raise IOError("Cannot find end_header field. Invalid PLY?")
    return {'has_normals': has_normals, 'vertex_count': vertex_count, 'has_views': has_views}


def split(pdalbin, input_point_cloud, outdir, filename_template, capacity, dims=None):
    """
    split a large pointcloud into small pcs

    :param input_point_cloud:
    :param outdir:
    :param filename_template:
    :param capacity:
    :param dims:
    :return:
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    cmd = '%s split -i %s -o %s --capacity %s' % (pdalbin, input_point_cloud, os.path.join(outdir, filename_template), capacity)
    if filename_template.endswith(".ply"):
        cmd += "--writers.ply.sized_types=false --writers.ply.storage_mode='little endian' "
    if dims is not None:
        cmd += '--writers.ply.dims="%s"' % dims

    run(cmd, "Split the large point cloud into small pcs...")

    return [os.path.join(outdir, f) for f in os.listdir(outdir)]


def fast_merge_ply(input_point_cloud_files, output_file):
    """
    merge small pcs into entire one, implement for fast

    :param input_point_cloud_files:
    :param output_file:
    :return:
    """
    log.logINFO("Begin fast merge ply...")
    vertex_count = sum([ply_info(pcf)['vertex_count'] for pcf in input_point_cloud_files])
    master_file = input_point_cloud_files[0]
    with open(output_file, "wb") as out:
        with open(master_file, "r", errors="ignore") as fhead:
            # Copy header
            line = fhead.readline()
            out.write(line.encode('utf8'))

            i = 0
            while line.strip().lower() != "end_header":
                line = fhead.readline()

                # Intercept element vertex field
                if line.lower().startswith("element vertex "):
                    out.write(("element vertex %s\n" % vertex_count).encode('utf8'))
                else:
                    out.write(line.encode('utf8'))

                i += 1
                if i > 100:
                    raise IOError("Cannot find end_header field. Invalid PLY?")

        for ipc in input_point_cloud_files:
            i = 0
            with open(ipc, "rb") as fin:
                # Skip header
                line = fin.readline()
                while line.strip().lower() != b"end_header":
                    line = fin.readline()

                    i += 1
                    if i > 100:
                        raise IOError("Cannot find end_header field. Invalid PLY?")

                # Write fields
                out.write(fin.read())

    return output_file
