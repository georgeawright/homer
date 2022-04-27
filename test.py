import os
import time
from unittest.mock import Mock

from linguoplotter import Linguoplotter
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.loggers import ActivityLogger, ErrorLogger

results_file_name = "results-a.txt"
if results_file_name in os.listdir():
    print("output file already exists")
    raise Exception

for i in range(30):
    time_string = str(time.time())
    logs_dir_path = f"logs/{time_string}"
    os.mkdir(logs_dir_path)

    log_file_name = f"{logs_dir_path}/activity"
    satisfaction_stream = open(f"{logs_dir_path}/satisfaction.csv", "w")

    error_file_name = f"{logs_dir_path}/errors.log"
    error_stream = open(error_file_name, "w")

    loggers = {
        "activity": ActivityLogger(log_file_name, satisfaction_stream),
        "structure": Mock(),
        "errors": ErrorLogger(error_stream),
    }

    HyperParameters.TESTING = True
    narrator = Linguoplotter.setup(loggers, random_seed=i)
    with open(results_file_name, "a") as results, open("program-a.lisp", "r") as f:
        program = f.read()
        result = narrator.run_program(program)
        result["time"] = time_string
        results.write(str(result))
        results.write("\n")

results_file_name = "results-b.txt"
if results_file_name in os.listdir():
    print("output file already exists")
    raise Exception

for i in range(30):
    time_string = str(time.time())
    logs_dir_path = f"logs/{time_string}"
    os.mkdir(logs_dir_path)

    log_file_name = f"{logs_dir_path}/activity"
    satisfaction_stream = open(f"{logs_dir_path}/satisfaction.csv", "w")

    error_file_name = f"{logs_dir_path}/errors.log"
    error_stream = open(error_file_name, "w")

    loggers = {
        "activity": ActivityLogger(log_file_name, satisfaction_stream),
        "structure": Mock(),
        "errors": ErrorLogger(error_stream),
    }

    HyperParameters.TESTING = True
    narrator = Linguoplotter.setup(loggers, random_seed=i)
    with open(results_file_name, "a") as results, open("program-b.lisp", "r") as f:
        program = f.read()
        result = narrator.run_program(program)
        result["time"] = time_string
        results.write(str(result))
        results.write("\n")

results_file_name = "results-c.txt"
if results_file_name in os.listdir():
    print("output file already exists")
    raise Exception

for i in range(30):
    time_string = str(time.time())
    logs_dir_path = f"logs/{time_string}"
    os.mkdir(logs_dir_path)

    log_file_name = f"{logs_dir_path}/activity"
    satisfaction_stream = open(f"{logs_dir_path}/satisfaction.csv", "w")

    error_file_name = f"{logs_dir_path}/errors.log"
    error_stream = open(error_file_name, "w")

    loggers = {
        "activity": ActivityLogger(log_file_name, satisfaction_stream),
        "structure": Mock(),
        "errors": ErrorLogger(error_stream),
    }

    HyperParameters.TESTING = True
    narrator = Linguoplotter.setup(loggers, random_seed=i)
    with open(results_file_name, "a") as results, open("program-c.lisp", "r") as f:
        program = f.read()
        result = narrator.run_program(program)
        result["time"] = time_string
        results.write(str(result))
        results.write("\n")

results_file_name = "results-d.txt"
if results_file_name in os.listdir():
    print("output file already exists")
    raise Exception

for i in range(30):
    time_string = str(time.time())
    logs_dir_path = f"logs/{time_string}"
    os.mkdir(logs_dir_path)

    log_file_name = f"{logs_dir_path}/activity"
    satisfaction_stream = open(f"{logs_dir_path}/satisfaction.csv", "w")

    error_file_name = f"{logs_dir_path}/errors.log"
    error_stream = open(error_file_name, "w")

    loggers = {
        "activity": ActivityLogger(log_file_name, satisfaction_stream),
        "structure": Mock(),
        "errors": ErrorLogger(error_stream),
    }

    HyperParameters.TESTING = True
    narrator = Linguoplotter.setup(loggers, random_seed=i)
    with open(results_file_name, "a") as results, open("program-d.lisp", "r") as f:
        program = f.read()
        result = narrator.run_program(program)
        result["time"] = time_string
        results.write(str(result))
        results.write("\n")
