from unittest.mock import Mock

from homer import Homer
from homer.loggers import ActivityLogger, StructureLogger


activity_stream = open("logs/activity.log", "w")
satisfaction_stream = open("logs/satisfaction.csv", "w")
loggers = {
    "activity": ActivityLogger(activity_stream, satisfaction_stream),
    "structure": StructureLogger("logs/structures"),
    "errors": Mock(),
}
narrator = Homer.setup(loggers, random_seed=1)

with open("program.lisp", "r") as f:
    program = f.read()
    narrator.run_program(program)

activity_stream.close()
