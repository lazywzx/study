import itertools
import cv2, os
import numpy as np
from plyfile import PlyData
from ..s0_dataset import log


def separate_ortho(filename, output):
    """
    gen orthophotos from point cloud.

    :param filename:
    :param output:
    """
    plydata = PlyData.read(filename)
    points = plydata['vertex'].data
    length = len(points[0])
    points = list(itertools.chain.from_iterable(points))
    point_array = np.array(points).reshape(int(len(points) / length), length)
    # def img scale
    xmax = max(point_array[:, 0])
    xmin = min(point_array[:, 0])
    ymax = max(point_array[:, 1])
    ymin = min(point_array[:, 1])

    x_scale = int((xmax - xmin) * 32)
    x_bais = int((xmax - ymin) * 0.5)
    y_scale = int((ymax - ymin) * 32)
    y_bais = int((ymax - ymin) * 0.5)

    # copy points and colors
    copy_point = np.zeros((len(point_array), 2))
    copy_color = np.zeros((len(point_array), 3))
    # expand point
    copy_point[:, 0] = (point_array[:, 0] - xmin) * 30
    copy_point[:, 1] = (point_array[:, 1] - ymin) * 30
    # def color
    if length == 11:
        copy_color[:, 0] = point_array[:, 8]
        copy_color[:, 1] = point_array[:, 7]
        copy_color[:, 2] = point_array[:, 6]
    else:
        copy_color[:, 0] = point_array[:, 5]
        copy_color[:, 1] = point_array[:, 4]
        copy_color[:, 2] = point_array[:, 3]

    img = np.zeros((x_scale, y_scale, 3), dtype=np.uint8)
    for i in range(len(copy_point)):
        for c in range(3):
            img[int(copy_point[i][0]) + x_bais][int(copy_point[i][1]) + y_bais][c] = copy_color[i][c]

    # dilate and erosion
    kernel = np.ones((9, 9), np.uint8)
    dilate = cv2.dilate(img, kernel)
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(dilate, kernel)

    cv2.imwrite(output, erosion)


def ortho_ply(indir, outdir):
    """
    export orthos from plys.

    :param indir:
    :param outdir:
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    log.logINFO("Creating ortho-photos from PCs...")
    filelist = os.listdir(indir)
    for file in filelist:
        filepath = os.path.join(indir, file)
        name, ext = os.path.splitext(file)
        outpath = os.path.join(outdir, name + ".jpg")
        separate_ortho(filepath, outpath)
