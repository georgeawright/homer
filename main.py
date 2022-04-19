import os
import time
from unittest.mock import Mock

from linguoplotter import Linguoplotter
from linguoplotter.loggers import ActivityLogger, ErrorLogger, StructureLogger

time_string = str(time.time())
logs_dir_path = f"logs/{time_string}"
os.mkdir(logs_dir_path)
structure_logs_dir_path = f"{logs_dir_path}/structures"
os.mkdir(structure_logs_dir_path)

log_file_name = f"{logs_dir_path}/activity"
satisfaction_stream = open(f"{logs_dir_path}/satisfaction.csv", "w")
error_file_name = f"{logs_dir_path}/errors.log"
error_stream = open(error_file_name, "w")
loggers = {
    "activity": ActivityLogger(log_file_name, satisfaction_stream),
    "structure": StructureLogger(f"{structure_logs_dir_path}"),
    "errors": ErrorLogger(error_stream),
}
narrator = Linguoplotter.setup(loggers, random_seed=1)

with open("program.lisp", "r") as f:
    program = f.read()
    narrator.run_program(program)
