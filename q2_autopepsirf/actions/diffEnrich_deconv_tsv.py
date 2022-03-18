from math import inf
import pandas as pd
import qiime2
from collections import defaultdict
import csv, os

from q2_pepsirf.format_types import (
    PepsirfInfoSumOfProbesFmt, PepsirfInfoSNPNFormat,
    PepsirfContingencyTSVFormat, ZscoreNanFormat,
    EnrichedPeptideDirFmt, PeptideBinFormat,
    EnrichThreshFileFormat, PeptideIDListFmt,
    PepsirfLinkTSVFormat, PepsirfDMPFormat
    )

def diffEnrich_deconv_tsv(
    ctx,
    raw_data_tsv,
    bins_tsv,
    enriched: PeptideIDListFmt,
    threshold: int,
    linked: PepsirfLinkTSVFormat,
    infer_pairs_source=True,
    flexible_reps_source=False,
    s_enrich_source=False,
    user_defined_source = None,
    negative_control_tsv=None,
    negative_id=None,
    negative_names=None,
    thresh_file_tsv = None,
    exact_z_thresh = None,
    exact_cs_thresh = "20",
    exact_zenrich_thresh = None,
    pepsirf_tsv_dir = "./",
    tsv_base_str = None,
    step_z_thresh = 5,
    upper_z_thresh = 30,
    lower_z_thresh = 5,
    raw_constraint = 300000,
    hdi = 0.95,
    scoring_strategy: str = "summation",
    score_filtering: bool = False,
    score_tie_threshold: float = 0.0,
    score_overlap_threshold: float = 0.0,
    id_name_map: PepsirfDMPFormat = None,
    single_threaded: bool = False,
    outfile: str = "./deconv.out",
    pepsirf_binary = "pepsirf"
    ):

    diffEnrich_deconv = ctx.get_action('autopepsirf', 'diffEnrich_deconv')

    raw_data = ctx.make_artifact(
        type = 'FeatureTable[RawCounts]',
        view = raw_data_tsv,
        view_type=PepsirfContingencyTSVFormat
    )

    bins = ctx.make_artifact(
        type = 'PeptideBins',
        view = bins_tsv,
        view_type=PeptideBinFormat
    )

    if negative_control_tsv:
        negative_control = ctx.make_artifact(
            type='FeatureTable[Normed]',
            view=negative_control_tsv,
            view_type=PepsirfContingencyTSVFormat
        )
    # otherwise set negative control to none
    else:
        negative_control = None
    
    #if thresh-file provided import into artifact
    if thresh_file_tsv:
        thresh_file = ctx.make_artifact(
            type='EnrichThresh',
            view=thresh_file_tsv,
            view_type=EnrichThreshFileFormat
        )
    #otherwise set thresh-file to none
    else:
        thresh_file = None

    (col_sum, diff, diff_ratio, zscore_out, nan_out, sample_names,
        read_counts, rc_boxplot_out, enrich_dir, enrichedCountsBoxplot, 
        zscore_scatter, colsum_scatter, zenrich_out, dir_out, score_per_round, 
        map_dir, ) = diffEnrich_deconv(
        raw_data = raw_data,
        bins = bins,
        enriched = enriched,
        threshold = threshold,
        linked = linked,
        infer_pairs_source = infer_pairs_source,
        flexible_reps_source = flexible_reps_source,
        s_enrich_source = s_enrich_source,
        user_defined_source = user_defined_source,
        negative_control = negative_control,
        negative_id = negative_id,
        negative_names = negative_names,
        thresh_file = thresh_file,
        exact_z_thresh = exact_z_thresh,
        exact_cs_thresh = exact_cs_thresh,
        exact_zenrich_thresh = exact_zenrich_thresh,
        pepsirf_tsv_dir = pepsirf_tsv_dir,
        tsv_base_str = tsv_base_str,
        step_z_thresh = step_z_thresh,
        upper_z_thresh = upper_z_thresh,
        lower_z_thresh = lower_z_thresh,
        raw_constraint = raw_constraint,
        hdi = hdi,
        scoring_strategy = scoring_strategy,
        score_filtering = score_filtering,
        score_tie_threshold = score_tie_threshold,
        score_overlap_threshold = score_overlap_threshold,
        id_name_map = id_name_map,
        single_threaded = single_threaded,
        outfile = outfile,
        pepsirf_binary = pepsirf_binary 
    )
    #plot? I just run through deconv that's all I really know

    return ( col_sum, diff, diff_ratio, zscore_out, nan_out, sample_names,
        read_counts, rc_boxplot_out, enrich_dir, enrichedCountsBoxplot, 
        zscore_scatter, colsum_scatter, zenrich_out, dir_out, score_per_round, 
        map_dir, )
    


