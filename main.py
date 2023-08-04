import csv
import json
import os
import statistics
import time

from rouge_score.rouge_scorer import RougeScorer
import zss

from linguoplotter import Linguoplotter
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.loggers import (
    ActivityLogger,
    ErrorLogger,
    MockLogger,
    StructureLogger,
    TextLogger,
)

DEVELOPMENT = False
LOG_INTERMMEDIATE_TEXTS = True

pwd = os.getcwd()

hyper_parameters_files = [
    # "hyper_parameters_files/h01.json",
    # "hyper_parameters_files/h02.json",
    # "hyper_parameters_files/h03.json",
    # "hyper_parameters_files/h04.json",
    # "hyper_parameters_files/h05.json",
    # "hyper_parameters_files/h06.json",
    # "hyper_parameters_files/h07.json",
    # "hyper_parameters_files/h08.json",
    # "hyper_parameters_files/h09.json",
    # "hyper_parameters_files/h10.json",
    # "hyper_parameters_files/h11.json",
    # "hyper_parameters_files/h12.json",
    # "hyper_parameters_files/h13.json",
    # "hyper_parameters_files/h14.json",
    # "hyper_parameters_files/h15.json",
    # "hyper_parameters_files/h16.json",
    "hyper_parameters_files/h17.json",
    "hyper_parameters_files/h18.json",
    "hyper_parameters_files/h19.json",
    "hyper_parameters_files/h20.json",
    "hyper_parameters_files/h21.json",
    "hyper_parameters_files/h22.json",
    "hyper_parameters_files/h23.json",
    "hyper_parameters_files/h24.json",
    "hyper_parameters_files/h25.json",
    "hyper_parameters_files/h26.json",
    "hyper_parameters_files/h27.json",
    "hyper_parameters_files/h28.json",
    "hyper_parameters_files/h29.json",
    "hyper_parameters_files/h30.json",
    "hyper_parameters_files/h31.json",
    "hyper_parameters_files/h32.json",
    "hyper_parameters_files/h33.json",
    "hyper_parameters_files/h34.json",
    "hyper_parameters_files/h35.json",
    "hyper_parameters_files/h36.json",
    "hyper_parameters_files/h37.json",
    "hyper_parameters_files/h38.json",
    "hyper_parameters_files/h39.json",
    "hyper_parameters_files/h40.json",
]
program_files = [
    "narration-1.lisp",
    "narration-2.lisp",
    "narration-3.lisp",
    "narration-4.lisp",
    "narration-5.lisp",
    "narration-6.lisp",
]
random_seeds = range(5)

start_time = time.time()
results = []

for hyper_parameters_file in hyper_parameters_files:
    print(hyper_parameters_file)
    for i in random_seeds:
        for program_file in program_files:
            iteration_start_time = time.time()
            time_string = str(time.time())
            logs_dir_path = f"{pwd}/logs/{time_string}"
            os.mkdir(logs_dir_path)
            with open(f"{logs_dir_path}/details.txt", "w") as f:
                run_details = {
                    "Program": program_file,
                    "random_seed": i,
                    "hyper_parameters": hyper_parameters_file,
                }
                f.write(json.dumps(run_details))
            error_file_name = f"{logs_dir_path}/errors.log"
            error_stream = open(error_file_name, "w")
            if DEVELOPMENT:
                structure_logs_dir_path = f"{logs_dir_path}/structures"
                os.mkdir(structure_logs_dir_path)
                codelets_directory = f"{logs_dir_path}/codelets"
                os.mkdir(codelets_directory)
                os.mkdir(f"{codelets_directory}/ids")
                os.mkdir(f"{codelets_directory}/times")
                satisfaction_stream = open(f"{logs_dir_path}/satisfaction.csv", "w")
                determinism_stream = open(f"{logs_dir_path}/determinism.csv", "w")
                coderack_population_stream = open(
                    f"{logs_dir_path}/coderack_population.csv", "w"
                )
                view_count_stream = open(f"{logs_dir_path}/view_count.csv", "w")
                codelet_spawned_stream = open(f"{logs_dir_path}/codelets_spawned", "w")
                codelet_run_stream = open(f"{logs_dir_path}/codelets_run", "w")
                activity_logger = ActivityLogger(
                    codelets_directory,
                    satisfaction_stream=satisfaction_stream,
                    determinism_stream=determinism_stream,
                    coderack_population_stream=coderack_population_stream,
                    view_count_stream=view_count_stream,
                    codelet_spawned_stream=codelet_spawned_stream,
                    codelet_run_stream=codelet_run_stream,
                )
                structure_logger = StructureLogger(f"{structure_logs_dir_path}")
            else:
                activity_logger = MockLogger()
                structure_logger = MockLogger()
            if LOG_INTERMMEDIATE_TEXTS:
                text_logger = TextLogger(
                    hyper_parameters=hyper_parameters_file,
                    seed=i,
                    program=program_file,
                    stream=open(f"{pwd}/logs/texts.csv", "a"),
                )
            else:
                text_logger = MockLogger()
            loggers = {
                "activity": activity_logger,
                "structure": structure_logger,
                "text": text_logger,
                "error": ErrorLogger(error_stream),
            }
            with open(hyper_parameters_file, "r") as f, open(
                f"{logs_dir_path}/hyper_parameters.json", "w"
            ) as f2:
                hyper_parameters_json = f.read()
                f2.write(hyper_parameters_json)
                hyper_parameters = HyperParameters.from_dict(
                    json.loads(hyper_parameters_json)
                )
            narrator = Linguoplotter.setup(hyper_parameters, loggers, random_seed=i)
            narrator.interpreter.interpret_file("builtin.lisp")
            os.chdir("example-programs/weather")
            narrator.interpreter.interpret_file(program_file)
            os.chdir("../..")
            result = narrator.run()
            result["Program"] = program_file
            iteration_end_time = time.time()
            results.append(result)
            with open(f"{logs_dir_path}/details.txt", "w") as f:
                run_details = dict(run_details, **result)
                run_details["time_in_seconds"] = (
                    iteration_end_time - iteration_start_time
                )
                f.write(json.dumps(run_details))
            with open(f"{logs_dir_path}/codelet_times.csv", "w", newline="") as csvfile:
                fieldnames = list(narrator.coderack.codelet_times[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for codelet_time in narrator.coderack.codelet_times:
                    writer.writerow(codelet_time)
            if result["result"] is not None:
                result["tree"] = narrator.bubble_chamber.worldview.view.to_zss_tree()

end_time = time.time()
print(results)
run_length = end_time - start_time
print(run_length)

# calculate string and tree similarity and output to a statistics file
rouge_scorer = RougeScorer(["rougeL"], use_stemmer=True)
results_stats = {program_file: {} for program_file in program_files}
for program_file in program_files:
    program_results = [r for r in results if r["Program"] == program_file]
    texts = [r["result"] for r in program_results if r["result"] is not None]
    trees = [r["tree"] for r in program_results if r["result"] is not None]
    results_stats[program_file]["mean_satisfaction"] = statistics.fmean(
        [r["satisfaction"] for r in program_results]
    )
    results_stats[program_file]["median_satisfaction"] = statistics.median(
        [r["satisfaction"] for r in program_results]
    )
    try:
        rouge_scores = [
            rouge_scorer.score(texts[i], texts[j])["rougeL"].fmeasure
            for i in range(len(texts))
            for j in range(len(texts))
            if j > i
        ]
        results_stats[program_file]["mean_pairwise_rouge"] = statistics.fmean(
            rouge_scores,
        )
        results_stats[program_file]["median_pairwise_rouge"] = statistics.median(
            rouge_scores,
        )
    except statistics.StatisticsError:
        results_stats[program_file]["mean_pairwise_rouge"] = None
        results_stats[program_file]["median_pairwise_rouge"] = None
    try:
        zss_scores = [
            zss.simple_distance(trees[i], trees[j])
            for i in range(len(trees))
            for j in range(len(trees))
            if j > i
        ]
        results_stats[program_file]["mean_pairwise_zss"] = statistics.fmean(
            zss_scores,
        )
        results_stats[program_file]["median_pairwise_zss"] = statistics.median(
            zss_scores,
        )
    except statistics.StatisticsError:
        results_stats[program_file]["mean_pairwise_zss"] = None
        results_stats[program_file]["median_pairwise_zss"] = None
with open(f"{pwd}/logs/stats.txt", "w") as f:
    f.write(json.dumps(results_stats))
