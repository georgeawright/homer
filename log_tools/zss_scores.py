import json
import statistics

with open("logs_refinement_zss/stats.txt", "r") as f:
    stats = json.load(f)

for hyperparameters, results in stats.items():
    mean_satisfaction = statistics.fmean(
        [
            program_stats["mean_satisfaction"]
            for program, program_stats in results.items()
            if program_stats["mean_satisfaction"] is not None
        ]
    )
    median_satisfaction = statistics.median(
        [
            program_stats["median_satisfaction"]
            for program, program_stats in results.items()
            if program_stats["median_satisfaction"] is not None
        ]
    )
    mean_rouge = statistics.fmean(
        [
            program_stats["mean_pairwise_rouge"]
            for program, program_stats in results.items()
            if program_stats["mean_pairwise_rouge"] is not None
        ]
    )
    median_rouge = statistics.median(
        [
            program_stats["median_pairwise_rouge"]
            for program, program_stats in results.items()
            if program_stats["median_pairwise_rouge"] is not None
        ]
    )
    mean_zss = statistics.fmean(
        [
            program_stats["mean_pairwise_zss"]
            for program, program_stats in results.items()
            if program_stats["mean_pairwise_zss"] is not None
        ]
    )
    median_zss = statistics.median(
        [
            program_stats["median_pairwise_zss"]
            for program, program_stats in results.items()
            if program_stats["median_pairwise_zss"] is not None
        ]
    )
    print(
        f"{hyperparameters}\t{mean_satisfaction}\t{median_satisfaction}\t"
        + f"{mean_rouge}\t{median_rouge}\t{mean_zss}\t{median_zss}"
    )
