import json
import os
import statistics

from matplotlib import pyplot

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
    codelets = details["codelets_run"]
    if program not in program_results:
        program_results[program] = []
    program_results[program].append(codelets)

program_results = list(program_results.items())
program_results.sort(key=lambda x: x[0])
programs = [program.split(".")[0].split("-")[1] for program, _ in program_results]
run_times = [[x for x in results] for _, results in program_results]

figure, ax = pyplot.subplots()
figure.set_figwidth(8)
figure.set_figheight(6)
ax.set_title("Runtimes (in codelets) for each Input")
ax.set_xlabel("Input Sequence")
ax.set_ylabel("Runtime (number of codelets run)")
ax.set_xticklabels(programs)

bp = ax.boxplot(run_times, 0, "")

pyplot.savefig(f"runtimes_boxplot.png")
