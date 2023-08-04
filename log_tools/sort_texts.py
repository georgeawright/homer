import csv

with open("logs/texts.csv", "r") as f:
    rows = csv.DictReader(
        f, fieldnames=("hyperparams", "seed", "program", "time", "text", "quality")
    )

    texts_by_program_by_hyperparams = {}
    hyperparams_by_text_by_program = {}

    for row in rows:
        hyperparams = row["hyperparams"].split("/")[1].split(".")[0]
        program = row["program"]
        text = row["text"]
        quality = row["quality"]
        try:
            texts_by_program = texts_by_program_by_hyperparams[hyperparams]
        except KeyError:
            texts_by_program_by_hyperparams[hyperparams] = {}
            texts_by_program = texts_by_program_by_hyperparams[hyperparams]
        try:
            texts = texts_by_program[program]
        except KeyError:
            texts_by_program[program] = {}
            texts = texts_by_program[program]
        try:
            highest_quality = texts[text]
            if quality > highest_quality:
                texts[text] = quality
        except KeyError:
            texts[text] = quality

        try:
            hyperparams_by_text = hyperparams_by_text_by_program[program]
        except KeyError:
            hyperparams_by_text_by_program[program] = {}
            hyperparams_by_text = hyperparams_by_text_by_program[program]
        try:
            all_hyperparams = hyperparams_by_text[text]
        except KeyError:
            hyperparams_by_text[text] = set()
            all_hyperparams = hyperparams_by_text[text]
        all_hyperparams.add(hyperparams)

for program, hyperparams_by_text in hyperparams_by_text_by_program.items():
    print("program", program)
    for text, hyperparams in hyperparams_by_text.items():
        if len(hyperparams) < 5:
            continue
        print(text)
        print(hyperparams)
    print()
