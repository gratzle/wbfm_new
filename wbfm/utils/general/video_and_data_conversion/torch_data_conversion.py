import os

import numpy as np
from tqdm.auto import tqdm

from wbfm.utils.projects.finished_project_data import ProjectData
from wbfm.utils.projects.project_config_classes import ModularProjectConfig


def convert_all_matches_to_cpu_from_config(project_config: ModularProjectConfig):
    """Loads raw_matches and convert the features to numpy arrays that live on the cpu"""

    project_data = ProjectData.load_final_project_data_from_config(project_config, to_load_frames=True)
    matches = project_data.raw_matches

    for match in tqdm(matches.values()):
        feature_matches = match.feature_matches
        feature_matches = [[m[0], int(m[1]), m[2].cpu().numpy()] for m in feature_matches]
        match.feature_matches = np.array(feature_matches)

    training_cfg = project_config.get_training_config()
    fname = os.path.join('2-training_data', 'raw', 'match_dat.pickle')
    training_cfg.pickle_data_in_local_project(matches, fname)
