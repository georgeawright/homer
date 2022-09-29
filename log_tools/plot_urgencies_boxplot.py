import statistics

from matplotlib import pyplot

log_directories = [
    "1662051198.4181452",
    "1662051655.8630729",
    "1662051788.519332",
    "1662052132.4650414",
    "1662052204.919932",
    "1662049847.8702214",
    "1662050022.2789903",
    "1662050178.2850618",
    "1662050284.1352236",
    "1662050963.264788",
]

average_ages_when_run = []
average_urgencies_of_codelets_run = []
urgencies_of_codelets_run = []

for directory in log_directories:
    codelets_spawned_file = f"logs/{directory}/codelets_spawned"
    codelets_run_file = f"logs/{directory}/codelets_run"

    with open(codelets_spawned_file, "r") as f:
        lines = f.readlines()
    codelets_spawned = []
    for line in lines:
        info = line.split(",")
        codelets_spawned.append(
            {
                "time": int(info[0]),
                "codelet": info[1],
                "urgency": float(info[2]),
            }
        )

    with open(codelets_run_file, "r") as f:
        lines = f.readlines()
    codelets_run = []
    for line in lines:
        info = line.split(",")
        codelets_run.append(
            {
                "time": int(info[0]),
                "codelet": info[1],
                "urgency": float(info[2]) if float(info[2]) < 1.0 else 1.0,
            }
        )
    urgencies = [c["urgency"] for c in codelets_run]
    urgencies_of_codelets_run.append(urgencies)

    average_urgency_of_run_codelet = statistics.fmean(
        [codelet["urgency"] for codelet in codelets_run]
    )
    average_urgencies_of_codelets_run.append(average_urgency_of_run_codelet)
    print(average_urgency_of_run_codelet)

# figure = pyplot.figure()
# ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
figurge, ax = pyplot.subplots()

ax.set_title("Urgency of Codelets Run")
ax.set_xlabel("Run (0=without coderack cleaner, 1=with coderack cleaner)")
ax.set_ylabel("Urgency")
ax.set_xticklabels(["0"] * 5 + ["1"] * 5)

bp = ax.boxplot(urgencies_of_codelets_run, 0, "")

pyplot.savefig(f"urgencies_boxplot.png")
