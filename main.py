import csv
import json
import os
import time

from linguoplotter import Linguoplotter
from linguoplotter.loggers import (
    ActivityLogger,
    ErrorLogger,
    MockLogger,
    StructureLogger,
)

DEVELOPMENT = True

pwd = os.getcwd()

program_files = [
    "narration-1.lisp",
    # "narration-2.lisp",
    # "narration-3.lisp",
    # "narration-4.lisp",
    # "narration-5.lisp",
    "narration-6.lisp",
]
start_time = time.time()
for program_file in program_files:
    results = []
    random_seeds = range(5)

    for i in random_seeds:
        time_string = str(time.time())
        logs_dir_path = f"{pwd}/logs/{time_string}"
        os.mkdir(logs_dir_path)
        with open(f"{logs_dir_path}/details.txt", "w") as f:
            run_details = {"Program": program_file, "random_seed": i}
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
        loggers = {
            "activity": activity_logger,
            "structure": structure_logger,
            "error": ErrorLogger(error_stream),
        }
        narrator = Linguoplotter.setup(loggers, random_seed=i)
        narrator.interpreter.interpret_file("builtin.lisp")
        os.chdir("example-programs/weather")
        narrator.interpreter.interpret_file(program_file)
        os.chdir("../..")
        result = narrator.run()
        results.append(result)
        with open(f"{logs_dir_path}/details.txt", "w") as f:
            run_details = dict(run_details, **result)
            f.write(json.dumps(run_details))
        with open(f"{logs_dir_path}/codelet_times.csv", "w", newline="") as csvfile:
            fieldnames = list(narrator.coderack.codelet_times[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for codelet_time in narrator.coderack.codelet_times:
                writer.writerow(codelet_time)
    end_time = time.time()
    print(results)
    run_length = end_time - start_time
    print(run_length)
