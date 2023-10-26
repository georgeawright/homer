import json
import os
import statistics

LOGS_DIRECTORY = "logs_100_seeds"
program_results = {}

log_directories = os.listdir(LOGS_DIRECTORY)
for log_directory in log_directories:
    try:
        with open(f"{LOGS_DIRECTORY}/{log_directory}/details.txt") as f:
            details = json.load(f)
    except NotADirectoryError:
        continue
    program = details["Program"]
    text = details["result"]
    satisfaction = details["satisfaction"]
    codelets = details["codelets_run"]
    if program not in program_results:
        program_results[program] = {
            "texts": set(),
            "satisfactions": [],
            "non_time_out_satisfactions": [],
            "run_lengths": [],
            "time_out_count": 0,
        }
    program_results[program]["satisfactions"].append(satisfaction)
    program_results[program]["run_lengths"].append(codelets)
    if text is None:
        program_results[program]["time_out_count"] += 1
    else:
        program_results[program]["texts"].add(text)
        program_results[program]["non_time_out_satisfactions"].append(satisfaction)

print(
    "program\tmean_satisfaction\tmean_non_time_out_satisfaction\tmean_run_length\ttime_out_count\tdistinct_texts"
)
for program, results in program_results.items():
    mean_satisfaction = statistics.fmean(results["satisfactions"])
    mean_non_time_out_satisfaction = statistics.fmean(
        results["non_time_out_satisfactions"]
    )
    mean_run_length = statistics.fmean(results["run_lengths"])
    time_out_count = results["time_out_count"]
    distinct_texts = len(results["texts"])

    print(
        f"{program}\t{mean_satisfaction}\t{mean_non_time_out_satisfaction}\t{mean_run_length}\t{time_out_count}\t{distinct_texts}"
    )
