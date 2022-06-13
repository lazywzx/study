import exifread
from ..s0_dataset import log


def int_values(tag):
    if isinstance(tag.values, list):
        return [int(v) for v in tag.values]
    else:
        return [int(tag.values)]


def float_values(tag):
    if isinstance(tag.values, list):
        return [float(v.num) / float(v.den) if v.den != 0 else None for v in tag.values]
    else:
        return [float(tag.values.num) / float(tag.values.den) if tag.values.den != 0 else None]


def int_value(tag):
    v = int_values(tag)
    if len(v) > 0:
        return v[0]


def float_value(tag):
    v = float_values(tag)
    if len(v) > 0:
        return v[0]


def dms_to_decimal(dms, sign):
    """Converts dms coords to decimal degrees"""
    degrees, minutes, seconds = float_values(dms)
    if degrees is not None and minutes is not None and seconds is not None:
        return (-1 if sign.values[0] in 'SWsw' else 1) * (degrees + minutes / 60 + seconds / 3600)


def parse_gps_values(path_file):
    """
    extract gps altitude, latitude, longitude info from image.

    :param path_file:
    :return: info_dict
    """
    with open(path_file, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        altitude = None
        latitude = None
        longitude = None
        try:
            if 'GPS GPSAltitude' in tags:
                altitude = float_value(tags['GPS GPSAltitude'])
                if 'GPS GPSAltitudeRef' in tags and int_value(tags['GPS GPSAltitudeRef']) > 0:
                    altitude *= -1
            if 'GPS GPSLatitude' in tags and 'GPS GPSLatitudeRef' in tags:
                latitude = dms_to_decimal(tags['GPS GPSLatitude'], tags['GPS GPSLatitudeRef'])
            if 'GPS GPSLongitude' in tags and 'GPS GPSLongitudeRef' in tags:
                longitude = dms_to_decimal(tags['GPS GPSLongitude'], tags['GPS GPSLongitudeRef'])
        except (IndexError, ValueError) as e:
            log.logWARNING("Cannot read basic EXIF tags for %s: %s" % (path_file, str(e)))

        return {'altitude': altitude, 'latitude': latitude, 'longitude': longitude}
