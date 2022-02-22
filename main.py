from unittest.mock import Mock

from homer import Homer
from homer.loggers import ActivityLogger


activity_stream = open("activity.log", "w")
loggers = {
    "activity": ActivityLogger(activity_stream),
    "structure": Mock(),
    "errors": Mock(),
}
narrator = Homer.setup(loggers, random_seed=1)

with open("program.lisp", "r") as f:
    program = f.read()
    narrator.run_program(program)

activity_stream.close()
