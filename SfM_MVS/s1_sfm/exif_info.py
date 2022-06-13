import math, pyproj, os
from s0_dataset import log, DSTree, DSParameter
from s1_sfm import extract_gps, extract_dop

tree = DSTree.tree
args = DSParameter.args


def parse_srs_header(header):
    """
    Parse a header coming from GCP or coordinate file
    :param header (str) line
    :return Proj object
    """
    log.logINFO('Parsing SRS header: %s' % header)
    header = header.strip()
    ref = header.split(' ')
    if ref[0] == 'WGS84' and ref[1] == 'UTM':
        datum = ref[0]
        utm_pole = (ref[2][len(ref[2]) - 1]).upper()
        utm_zone = int(ref[2][:len(ref[2]) - 1])

        proj_args = {'zone': utm_zone, 'datum': datum}

        proj4 = '+proj=utm +zone={zone} +datum={datum} +units=m +no_defs=True'
        if utm_pole == 'S':
            proj4 += ' +south=True'

        srs = pyproj.CRS.from_proj4(proj4.format(**proj_args))
    elif '+proj' in header:
        srs = pyproj.CRS.from_proj4(header.strip('\''))
    elif header.lower().startswith("epsg:"):
        srs = pyproj.CRS.from_epsg(header.lower()[5:])
    else:
        raise RuntimeError('Could not parse coordinates. Bad SRS supplied: %s' % header)

    return srs


def get_gps_dop(gps_xy_stddev, gps_z_stddev):
    """
    get dop val from gps_xy_stddev and gps_z_stddev

    :param gps_xy_stddev:
    :param gps_z_stddev:
    :return: dop
    """
    val = None
    if gps_xy_stddev is not None:
        val = gps_xy_stddev
    if gps_z_stddev is not None:
        val = max(val, gps_z_stddev)
    return val


def extract_utm_coords(photos_path):
    """
    Create a coordinate file containing the GPS positions of all cameras to be used later in the ODM toolchain for
    automatic georeferecing

    :param photos_path list of photos
    :return srs, dx, dy, exif_override
    """
    utm_zone = None
    hemisphere = None
    proj4 = None
    dx = 0
    dy = 0
    coords = []
    exif_override = {}

    photos = os.listdir(photos_path)
    for photo in photos:
        image_path = os.path.join(tree.input_images, photo)
        gd = extract_gps.parse_gps_values(image_path)
        if gd['latitude'] is None or gd['longitude'] is None:
            log.logWARNING("GPS position not available for %s" % photo)
            continue

        gps_dop = extract_dop.parse_dop_values(image_path)
        dop = get_gps_dop(gps_dop["gps_xy_stddev"], gps_dop["gps_z_stddev"])
        if dop is None:
            dop = args.gps_accuracy
        exif_override[photo] = {
            'gps': {
                'latitude': gd['latitude'],
                'longitude': gd['longitude'],
                'altitude': gd['altitude'] if gd['altitude'] is not None else 0,
                'dop': dop
            }
        }

        if utm_zone is None:
            utm_zone = (int(math.floor((gd['longitude'] + 180.0) / 6.0)) % 60) + 1
            hemisphere = 'S' if gd['latitude'] < 0 else 'N'

        if hemisphere == 'N':
            p = pyproj.Proj(proj='utm', zone=utm_zone, ellps='WGS84', preserve_units=True)
        else:
            p = pyproj.Proj(proj='utm', zone=utm_zone, ellps='WGS84', preserve_units=True, south=True)
        x, y = p(gd['longitude'], gd['latitude'])

        alt = gd['altitude'] if gd['altitude'] is not None else 0
        coord = [x, y, alt]
        coords.append(coord)

    if utm_zone is not None:
        line = ("WGS84 UTM %s%s" % (utm_zone, hemisphere))
        srs = parse_srs_header(line)
        proj4 = srs.to_proj4()

        # Calculate average
        dx = 0.0
        dy = 0.0
        num = float(len(coords))
        for coord in coords:
            dx += coord[0] / num
            dy += coord[1] / num

        dx = int(math.floor(dx))
        dy = int(math.floor(dy))

    return proj4, dx, dy, exif_override


def georeference_with_gps(photos_path, coords_path):
    """
    Extract the gps info from images.

    :param photos_path:
    :param coords_path:
    :return:
    """
    proj4, utm_east_offset, utm_north_offset, exif_override = extract_utm_coords(photos_path)
    log.logINFO("Writing GPS info to coords file.")
    with open(coords_path, 'w+') as coord:
        coord.write(str(utm_east_offset) + "\n")
        coord.write(str(utm_north_offset) + "\n")
        if proj4 is not None:
            coord.write(proj4 + '\n')
        else:
            coord.write('None\n')
        coord.close()

    ig = True if proj4 is not None or utm_east_offset != 0 or utm_north_offset != 0 else False
    return {'is_georeferenced': ig, 'utm_east_offset': utm_east_offset, 'utm_north_offset': utm_north_offset,
            'proj4': proj4, 'exif': exif_override}


gpsinfo_dict = georeference_with_gps(tree.input_images, tree.gps_txt)
