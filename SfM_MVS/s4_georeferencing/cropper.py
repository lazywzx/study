import os, json
from osgeo import ogr
from s0_dataset import log, DSTree
from s0_dataset.runCMD import run

tree = DSTree.tree


def create_bounds_geojson(pointcloud_path, buffer_distance=0, decimation_step=40):
    """
    Compute a buffered polygon around the data extents (not just a bounding box) of the given point cloud.
    @return filename to GeoJSON containing the polygon
    """
    # Do decimation prior to extracting boundary information
    decimated_pointcloud_path = os.path.join(tree.georeferencingDIR, 'decimated.las')
    cmd = ('{} translate -i {} -o {} decimation --filters.decimation.step={}'.format(
        tree.pdal, pointcloud_path, decimated_pointcloud_path, decimation_step))
    run(cmd, "Decimation for the model.")

    # Use PDAL to dump boundary information then read the information back
    boundary_file_path = os.path.join(tree.georeferencingDIR, 'boundary.json')
    cmd = ('{0} info --boundary --filters.hexbin.edge_size=1 --filters.hexbin.threshold=0 {1} > {2}'.format(
        tree.pdal, decimated_pointcloud_path, boundary_file_path))
    run(cmd, "Dump boundary info of the model.")
    os.remove(decimated_pointcloud_path)    # remove some large files

    with open(boundary_file_path, 'r') as f:
        json_f = json.loads(f.read())
        pc_geojson_boundary_feature = json_f['boundary']['boundary_json']

    if pc_geojson_boundary_feature is None:
        raise RuntimeError("Could not determine point cloud boundaries")

    # Write bounds to GeoJSON
    bounds_geojson_path = os.path.join(tree.georeferencingDIR, 'bounds.geojson')
    with open(bounds_geojson_path, "w") as f:
        f.write(json.dumps({"type": "FeatureCollection", "features": [{"type": "Feature",
                                                                       "geometry": pc_geojson_boundary_feature}]}))

    # Create a convex hull around the boundary as to encompass the entire area (no holes)
    driver = ogr.GetDriverByName('GeoJSON')
    ds = driver.Open(bounds_geojson_path, 0)  # ready-only
    layer = ds.GetLayer()

    # Collect all Geometry
    geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
    for feature in layer:
        geomcol.AddGeometry(feature.GetGeometryRef())

    # Calculate convex hull
    convexhull = geomcol.ConvexHull()

    # If buffer distance is specified
    # Create two buffers, one shrinked by
    # N + 3 and then that buffer expanded by 3
    # so that we get smooth corners. \m/
    BUFFER_SMOOTH_DISTANCE = 3
    if buffer_distance > 0:
        # For small areas, check that buffering doesn't obliterate our hull
        tmp = convexhull.Buffer(-(buffer_distance + BUFFER_SMOOTH_DISTANCE))
        tmp = tmp.Buffer(BUFFER_SMOOTH_DISTANCE)
        if tmp.Area() > 0:
            convexhull = tmp
        else:
            log.logWARNING("Very small crop area detected, we will not smooth it.")

    # Save to a new file
    if os.path.exists(bounds_geojson_path):
        driver.DeleteDataSource(bounds_geojson_path)

    out_ds = driver.CreateDataSource(bounds_geojson_path)
    layer = out_ds.CreateLayer("convexhull", geom_type=ogr.wkbPolygon)

    feature_def = layer.GetLayerDefn()
    feature = ogr.Feature(feature_def)
    feature.SetGeometry(convexhull)
    layer.CreateFeature(feature)

    return bounds_geojson_path


def create_bounds_gpkg(pointcloud_path, buffer_distance=0, decimation_step=40):
    """
    Compute a buffered polygon around the data extents (not just a bounding box) of the given point cloud.
    @return filename to Geopackage containing the polygon
    """
    bounds_geojson_path = create_bounds_geojson(pointcloud_path, buffer_distance, decimation_step)
    summary_file_path = os.path.join(tree.georeferencingDIR, 'summary.json')
    cmd = ('{0} info --summary {1} > {2}'.format(tree.pdal, pointcloud_path, summary_file_path))
    run(cmd, "Export summary json.")

    with open(summary_file_path, 'r') as f:
        json_f = json.loads(f.read())
        pc_proj4 = json_f['summary']['srs']['proj4']

    if pc_proj4 is None:
        raise RuntimeError("Could not determine point cloud proj4 declaration")

    bounds_gpkg_path = os.path.join(tree.georeferencingDIR, 'bounds.gpkg')
    # Convert bounds to GPKG
    kwargs = {'bin':tree.ogr2ogr, 'input': bounds_geojson_path, 'output': bounds_gpkg_path, 'proj4': pc_proj4}
    cmd = '{bin} -overwrite -f GPKG -a_srs "{proj4}" {output} {input} > /dev/null 2>&1'.format(**kwargs)
    run(cmd, "Convert bounds to GPKG.")

    return bounds_gpkg_path
