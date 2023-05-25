from collections import defaultdict
import csv
import statistics

from matplotlib import pyplot

with open("codelet_times.csv", "r") as f:
    reader = csv.DictReader(f)
    codelet_times = [
        {
            "id": row["id"],
            "type": row["type"].split(".")[-1][:-2],
            "start": float(row["start"]),
            "end": float(row["end"]),
        }
        for row in reader
    ]

class_run_times = defaultdict(list)
codelet_type_counts = defaultdict(int)

for row in codelet_times:
    class_run_times[row["type"]].append(row["end"] - row["start"])
    codelet_type_counts[row["type"]] += 1

average_run_times_by_type = [
    (k, statistics.fmean(v)) for k, v in class_run_times.items()
]
average_run_times_by_type.sort(key=lambda x: x[1])

codelet_type_counts = [(k, v) for k, v in codelet_type_counts.items()]
codelet_type_counts.sort(key=lambda x: x[1])


for average_run_time in average_run_times_by_type:
    print(average_run_time)

for count in codelet_type_counts:
    print(count)

x = range(len(codelet_times))
y = [t["end"] - t["start"] for t in codelet_times]
figure = pyplot.figure()
ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(x, y)
ax.set_title("Codelet Run Times Over Time")
ax.set_xlabel("Codelets Run")
ax.set_ylabel("Run length")
ax.set_xticks([x * 5000 for x in range(5)])
ax.set_yticks([0, 1])

pyplot.savefig("runtimes.png")
