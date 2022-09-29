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
        birth_time = None
        for c in codelets_spawned:
            if c["codelet"] == info[1]:
                birth_time = c["time"]
                break
        codelets_run.append(
            {
                "time": int(info[0]),
                "codelet": info[1],
                "urgency": float(info[2]),
                "birth_time": birth_time,
            }
        )
    urgencies = [c["urgency"] for c in codelets_run]
    urgencies_of_codelets_run.append(urgencies)

    average_urgency_of_run_codelet = statistics.fmean(
        [codelet["urgency"] for codelet in codelets_run]
    )
    average_urgencies_of_codelets_run.append(average_urgency_of_run_codelet)
    print(average_urgency_of_run_codelet)

    average_age_when_run = statistics.fmean(
        [codelet["time"] - codelet["birth_time"] for codelet in codelets_run]
    )
    average_ages_when_run.append(average_age_when_run)
    print(average_age_when_run)

figure = pyplot.figure()
ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
for i in range(len(average_ages_when_run)):
    age = average_ages_when_run[i]
    if i == 0:
        colour = "#FFC20A"
        (bar1,) = ax.bar(i, age, color=colour)
        bar1.set_label("Without Coderack Cleaner")
    elif i == 5:
        colour = "#0C7BDC"
        (bar2,) = ax.bar(i, age, color=colour)
        bar2.set_label("With Coderack Cleaner")
    else:
        ax.bar(i, age, color=colour)

ax.set_title("Average Age of Codelets When Run")
ax.set_xlabel("Run")
ax.set_ylabel("Codelets Run")
ax.set_xticks([])
ax.legend(handles=[bar1, bar2])

pyplot.savefig(f"codelet_ages.png")

figure = pyplot.figure()
ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
for i in range(len(average_urgencies_of_codelets_run)):
    urgency = average_urgencies_of_codelets_run[i]
    if i == 0:
        colour = "#FFC20A"
        (bar1,) = ax.bar(i, urgency, color=colour)
        bar1.set_label("Without Coderack Cleaner")
    elif i == 5:
        colour = "#0C7BDC"
        (bar2,) = ax.bar(i, urgency, color=colour)
        bar2.set_label("With Coderack Cleaner")
    else:
        ax.bar(i, urgency, color=colour)

ax.set_title("Average Urgency of Codelets Run")
ax.set_xlabel("Run")
ax.set_ylabel("Urgency")
ax.set_xticks([])
ax.legend(handles=[bar1, bar2])

pyplot.savefig(f"codelet_urgencies.png")
