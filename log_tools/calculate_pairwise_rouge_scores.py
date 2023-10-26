import json
import os
import statistics
from rouge_score.rouge_scorer import RougeScorer


def calculate_rouge_score(text_1, text_2):
    rouge_scorer = RougeScorer(["rougeL"], use_stemmer=True)
    individual_score = rouge_scorer.score(text_1, text_2)
    return individual_score["rougeL"].precision


texts_by_program_by_hyperparams = {}
log_directories = os.listdir("logs")
for directory in log_directories:
    if directory == "stats.txt":
        continue
    details_file = f"logs/{directory}/details.txt"
    with open(details_file, "r") as f:
        details_json = json.load(f)
    hyperparams = details_json["hyper_parameters"]
    program = details_json["Program"]
    result = details_json["result"]
    result = result if result is None else details_json["result"].replace(" \x08", "")
    try:
        texts_by_program = texts_by_program_by_hyperparams[hyperparams]
    except KeyError:
        texts_by_program_by_hyperparams[hyperparams] = {}
        texts_by_program = texts_by_program_by_hyperparams[hyperparams]
    try:
        texts = texts_by_program[program]
    except KeyError:
        texts_by_program[program] = []
        texts = texts_by_program[program]
    if result is not None:
        texts.append(result)


pairwise_rouges_by_program_by_hyperparams = {
    h: {p: [] for p in texts_by_program}
    for h, texts_by_program in texts_by_program_by_hyperparams.items()
}
mean_rouges_by_program_by_hyperparams = {
    h: {p: [] for p in texts_by_program}
    for h, texts_by_program in texts_by_program_by_hyperparams.items()
}
median_rouges_by_program_by_hyperparams = {
    h: {p: [] for p in texts_by_program}
    for h, texts_by_program in texts_by_program_by_hyperparams.items()
}

for hyperparams, texts_by_program in texts_by_program_by_hyperparams.items():
    for program, texts in texts_by_program.items():
        for i in range(len(texts)):
            for j in range(len(texts)):
                if i == j:  # ignore same output, don't ignore all equal texts
                    continue
                rouge_score = calculate_rouge_score(texts[i], texts[j])
                pairwise_rouges_by_program_by_hyperparams[hyperparams][program].append(
                    rouge_score
                )
for hyperparams, rouges_by_program in pairwise_rouges_by_program_by_hyperparams.items():
    for program, rouges in rouges_by_program.items():
        try:
            mean_rouges_by_program_by_hyperparams[hyperparams][
                program
            ] = statistics.fmean(rouges)
        except statistics.StatisticsError:
            mean_rouges_by_program_by_hyperparams[hyperparams][program] = None
for hyperparams, rouges_by_program in pairwise_rouges_by_program_by_hyperparams.items():
    for program, rouges in rouges_by_program.items():
        try:
            median_rouges_by_program_by_hyperparams[hyperparams][
                program
            ] = statistics.median(rouges)
        except statistics.StatisticsError:
            median_rouges_by_program_by_hyperparams[hyperparams][program] = None

mean_rouges_by_hyperparams = {h: None for h in texts_by_program_by_hyperparams}
median_rouges_by_hyperparams = {h: None for h in texts_by_program_by_hyperparams}

for (
    hyperparams,
    mean_rouges_by_program,
) in mean_rouges_by_program_by_hyperparams.items():
    mean_rouges = [r for r in mean_rouges_by_program.values() if r is not None]
    try:
        mean_rouges_by_hyperparams[hyperparams] = statistics.fmean(mean_rouges)
    except statistics.StatisticsError:
        mean_rouges_by_hyperparams[hyperparams] = None
for (
    hyperparams,
    median_rouges_by_program,
) in median_rouges_by_program_by_hyperparams.items():
    median_rouges = [r for r in median_rouges_by_program.values() if r is not None]
    try:
        median_rouges_by_hyperparams[hyperparams] = statistics.median(median_rouges)
    except statistics.StatisticsError:
        median_rouges_by_hyperparams[hyperparams] = None

for hyperparams in mean_rouges_by_hyperparams:
    print(
        hyperparams,
        mean_rouges_by_hyperparams[hyperparams],
        median_rouges_by_hyperparams[hyperparams],
    )
