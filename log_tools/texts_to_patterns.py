import json
import os
import statistics

LOGS_DIRECTORY = "logs_100_seeds"

VERBS = ["be", "move", "increase", "decrease", "shrink", "expand", "spread"]
CONJUNCTIONS = ["and", "but", "then", "meanwhile"]
DAYS = ["friday", "saturday", "sunday"]


def text_to_discourse_structure(text: str):
    words = text.split(" ")
    relevant_words = []
    for i in range(len(words)):
        word = words[i]
        try:
            next_word = words[i + 1]
        except IndexError:
            next_word = None
        if word in VERBS:
            pass
            # relevant_words.append(word)
        if word in CONJUNCTIONS and next_word not in DAYS:
            relevant_words.append(word)
    structure = "-".join(relevant_words)
    if len(structure) == 0:
        return "None"
    return structure


def text_to_temporal_ordering(text: str):
    words = text.split(" ")
    relevant_words = []
    for i in range(len(words)):
        word = words[i]
        if word in DAYS:
            relevant_words.append(word)
    structure = "-".join(relevant_words)
    if len(structure) == 0:
        return "None"
    return structure


discourse_results = {}
temporal_results = {}

log_directories = os.listdir(LOGS_DIRECTORY)
for log_directory in log_directories:
    try:
        with open(f"{LOGS_DIRECTORY}/{log_directory}/details.txt") as f:
            results = json.load(f)
    except NotADirectoryError:
        continue
    program = results["Program"]
    text = results["result"] if results["result"] is not None else ""
    satisfaction = results["satisfaction"]
    codelets = results["codelets_run"]
    if program not in discourse_results:
        discourse_results[program] = {}
        temporal_results[program] = {}
    discourse_structure = text_to_discourse_structure(text)
    temporal_ordering = text_to_temporal_ordering(text)
    if discourse_structure not in discourse_results[program]:
        discourse_results[program][discourse_structure] = {
            "satisfactions": [satisfaction],
            "codelets": [codelets],
        }
    else:
        discourse_results[program][discourse_structure]["satisfactions"].append(
            satisfaction
        )
        discourse_results[program][discourse_structure]["codelets"].append(codelets)
    if temporal_ordering not in temporal_results[program]:
        temporal_results[program][temporal_ordering] = {
            "satisfactions": [satisfaction],
            "codelets": [codelets],
        }
    else:
        temporal_results[program][temporal_ordering]["satisfactions"].append(
            satisfaction
        )
        temporal_results[program][temporal_ordering]["codelets"].append(codelets)

for program, results in discourse_results.items():
    for result, stats in results.items():
        stats["frequency"] = len(stats["satisfactions"])
        stats["mean_satisfaction"] = statistics.fmean(stats["satisfactions"])
        stats["median_satisfaction"] = statistics.median(stats["satisfactions"])
        stats["mean_codelets"] = statistics.fmean(stats["codelets"])
        stats["median_codelets"] = statistics.median(stats["codelets"])
        try:
            stats["stdev_satisfaction"] = statistics.stdev(stats["satisfactions"])
            stats["stdev_codelets"] = statistics.stdev(stats["codelets"])
        except statistics.StatisticsError:
            stats["stdev_satisfaction"] = None
            stats["stdev_codelets"] = None
for program, results in temporal_results.items():
    for result, stats in results.items():
        stats["frequency"] = len(stats["satisfactions"])
        stats["mean_satisfaction"] = statistics.fmean(stats["satisfactions"])
        stats["median_satisfaction"] = statistics.median(stats["satisfactions"])
        stats["mean_codelets"] = statistics.fmean(stats["codelets"])
        stats["median_codelets"] = statistics.median(stats["codelets"])
        try:
            stats["stdev_satisfaction"] = statistics.stdev(stats["satisfactions"])
            stats["stdev_codelets"] = statistics.stdev(stats["codelets"])
        except statistics.StatisticsError:
            stats["stdev_satisfaction"] = None
            stats["stdev_codelets"] = None

totals = {}
for program in discourse_results:
    for result, stats in discourse_results[program].items():
        if result in totals:
            totals[result] += stats["frequency"]
        else:
            totals[result] = stats["frequency"]

print("Pattern\tTotal")
for result, total in totals.items():
    print(f"{result}\t{total}")
