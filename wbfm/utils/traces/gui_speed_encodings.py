from functools import partial
from typing import Dict

import pandas as pd
from sklearn.model_selection import KFold

from wbfm.gui.utils.utils_dash import save_folder_for_two_dataframe_dashboard
from wbfm.utils.projects.finished_project_data import ProjectData
from wbfm.utils.visualization.behavior_comparison_plots import NeuronToUnivariateEncoding
from wbfm.utils.visualization.multiproject_wrappers import MultiProjectBehaviorPlotterWithBehavior


def build_all_gui_dfs_speed_encoding(all_projects_gcamp: Dict[str, ProjectData],
                                     all_projects_gfp: Dict[str, ProjectData],
                                     output_folder: str = None,
                                     trace_options=None,
                                     encoder_opt=None,
                                     verbose=0,
                                     **kwargs):

    # Use same trace options for all plots
    if trace_options is None:
        trace_options = {}
    if encoder_opt is None:
        encoder_opt = {}
    opt = dict(interpolate_nan=False,
               filter_mode='rolling_mean',
               min_nonnan=0.9,
               nan_tracking_failure_points=True,
               nan_using_ppca_manifold=False,  # This takes a long time!
               channel_mode='dr_over_r_50')
    opt.update(trace_options)

    default_encoder_opt = dict(df_name=opt['channel_mode'], y_train='signed_middle_body_speed')
    default_encoder_opt.update(encoder_opt)
    encoder_opt = default_encoder_opt
    constructor_kwargs = dict(df_kwargs=opt, dataframes_to_load=[opt['channel_mode']])

    cv_factory = partial(KFold, n_splits=3)

    # Get summary dataframes
    df_opt = dict(encoder_opt=encoder_opt, constructor_kwargs=constructor_kwargs, cv_factory=cv_factory)
    df_opt.update(kwargs)
    df_summary_gcamp, all_dfs_prediction_gcamp, df_raw_gcamp = calculate_all_dfs_using_encoder(all_projects_gcamp,
                                                                                               genotype='gcamp',
                                                                                               **df_opt)
    df_summary_gfp, all_dfs_prediction_gfp, df_raw_gfp = calculate_all_dfs_using_encoder(all_projects_gfp, genotype='gfp',
                                                                                         **df_opt)

    # Concatenate all dictionaries into single dataframes
    # Outer keys are 'multi', 'single', and 'leifer'
    df_summary = pd.concat([df_summary_gcamp, df_summary_gfp])
    df_pred_concat = {}
    for key in all_dfs_prediction_gcamp.keys():
        # Concatenate nested dataframes; inner keys refer to each dataset
        df_prediction_gcamp = all_dfs_prediction_gcamp[key]
        df_prediction_gcamp = pd.concat(df_prediction_gcamp, axis=1)
        df_prediction_gcamp.columns = df_prediction_gcamp.columns.droplevel(1)

        df_prediction_gfp = all_dfs_prediction_gfp[key]
        df_prediction_gfp = pd.concat(df_prediction_gfp, axis=1)
        df_prediction_gfp.columns = df_prediction_gfp.columns.droplevel(1)

        df_pred = pd.concat([df_prediction_gcamp, df_prediction_gfp], axis=1)
        df_pred_concat[key] = df_pred
    df_raw = pd.concat([df_raw_gcamp, df_raw_gfp], axis=1)
    raw_dfs = {'speed': df_raw}
    raw_dfs.update(df_pred_concat)
    if verbose >= 1:
        print("Done calculating all dataframes")
        print("Saving the following raw dataframes:")
        print(raw_dfs.keys())
        if verbose >= 2:
            print(raw_dfs)

    # Save
    save_folder_for_two_dataframe_dashboard(output_folder, df_summary, raw_dfs)

    return df_summary, raw_dfs


def calculate_all_dfs_using_encoder(all_projects, genotype='gcamp', only_model_single_state=None,
                                    encoder_opt=None, constructor_kwargs=None, cv_factory=None):
    multi_encoder = MultiProjectBehaviorPlotterWithBehavior(all_projects=all_projects, constructor_kwargs=constructor_kwargs,
                                                            class_constructor=NeuronToUnivariateEncoding)
    multi_encoder.set_for_all_classes({'cv_factory': cv_factory})

    _encoder_opt = encoder_opt.copy()
    _encoder_opt['only_model_single_state'] = only_model_single_state
    df_summary = multi_encoder.calc_dataset_summary_df(**_encoder_opt)
    _encoder_opt['use_multineuron'] = True
    df_prediction_multi = multi_encoder.calc_prediction_or_raw_df(**_encoder_opt, prediction_not_raw=True)
    try:
        _encoder_opt['use_multineuron'] = False
        df_prediction_single = multi_encoder.calc_prediction_or_raw_df(**_encoder_opt, prediction_not_raw=True)
    except NotImplementedError:
        df_prediction_single = None
    _encoder_opt['use_leifer_method'] = True
    df_prediction_leifer = multi_encoder.calc_prediction_or_raw_df(**_encoder_opt, prediction_not_raw=True)
    df_raw = multi_encoder.calc_prediction_or_raw_df(**_encoder_opt, prediction_not_raw=False)

    # Concatenate all dictionaries into single dataframes
    df_summary = pd.concat(df_summary)
    df_summary['genotype'] = genotype
    df_summary.index = df_summary.index.droplevel(1)

    all_dfs_prediction = {'multi': df_prediction_multi, 'single': df_prediction_single, 'leifer': df_prediction_leifer}
    # Remove any None values
    all_dfs_prediction = {k: v for k, v in all_dfs_prediction.items() if v is not None}
    df_raw = pd.concat(df_raw, axis=1)
    df_raw.columns = df_raw.columns.droplevel(1)

    return df_summary, all_dfs_prediction, df_raw
