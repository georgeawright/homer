import json
import statistics

print("-" * 80)
results_file_name = "results-d.txt"
print(results_file_name)

texts = {}
with open(results_file_name, "r") as f:
    results = f.readlines()
    for result in results:
        result = result.replace("'", '"')
        result = result.replace(" \\x08", "")
        result = json.loads(result)
        text = result["result"]
        satisfaction = result["satisfaction"]
        codelets_run = result["codelets_run"]
        if text in texts:
            texts[text]["satisfactions"].append(satisfaction)
            texts[text]["run_lengths"].append(codelets_run)
        else:
            texts[text] = {
                "satisfactions": [satisfaction],
                "run_lengths": [codelets_run],
            }

for text in texts:
    texts[text]["mean_satisfaction"] = statistics.fmean(texts[text]["satisfactions"])
    texts[text]["mean_run_length"] = statistics.fmean(texts[text]["run_lengths"])
    texts[text]["frequency"] = len(texts[text]["run_lengths"])
    print(text, texts[text])

highest_mean_satisfaction = 0
highest_actual_satisfaction = 0
highest_frequency = 0
lowest_mean_satisfaction = 1
lowest_actual_satisfaction = 1

texts_with_highest_mean_satisfaction = []
texts_with_highest_actual_satisfaction = []
texts_with_highest_frequency = []
texts_with_lowest_mean_satisfaction = []
texts_with_lowest_actual_satisfaction = []

for text in texts:
    if texts[text]["mean_satisfaction"] > highest_mean_satisfaction:
        highest_mean_satisfaction = texts[text]["mean_satisfaction"]
        texts_with_highest_mean_satisfaction = [text]
    elif texts[text]["mean_satisfaction"] == highest_mean_satisfaction:
        texts_with_highest_mean_satisfaction.append(text)

    if max(texts[text]["satisfactions"]) > highest_actual_satisfaction:
        highest_actual_satisfaction = max(texts[text]["satisfactions"])
        texts_with_highest_actual_satisfaction = [text]
    elif max(texts[text]["satisfactions"]) == highest_actual_satisfaction:
        texts_with_highest_actual_satisfaction.append(text)

    if texts[text]["frequency"] > highest_frequency:
        highest_frequency = texts[text]["frequency"]
        texts_with_highest_frequency = [text]
    elif texts[text]["frequency"] == highest_frequency:
        texts_with_highest_frequency.append(text)

    if texts[text]["mean_satisfaction"] < lowest_mean_satisfaction:
        lowest_mean_satisfaction = texts[text]["mean_satisfaction"]
        texts_with_lowest_mean_satisfaction = [text]
    elif texts[text]["mean_satisfaction"] == lowest_mean_satisfaction:
        texts_with_lowest_mean_satisfaction.append(text)

    if min(texts[text]["satisfactions"]) < lowest_actual_satisfaction:
        lowest_actual_satisfaction = min(texts[text]["satisfactions"])
        texts_with_lowest_actual_satisfaction = [text]
    elif min(texts[text]["satisfactions"]) == lowest_actual_satisfaction:
        texts_with_lowest_actual_satisfaction.append(text)

print("highest mean satisfaction")
print(highest_mean_satisfaction, texts_with_highest_mean_satisfaction)
print("highest actual satisfaction")
print(highest_actual_satisfaction, texts_with_highest_actual_satisfaction)
print("highest frequency")
print(highest_frequency, texts_with_highest_frequency)
print("lowest mean satisfaction")
print(lowest_mean_satisfaction, texts_with_lowest_mean_satisfaction)
print("lowest actual satisfaction")
print(lowest_actual_satisfaction, texts_with_lowest_actual_satisfaction)
