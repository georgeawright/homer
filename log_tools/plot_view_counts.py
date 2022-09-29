import csv

from matplotlib import pyplot

log_directories = [
    "1662052910.423777",
    "1662053106.142147",
    "1662053195.6314495",
    "1662053359.2686157",
    "1662053389.9120748",
    "1662049847.8702214",
    "1662050022.2789903",
    "1662050178.2850618",
    "1662050284.1352236",
    "1662050963.264788",
]


figure = pyplot.figure()
ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])

line_count = 0
for log_directory in log_directories:
    x = []
    y = []
    with open(f"logs/{log_directory}/view_count.csv") as f:
        csv_reader = csv.reader(f)
        i = 0
        for row in csv_reader:
            if i % 500 == 0:
                x.append(int(row[0]))
                y.append(float(row[1]))
            i += 1

    if line_count < 5:
        color = "#FFC20A"
    elif line_count < 10:
        color = "#0C7BDC"
    else:
        color = "black"

    if line_count == 0:
        (line1,) = ax.plot(x, y, color=color)
        line1.set_label("Without Recycler + Garbage Collector")
    elif line_count == 5:
        (line2,) = ax.plot(x, y, color=color)
        line2.set_label("With Recyler + Garbage Collector")
    else:
        ax.plot(x, y, color=color)
    ax.set_title("Number of Views Over Time")
    ax.set_xlabel("Codelets Run")
    ax.set_ylabel("Number of Views")
    ax.set_xticks([x * 10000 for x in range(6)])

    line_count += 1

ax.legend(handles=[line1, line2])
pyplot.savefig("view_counts.png")
