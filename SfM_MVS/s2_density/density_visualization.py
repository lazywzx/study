import os, json, random, cv2
import numpy as np
from plyfile import PlyData
import itertools
from matplotlib import pyplot as plt
import matplotlib
from ..s0_dataset import log
from ..s0_dataset.runCMD import run


def dense_recon(bin, ds_path):
    """
    density point cloud

    :param bin:
    :param ds_path:
    :param debug:
    """
    log.logINFO("Density point cloud... This will take a while, please wait for minutes.")
    for task in ['undistort', 'export_visualsfm --points', 'compute_depthmaps']:
        cmd = " ".join([bin, task, ds_path, ' > /dev/null 2>&1'])
        run(cmd, "Run " + task + "...")


"""funcs for drawing the track of flight"""


class Photo(object):
    """
    save photos exif info
    """
    def __init__(self, name, lat, lon, alt, time):
        self.name = name
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt
        self.time = time


def flight_track(exif_path, output_path, expand=500000, bound=1.3):
    """
    Draw the flight track from exif info.

    :param exif_path:
    :param output_path:
    :param expand:
    :param bound:
    """
    log.logINFO("Extracting info from exif files.")
    # extract exif info
    filelist = os.listdir(exif_path)
    photo_list = []
    for path in filelist:
        datapath = os.path.join(exif_path, path)
        with open(datapath, "r") as file:
            data = json.load(file)
        photo_list.append(Photo(path, data["gps"]["latitude"], data["gps"]["longitude"], data["gps"]["altitude"],
                                data["capture_time"]))

    # sort for capture time
    def time_sort(elem):
        return elem.time
    photo_list.sort(key=time_sort)

    # compute img info
    # width
    lat_min = min([k.latitude for k in photo_list])
    lat_max = max([k.latitude for k in photo_list])
    width = int((lat_max - lat_min) * expand * bound)
    wid_bais = int(width * (bound - 1) / 2)
    # length
    lon_min = min([k.longitude for k in photo_list])
    lon_max = max([k.longitude for k in photo_list])
    length = int((lon_max - lon_min) * expand * bound)
    len_bais = int(length * (bound - 1) / 2)
    # scale
    alt_min = min([k.altitude for k in photo_list])
    alt_max = max([k.altitude for k in photo_list])
    alt = int(alt_max - alt_min)

    scale = min(width, length) / (len(filelist) * 0.3)

    # create and draw
    track_img = np.ones((width, length, 3), np.uint8) * 255
    log.logINFO("Drawing photo nodes.")
    for i in range(len(photo_list)):
        photo_list[i].latitude = int((photo_list[i].latitude - lat_min) * expand + wid_bais)
        photo_list[i].longitude = int((photo_list[i].longitude - lon_min) * expand + len_bais)
        photo_list[i].altitude = int((photo_list[i].altitude - alt_min) / alt * 5 + scale)
        if i == 0:
            color = (0, 255, 0)
        elif i == len(photo_list) - 1:
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)
        cv2.circle(track_img, (photo_list[i].longitude, photo_list[i].latitude), photo_list[i].altitude, color, 3)

        if i > 0:
            cv2.line(track_img, (photo_list[i - 1].longitude, photo_list[i - 1].latitude), (photo_list[i].longitude, photo_list[i].latitude), (0, 0, 0), 2)

    # save to file0
    cv2.imwrite(output_path, track_img)


"""funcs for drawing features/matches"""


def draw_features(img, x, y, scale, orien, destype='circle'):
    """
    draw features on image

    :param img:
    :param x:
    :param y:
    :param scale:
    :param orien: must be radius
    :param destype:
    :return:
    """
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    x = int(x)
    y = int(y)
    scale = int(scale)
    lx = int(scale * np.cos(orien) + x)
    ly = int(scale * np.sin(orien) + y)

    # drawing type
    if destype == 'arrowed':
        cv2.arrowedLine(img, (x, y), (lx, ly), color, 2, 8, 0, 0.3)
    else:
        cv2.circle(img, (x, y), scale, color, 5)
        cv2.line(img, (x, y), (lx, ly), color, 5)

    return img


def extract_imgname(npz_name):
    """
    extract image name from npz file

    :param npz_name:
    :return:
    """
    name, ext = os.path.splitext(npz_name)
    imgname, feaext = os.path.splitext(name)
    return imgname


def feature_vis(feature_path, img_path, output_path):
    """
    visualize features on images

    :param feature_path:
    :param img_path:
    :param output_path:
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    featlist = os.listdir(feature_path)
    for npzname in featlist:
        imgname = extract_imgname(npzname)
        log.logINFO("Drawing features on img: " + imgname)
        # read image
        rawimg = cv2.imread(os.path.join(img_path, imgname))
        drawimg = rawimg.copy()
        height = drawimg.shape[0]
        weight = drawimg.shape[1]
        # read points
        feat_path = os.path.join(feature_path, npzname)
        points = (np.load(feat_path))['points']
        for p in points:
            x = (p[0] + 0.5) * weight
            y = (p[1] + float(height) / weight / 2) * weight
            scale = p[2] * weight
            orien = np.deg2rad(p[3])
            drawimg = draw_features(drawimg, x, y, scale, orien)
        # put text -points: num- on image
        cv2.putText(drawimg, "points: " + str(len(points)), (int(weight * 0.05), int(height * 0.05)),
                    cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 8)
        small_img = cv2.resize(drawimg, (int(weight / 4), int(height / 4)))
        cv2.imwrite(os.path.join(output_path, "draw_" + imgname), small_img)  # save to file


def draw_matches(bin, ds_path):
    """
    draw matches between two images

    :param bin:
    :param ds_path:
    """
    cmd = " ".join([bin, '--save_figs', ds_path, ' > /dev/null 2>&1'])
    run(cmd, "Drawing matches...It will take a while.")


"""funcs for drawing density"""


def stat(mat, output):
    """
    plot density dist

    :param mat:
    """
    xscale = int(max(mat[:, 0]))
    yscale = int(max(mat[:, 1]))
    tmpmat = np.zeros((xscale, yscale), dtype=np.uint32)
    mask = np.zeros((len(mat), 2), dtype=np.bool)
    for i in range(xscale):
        for j in range(yscale):
            mask[:, 0] = (mat[:, 0] >= i) * (mat[:, 0] < i + 1)
            mask[:, 1] = (mat[:, 1] >= j) * (mat[:, 1] < j + 1)
            tmpmat[i][j] = mask.sum()

    # num of per
    numper = 30
    per = int(tmpmat.max() / numper)
    xaxis = list(range(numper + 1))
    yaxis = np.zeros(numper + 1)
    for k in xaxis:
        yaxis[k] = ((tmpmat >= k * per) * (tmpmat < (k + 1) * per)).sum()
    # save fig
    # config font
    font = {'family': 'YaHei Consolas Hybrid', 'size': 10}
    matplotlib.rc('font', **font)
    plt.title("点云密度分布情况")
    plt.xlabel("密度区间（* " + str(per) + ")")
    plt.ylabel("各密度区间的数量")
    plt.plot(xaxis, yaxis)
    plt.savefig(output)


def plot_density(filename, output):
    """
    stat density

    :param filename:
    """
    plydata = PlyData.read(filename)
    points = plydata['vertex'].data
    length = len(points[0])
    points = list(itertools.chain.from_iterable(points))
    point_array = np.array(points).reshape(int(len(points) / length), length)
    # axis bias
    mat = np.zeros((len(point_array[:, 0]), 2), dtype=np.float)
    mat[:, 0] = point_array[:, 0]
    mat[:, 1] = point_array[:, 1]
    minx = min(mat[:, 0])
    miny = min(mat[:, 1])
    mat[:, 0] -= minx
    mat[:, 1] -= miny
    stat(mat, output)
