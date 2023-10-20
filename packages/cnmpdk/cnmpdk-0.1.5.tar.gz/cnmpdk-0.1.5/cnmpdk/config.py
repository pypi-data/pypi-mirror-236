__all__ = ["PATH"]

import pathlib

home = pathlib.Path.home()
cwd = pathlib.Path.cwd()

cwd_config = cwd / "config.yml" # TODO: Delete if not needed

home_config = home / ".config"  # TODO: Delete if not needed
config_dir = home / ".config"   # TODO: Delete if not needed
config_dir.mkdir(exist_ok=True)
module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent

library_version = "6.1.1"

class Path:
    module = module_path
    repo = repo_path

    tech_dir = module_path / "klayout"
    lyp = module_path / tech_dir / "cnm_klayout_layers.lyp"
    lyt = module_path / tech_dir / "cnm_technology.lyt"

    lyp_2_yaml = module_path / "cnm_layer_views.yaml"

    ip_blocks_dir = module_path / "ip_blocks"
    examples_dir = module_path / "examples"
    components_dir = module_path / "components"
    library_path = ip_blocks_dir / "CNM_library_v6.1.1_BB_MPW_06_07-07-2022_CNMPDK.gds"

    

PATH = Path()

if __name__ == "__main__":
    print(PATH)
