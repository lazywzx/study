import os
from s0_dataset import DSParameter, DSTree
from s0_dataset.runCMD import run

args = DSParameter.args
tree = DSTree.tree


def textur_process():
    """
    create textured model from meshes
    """
    if not os.path.exists(tree.texturingDIR):
        os.makedirs(tree.texturingDIR)
    # mvstex definitions
    kwargs = {
        'bin': tree.texrecon,
        'dataTerm': args.texturing_data_term,
        'outlierRemovalType': args.texturing_outlier_removal_type,
        'toneMapping': args.texturing_tone_mapping,
        'nvm_file': tree.osfm_nvm,
        'intermediate': '--no_intermediate_results',
        'threads': 1
    }
    # run texturing model
    if args.mesh3d:
        kwargs.update({'out_dir': tree.textured3d, 'model': tree.mesh3d})

        cmd = ('{bin} {nvm_file} {model} {out_dir} -d {dataTerm} -o {outlierRemovalType} -t {toneMapping} '
               '{intermediate} --num_threads={threads} > /dev/null 2>&1'.format(**kwargs))
        run(cmd, "Texturing 3D mesh model...")
    if args.mesh25d:
        kwargs.update({'out_dir': tree.textured25d, 'model': tree.mesh25d})

        cmd = ('{bin} {nvm_file} {model} {out_dir} -d {dataTerm} -o {outlierRemovalType} -t {toneMapping} '
               '{intermediate} --num_threads={threads} > /dev/null 2>&1'.format(**kwargs))
        run(cmd, "Texturing 2.5D mesh model...")
