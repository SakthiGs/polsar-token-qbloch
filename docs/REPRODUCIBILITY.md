# EXP37 results provenance

Original source: Google Drive research project `FPSD_QPOLVERIFIER_RUNS`, experiment folders labelled `exp37_fusion_fidelity_...`, June 2026.

The committed CSV files were read from the June 19 experiment's `logs` folder and preserve the source values:

- `grid_per_seed_metrics.csv`: eight model variants × ten seeds, with AP, AUC, F1 and other metrics.
- `tableA_verifier_comparison.csv`: aggregated model comparison and total parameter counts.
- `tableB_auc_significance.csv`: paired AUC comparisons and test summaries.
- `tableC_bootstrap_data_level_ci.csv`: bootstrap metric CIs; `b_boot` 1000.
- `tableC2_paired_bootstrap_delta.csv`: candidate-level paired bootstrap differences, `b_boot` 2000.
- `entanglement_ablation_comparisons.csv`: entanglement vs no-entanglement comparisons.

**Important:** AUC improvements across seeds and candidate-level bootstrap results are different inferential analyses; report labels and sample units accurately.

To make reproduction complete, commit the vetted notebooks plus an exact environment and input-provenance manifest, then run the end-to-end pipeline under controlled conditions. The current archive is an evidence snapshot, not a runnable deployment.
