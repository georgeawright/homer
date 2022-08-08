import csv
import os

from matplotlib import pyplot

log_directories = os.listdir("logs/")
log_directories.sort()
print(log_directories)
log_directory = log_directories[-1]

x = []
y = []
with open(f"logs/{log_directory}/view_count.csv") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        x.append(int(row[0]))
        y.append(float(row[1]))

figure = pyplot.figure()
ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(x, y)
ax.set_title("View Count Over Time")
ax.set_xlabel("Codelets Run")
ax.set_ylabel("View Count")
ax.set_xticks([x * 5000 for x in range(5)])

pyplot.savefig(f"logs/{log_directory}/view_count.png")
