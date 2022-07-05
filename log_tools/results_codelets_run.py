import json
import statistics

print("-" * 80)
results_file_name = "results-d.txt"
print(results_file_name)

run_lengths = []
with open(results_file_name, "r") as f:
    results = f.readlines()
    for result in results:
        result = result.replace("'", '"')
        result = result.replace(" \\x08", "")
        result = json.loads(result)
        codelets_run = result["codelets_run"]
        run_lengths.append(codelets_run)

mean_run_length = statistics.fmean(run_lengths)
sd = statistics.stdev(run_lengths)
print("mean:", mean_run_length)
print("standard dev:", sd)
