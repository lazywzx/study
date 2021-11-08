import xmltodict
from xml.parsers.expat import ExpatError
from six import string_types


# From https://github.com/mapillary/OpenSfM/blob/master/opensfm/exif.py
def get_xmp(file):
    """
    get xmp info.

    :param file:
    :return:
    """
    img_bytes = file.read()
    xmp_start = img_bytes.find(b'<x:xmpmeta')
    xmp_end = img_bytes.find(b'</x:xmpmeta')

    if xmp_start < xmp_end:
        xmp_str = img_bytes[xmp_start:xmp_end + 12].decode('utf8')
        try:
            xdict = xmltodict.parse(xmp_str)
        except ExpatError as e:
            from bs4 import BeautifulSoup
            xmp_str = str(BeautifulSoup(xmp_str, 'xml'))
            xdict = xmltodict.parse(xmp_str)

        xdict = xdict.get('x:xmpmeta', {})
        xdict = xdict.get('rdf:RDF', {})
        xdict = xdict.get('rdf:Description', {})
        if isinstance(xdict, list):
            return xdict
        else:
            return [xdict]
    else:
        return []


def get_xmp_tag(xmp_tags, tags):
    """
    get xmp tag info.

    :param xmp_tags:
    :param tags:
    :return:
    """
    if isinstance(tags, str):
        tags = [tags]
    for tag in tags:
        if tag in xmp_tags:
            t = xmp_tags[tag]
            if isinstance(t, string_types):
                return str(t)
            elif isinstance(t, dict):
                items = t.get('rdf:Seq', {}).get('rdf:li', {})
                if items:
                    if isinstance(items, string_types):
                        return items
                    return " ".join(items)
            elif isinstance(t, int) or isinstance(t, float):
                return t
    return None


def set_attr_from_xmp_tag(xmp_tags, tags):
    """
    set gps_xy_stddev and gps_z_stddev.

    :param xmp_tags:
    :param tags:
    :return:
    """
    v = get_xmp_tag(xmp_tags, tags)
    if v is not None:
        if "/" in v:
            parts = v.split("/")
            if len(parts) == 2:
                try:
                    num, den = map(float, parts)
                    if den != 0:
                        v = num / den
                    else:
                        v = v
                except ValueError:
                    pass
        return float(v)
    return None


def parse_dop_values(path_file):
    """
    extract gps_xy and gps_z.

    :param path_file:
    :return:
    """
    with open(path_file, 'rb') as f:
        # Extract XMP tags
        f.seek(0)
        xmp = get_xmp(f)
        for tags in xmp:
            if '@drone-dji:RtkStdLon' in tags:
                y = float(get_xmp_tag(tags, '@drone-dji:RtkStdLon'))
                x = float(get_xmp_tag(tags, '@drone-dji:RtkStdLat'))
                gps_xy_stddev = max(x, y)

                if '@drone-dji:RtkStdHgt' in tags:
                    gps_z_stddev = float(get_xmp_tag(tags, '@drone-dji:RtkStdHgt'))
            else:
                gps_xy_stddev = set_attr_from_xmp_tag(tags, ['@Camera:GPSXYAccuracy', 'GPSXYAccuracy'])
                gps_z_stddev = set_attr_from_xmp_tag(tags, ['@Camera:GPSZAccuracy', 'GPSZAccuracy'])
        return {"gps_xy_stddev": gps_xy_stddev, "gps_z_stddev": gps_z_stddev}
