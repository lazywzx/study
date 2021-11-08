import yaml
from ..s0_dataset import DSParameter, log
from ..s0_dataset.runCMD import run
from ..s1_sfm.config_yaml import osfmConfig

args = DSParameter.args


def default_config(file, config):
    """
    write default config to config.yaml

    :param config:
    :return:
    """
    config['feature_process_size'] = args.feature_process_size
    config['depthmap_resolution'] = args.depthmap_resolution
    config['processes'] = args.processes
    with open(file, "w", encoding="utf-8") as cf:
        yaml.dump(config, cf)
    return config


def modi_config(file, config_data, modi_data):
    """
    modify current config

    :param config_data:
    :param modi_data:
    :return:
    """
    for key, val in modi_data.items():
        config_data[key] = val
    with open(file, "w", encoding="utf-8") as cf:
        yaml.dump(config_data, cf)
    return config_data


def osfm_pipeline(gpsinfo, file, bin, dataset_path):
    """
    run the sfm pipeline

    :param file:
    :param bin:
    :param dataset_path:
    """
    log.logINFO("Write default config.")
    current_config = default_config(file, osfmConfig)   # setup default config
    # run tasks
    for task in ['extract_metadata', 'detect_features', 'match_features', 'create_tracks', 'reconstruct',
                 'export_geocoords', 'export_ply']:
        if task == 'detect_features':
            log.logINFO("Change config.processes to 1.")
            current_config = modi_config(file, current_config, {'processes': 1})
        elif current_config['processes'] != args.processes:
            log.logINFO("Change config.processes to default.")
            current_config = modi_config(file, current_config, {'processes': args.processes})
        # georeferencing the reconstruction
        if task == 'export_geocoords':
            if gpsinfo['is_georeferenced']:
                task += ' --reconstruction --proj \'%s\'' % gpsinfo['proj4']
            else:
                continue
        # run command
        cmd = " ".join([bin, task, dataset_path, ' > /dev/null 2>&1'])
        run(cmd, "Run " + task + "...")
