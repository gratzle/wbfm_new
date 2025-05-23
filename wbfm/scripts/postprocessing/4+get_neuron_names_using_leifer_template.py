"""
The top level function for producing dlc tracks in 3d
"""

# Experiment tracking
import sacred
from wbfm.utils.nn_utils.fdnc_predict import get_putative_names_from_config
from sacred import Experiment

# main function
from sacred.observers import TinyDbObserver
from wbfm.utils.external.monkeypatch_json import using_monkeypatch
from wbfm.utils.projects.project_config_classes import ModularProjectConfig

# Initialize sacred experiment
ex = Experiment(save_git_info=False)
ex.add_config(project_path=None, DEBUG=False)


@ex.config
def cfg(project_path, DEBUG):
    # Manually load yaml files
    cfg = ModularProjectConfig(project_path)
    project_dir = cfg.project_dir

    if not DEBUG:
        using_monkeypatch()
        log_dir = cfg.get_log_dir()
        ex.observers.append(TinyDbObserver(log_dir))


@ex.automain
def combine_tracks(_config, _run):
    sacred.commands.print_config(_run)

    project_config = _config['cfg']
    get_putative_names_from_config(project_config)
