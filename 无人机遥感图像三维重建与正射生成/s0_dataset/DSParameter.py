import multiprocessing


class DataSetParameter(object):
    """
    Config DataSet Parameters.
    """
    def __init__(self):
        self.verbose = False
        self.debug = False
        """Print additional messages to the console."""
        self.max_concurrency = multiprocessing.cpu_count()
        """
           The maximum number of processes to use in various processes. 
           Peak memory requirement is ~1GB per thread and 2 megapixel image resolution.
        """
        ##############################s1: reconstruction########################
        self.feature_process_size = 2000
        """sfm feature process size."""
        self.depthmap_resolution = 1000
        """Resolution of the depth maps."""
        self.processes = max(1, self.max_concurrency - 1)
        """max processes using."""
        self.gps_accuracy = 10
        """
            Set a value in meters for the GPS Dilution of Precision (DOP) information for all images.
            If your images are tagged with high precision GPS information (RTK), this value will be automatically set accordingly.
            You can use this option to manually set it in case the reconstruction fails.
            Lowering this option can sometimes help control bowling-effects over large areas.
        """

        ##############################s2: dense#################################
        self.vis_track = False
        self.vis_feature = False
        self.vis_matche = False
        self.exp_ply = False
        self.exp_dsm = False
        self.exp_ortho = True
        self.plot_den = False


        ##############################s3: filter################################
        self.pc_filter = 2.5
        """
            Filters the point cloud by removing points that deviate more than N standard deviations from the local mean.
            Set to 0 to disable filtering.
        """
        self.pc_sample = 0
        """
            Filters the point cloud by keeping only a single point around a radius N (in meters).
            This can be useful to limit the output resolution of the point cloud and remove duplicate points.
            Set to 0 to disable sampling.
        """

        ##############################s4: georeferencing#########################
        self.crop = 3
        """
            Automatically crop image outputs by creating a smooth buffer around the dataset boundaries, shrinked by N meters.
            Use 0 to disable cropping.
        """
        ##############################s5: dsm#####################################
        self.dtm = False
        """
            Use this tag to build a DTM (Digital Terrain Model, ground only) using a simple morphological filter.
            Check the --dem* and --smrf* parameters for finer tuning.
        """
        self.dsm = True
        """
            Use this tag to build a DSM (Digital Surface Model, ground + objects) using a progressive morphological filter.
            Check the --dem* parameters for finer tuning.
        """
        self.dem_gapfill_steps = 3
        """
            Number of steps used to fill areas with gaps. Set to 0 to disable gap filling.
            Starting with a radius equal to the output resolution, N different DEMs are generated with 
                progressively bigger radius using the inverse distance weighted (IDW) algorithm and merged together.
            Remaining gaps are then merged using nearest neighbor interpolation.
        """
        self.dem_resolution = 2
        """
            DSM/DTM resolution in cm / pixel. Note that this value is capped by a ground sampling distance (GSD) estimate.
            To remove the cap, check --ignore-gsd also.
        """
        self.dem_decimation = 1
        """
            Decimate the points before generating the DEM. 1 is no decimation (full quality). 100 decimates ~99%% of the points.
            Useful for speeding up generation of DEM results in very large datasets.
        """
        # Be careful, scalar = 1.5, slope = 0.08, threshold = 0.25, window = 15
        self.smrf_scalar = 1.25
        """Simple Morphological Filter elevation scalar parameter."""
        self.smrf_slope = 0.15
        """Simple Morphological Filter slope parameter (rise over run)."""
        self.smrf_threshold = 0.5
        """Simple Morphological Filter elevation threshold parameter (meters)."""
        self.smrf_window = 18.0
        """Simple Morphological Filter window radius parameter (meters)."""
        self.pc_classify = True
        """
            Classify the point cloud outputs using a Simple Morphological Filter.
            You can control the behavior of this option by tweaking the --dem-* parameters.
        """
        self.pc_rectify = True
        """
            Perform ground rectification on the point cloud.
            This means that wrongly classified ground points will be re-classified and gaps will be filled. Useful for generating DTMs.
        """
        if self.pc_rectify and not self.pc_classify:
            self.pc_classify = True

        if self.dtm and not self.pc_classify:
            self.pc_classify = True

        ##############################s6: mesh#####################################
        self.mesh3d = True
        """
            Use a full 3D mesh to compute the orthophoto instead of a 2.5D mesh.
            This option is a bit faster and provides similar results in planar areas.
        """
        self.mesh25d = True
        """Generation of a 2.5D model. This can save time if you only need 2D results such as orthophotos and DEMs."""
        self.mesh_size = 200000
        """The maximum vertex count of the output mesh."""
        self.mesh_octree_depth = 11
        """Octree depth used in the mesh reconstruction, increase to get more vertices, recommended values are 8-12."""
        if not self.mesh3d and not self.mesh25d:
            self.mesh3d = True
        """Must create one at least."""

        ##############################s7: text#####################################
        self.texturing_data_term = 'area'
        """
            choices=['gmi', 'area']
            When texturing the 3D mesh, for each triangle,
                choose to prioritize images with sharp features (gmi) or those that cover the largest area (area).
        """
        self.texturing_outlier_removal_type = 'gauss_clamping'
        """choices=['none', 'gauss_clamping', 'gauss_damping'], Type of photometric outlier removal method."""
        self.texturing_tone_mapping = 'gamma'
        """choices=['none', 'gamma'], Turn on gamma tone mapping or none for no tone mapping."""

        ##############################s8: orhto####################################
        self.ortho_resol = 30
        """pixels per meter."""
        self.orthophoto_compression = 'DEFLATE'
        """choices=['JPEG', 'LZW', 'PACKBITS', 'DEFLATE', 'LZMA', 'NONE'], Set the compression to use for orthophotos."""


args = DataSetParameter()
