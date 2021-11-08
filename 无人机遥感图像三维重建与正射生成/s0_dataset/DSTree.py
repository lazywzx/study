import os

# path/to/your/project
# place images_dir in ./project/images
root_path = "./langley/"
binpath = "./src/bin/"


class DataSetTree(object):
    """
    Config DataSet Tree, bin path, files path.
    """
    def __init__(self, root_path):
        # bin path
        self.bin = os.path.abspath(binpath)
        # PDAL
        self.pdal = os.path.join(self.bin, 'pdal')
        # ogr2ogr
        self.ogr2ogr = os.path.join(self.bin, 'ogr2ogr')
        # GDAL
        self.gdalDIR = os.path.join(self.bin, 'gdal')
        self.gdalbuildvrt = os.path.join(self.gdalDIR, 'gdalbuildvrt')
        self.gdal_translate = os.path.join(self.gdalDIR, 'gdal_translate')
        self.gdal_fillnodata = os.path.join(self.gdalDIR, 'gdal_fillnodata.py')
        self.gdalwarp = os.path.join(self.gdalDIR, 'gdalwarp')
        self.gdal_proximity = os.path.join(self.gdalDIR, 'gdal_proximity.py')
        # OpenSfM
        self.osfmDIR = os.path.join(self.bin, 'osfm/bin')
        self.opensfm = os.path.join(self.osfmDIR, 'opensfm')
        self.plot_matches = os.path.join(self.osfmDIR, 'plot_matches')
        # Poisson Recon
        self.poisson_recon = os.path.join(self.bin, 'PoissonRecon')
        # odm bin
        self.odm_bin = os.path.join(self.bin, 'odm')
        # Clean Mesh
        self.clean_mesh = os.path.join(self.odm_bin, 'odm_cleanmesh')
        # dem2mesh
        self.dem2mesh = os.path.join(self.odm_bin, 'dem2mesh')
        # orthophoto
        self.ortho_bin = os.path.join(self.odm_bin, 'odm_orthophoto')
        # Texturing Recon
        self.texrecon = os.path.join(self.bin, 'texrecon')

        # root path to the project
        self.root_path = os.path.abspath(root_path)
        # input raw images
        self.input_images = os.path.join(self.root_path, 'images')
        # log file
        self.logpath = os.path.join(self.root_path, 'logging.log')
        # result
        self.resultDIR = os.path.join(self.root_path, 'RESULT')

        #####################s1: SfM########################
        self.sfmDIR = os.path.join(self.root_path, 'S1_sfm')
        self.config_yaml = os.path.join(self.sfmDIR, 'config.yaml')
        self.osfm_sparse = os.path.join(self.sfmDIR, 'reconstruction.ply')
        self.osfm_recon = os.path.join(self.resultDIR, 'sfm_recon.ply')
        self.osfm_exif_override = os.path.join(self.sfmDIR, 'exif_overrides.json')
        self.gps_txt = os.path.join(self.sfmDIR, 'gps_info.txt')

        #####################s2: dense######################
        self.denseDIR = os.path.join(self.root_path, 'S2_density')
        self.merged_ply = os.path.join(self.sfmDIR, 'undistorted/depthmaps/merged.ply')
        self.densePC = os.path.join(self.denseDIR, 'dense_pc.ply')
        self.osfm_exif = os.path.join(self.sfmDIR, 'exif')
        self.osfm_flight = os.path.join(self.resultDIR, 'flight_track.jpg') # result
        self.osfm_features = os.path.join(self.sfmDIR, 'features')
        self.osfm_draw_feat = os.path.join(self.resultDIR, 'features')  # result
        self.osfm_plot_tracks = os.path.join(self.sfmDIR, 'plot_tracks')
        self.osfm_plot_matches = os.path.join(self.resultDIR, 'matches')    # result
        self.osfm_nvm = os.path.join(self.sfmDIR, 'undistorted/reconstruction.nvm')

        #####################s3: filter######################
        self.filterpointsDIR = os.path.join(self.root_path, 'S3_filter')
        self.filteredPC = os.path.join(self.filterpointsDIR, 'filteredDensePointCloud.ply')
        self.modify_pc = os.path.join(self.filterpointsDIR, 'modifyPC.ply')

        ####################s4: georeferencing##############
        self.georeferencingDIR = os.path.join(self.root_path, 'S4_georeferencing')
        self.georeferencing_model = os.path.join(self.georeferencingDIR, 'georeferenced_model.laz')
        self.densePC_geo = os.path.join(self.resultDIR, 'densePointCloud.laz')
        self.gpkgfile = os.path.join(self.georeferencingDIR, 'bounds.gpkg')

        ####################s5: dsm#########################
        self.dsmDIR = os.path.join(self.root_path, 'S5_dsm')
        self.dem_model = os.path.join(self.dsmDIR, 'dem_model.laz')
        self.dsm_tif = os.path.join(self.dsmDIR, 'dsm.tif')

        ####################s6: meshing#####################
        self.meshingDIR = os.path.join(self.root_path, 'S6_meshing')
        self.mesh3d = os.path.join(self.meshingDIR, 'mesh3d.ply')
        self.mesh25d = os.path.join(self.meshingDIR, 'mesh25d.ply')

        ####################s7: texturing###################
        self.texturingDIR = os.path.join(self.root_path, 'S7_texturing')
        self.textured3d = os.path.join(self.texturingDIR, 'textured3d')
        self.textured25d = os.path.join(self.texturingDIR, 'textured25d')

        ####################s8: orthophoto##################
        self.orthoDIR = os.path.join(self.root_path, 'S8_orthophoto')
        self.ortho3dDIR = os.path.join(self.orthoDIR, 'ortho3d')
        self.ortho25dDIR = os.path.join(self.orthoDIR, 'ortho25d')
        self.ortho_log = 'orthophoto_log.txt'
        self.orthophoto_render = 'orthophoto_render.tif'
        self.orthophoto_corners = 'orthophoto_corners.txt'
        self.orthophoto_tif = 'orthophoto.tif'

    def path(self, *args):
        return os.path.join(self.root_path, *args)


tree = DataSetTree(root_path)
