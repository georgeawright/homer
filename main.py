import os
import time

from linguoplotter import Linguoplotter
from linguoplotter.loggers import ActivityLogger, ErrorLogger, StructureLogger

pwd = os.getcwd()

time_string = str(time.time())
logs_dir_path = f"{pwd}/logs/{time_string}"
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
narrator = Linguoplotter.setup(loggers, random_seed=3)
narrator.interpreter.interpret_file("builtin.lisp")

os.chdir("example-programs/weather")
narrator.interpreter.interpret_file("narration-5-change-in-size.lisp")
os.chdir("../..")
narrator.run()
