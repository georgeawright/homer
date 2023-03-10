import os
import time

from linguoplotter import Linguoplotter
from linguoplotter.loggers import ActivityLogger, ErrorLogger, StructureLogger

DELETE_STRUCTURE_LOGS = True

pwd = os.getcwd()

program_files = [
    "narration-1.lisp",
    "narration-2.lisp",
    "narration-3.lisp",
    "narration-4.lisp",
    "narration-5.lisp",
    "narration-6.lisp",
]
for program_file in program_files:
    results = []
    random_seeds = range(50)

    for i in random_seeds:
        time_string = str(time.time())
        logs_dir_path = f"{pwd}/logs/{time_string}"
        os.mkdir(logs_dir_path)
        with open(f"{logs_dir_path}/details.txt", "w") as f:
            f.write(f"Program: {program_file}\nRandom seed: {i}\n")
        structure_logs_dir_path = f"{logs_dir_path}/structures"
        os.mkdir(structure_logs_dir_path)

        log_file_name = f"{logs_dir_path}/activity"
        satisfaction_stream = open(f"{logs_dir_path}/satisfaction.csv", "w")
        coderack_population_stream = open(
            f"{logs_dir_path}/coderack_population.csv", "w"
        )
        view_count_stream = open(f"{logs_dir_path}/view_count.csv", "w")
        codelet_spawned_stream = open(f"{logs_dir_path}/codelets_spawned", "w")
        codelet_run_stream = open(f"{logs_dir_path}/codelets_run", "w")
        error_file_name = f"{logs_dir_path}/errors.log"
        error_stream = open(error_file_name, "w")
        loggers = {
            "activity": ActivityLogger(
                log_file_name,
                satisfaction_stream,
                coderack_population_stream,
                view_count_stream,
                codelet_spawned_stream,
                codelet_run_stream,
            ),
            "structure": StructureLogger(f"{structure_logs_dir_path}"),
            "error": ErrorLogger(error_stream),
        }
        narrator = Linguoplotter.setup(loggers, random_seed=i)
        narrator.interpreter.interpret_file("builtin.lisp")

        os.chdir("example-programs/weather")
        narrator.interpreter.interpret_file(program_file)
        os.chdir("../..")
        result = narrator.run()
        results.append(result)
        with open(f"{logs_dir_path}/details.txt", "a") as f:
            text = result["result"]
            satisfaction = result["satisfaction"]
            codelets_run = result["codelets_run"]
            f.write(
                f"Result: {text}\nSatisfaction: {satisfaction}\nCodelets run: {codelets_run}"
            )
        if DELETE_STRUCTURE_LOGS:
            for structure_dir in os.listdir(f"{logs_dir_path}/structures/structures/"):
                for log_file in os.listdir(
                    f"{logs_dir_path}/structures/structures/{structure_dir}"
                ):
                    os.remove(
                        f"{logs_dir_path}/structures/structures/{structure_dir}/{log_file}"
                    )
    print(results)
