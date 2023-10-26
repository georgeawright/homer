import csv

selected_texts = {
    "temperatures will be cool in the country between saturday and sunday",
    "temperatures will be cold in the country between saturday and sunday",
    "temperatures will be cool in the country between saturday and sunday and they will be cold in the country between friday and saturday",
    "temperatures will be cold in the country between friday and saturday but they will be cool in the country between saturday and sunday",
    "temperatures will decrease in the country between saturday and sunday",
    "temperatures will be cold in the country between friday and saturday and they will be cool in the country between saturday and sunday",
    "temperatures will be cool in the southeast between saturday and sunday",
    "temperatures will be cool in the country between saturday and sunday and they will decrease in the country between saturday and sunday",
    "temperatures will be cold in the country on friday",
    "temperatures will be cool in the country between saturday and sunday meanwhile they will decrease in the country between saturday and sunday",
    "temperatures will increase in the country between friday and saturday",
    "temperatures will increase in the country between saturday and sunday",
    "temperatures will increase in the country between friday and saturday and they will increase in the country between saturday and sunday",
    "temperatures will be cool in the country between friday and saturday",
    "temperatures will be hotter in the country on sunday than in the country on saturday",
    "temperatures will be milder in the country on saturday than in the country on sunday",
    "temperatures will increase in the country between friday and saturday then they will increase in the country between saturday and sunday",
    "temperatures will be hot in the country on sunday",
    "temperatures will be hot across the west on sunday",
    "temperatures will be warm in the country on saturday",
    "temperatures will be cool across the north on sunday",
    "temperatures will increase across the south between friday and saturday",
    "the warm temperatures will move from the north southwards between saturday and sunday",
    "the warm temperatures will move from the southeast northwestwards between friday and saturday",
    "temperatures will be warm across the south on friday but they will be cool across the north on sunday",
    "the warm temperatures will move from the south northwards between friday and saturday then they will move from the north southwards between saturday and sunday",
    "temperatures will be colder across the north on friday than across the north on saturday",
    "temperatures will be warmer across the north on saturday than across the north on sunday",
    "temperatures will be cold in the north on friday",
    "temperatures will be warm across the north on saturday",
    "temperatures will be cool in the west on saturday",
    "the hot temperatures will move from the east westwards between saturday and sunday",
    "the hot temperatures across the southeast will shrink between saturday and sunday",
    "the cool temperatures will move from the not northeast northeastwards between saturday and sunday",
    "temperatures will decrease in the majority of the country between saturday and sunday",
    "the hot temperatures across the not majority of the country will shrink between saturday and sunday",
    "the hot temperatures across the east will shrink between saturday and sunday",
    "the cool temperatures will spread from the south northwards between saturday and sunday",
    "the mild temperatures will move from the southeast northwestwards between friday and saturday",
    "temperatures will be hot in the midlands between saturday and sunday",
    "the hot temperatures will move from the south northwards between friday and saturday",
    "the hot temperatures will spread from the south northwards between friday and saturday",
    "temperatures will be good across the southwest between friday and saturday",
    "temperatures will be hot in the south between friday and saturday",
    "the hot temperatures will move from the south northwards between friday and saturday and the cool temperatures will move from the north northwards between saturday and sunday",
    "the hot temperatures will spread from the south northwards between saturday and sunday and they will move from the south northwards between friday and saturday",
    "the good temperatures will move from the south northwards between friday and saturday and temperatures will be hot across the west between saturday and sunday",
    "the high temperatures will move from the south northwards between friday and saturday",
    "the hot temperatures will move from the south northwards between friday and saturday but the cool temperatures will move from the not east eastwards between friday and saturday",
    "temperatures will be mild across the east on saturday",
    "the hot temperatures will move from the southwest northeastwards between friday and saturday",
    "the hot temperatures will move from the south northwards between friday and saturday",
    "the hot temperatures will move from the west eastwards between friday and saturday",
    "the cool temperatures will move from the east westwards between friday and saturday",
    "temperatures will be cool in the majority of the country between friday and saturday",
    "temperatures will be hot across the north on sunday",
    "the hot temperatures will move from the northeast northeastwards between saturday and sunday",
    "the hot temperatures will move from the not northeast northeastwards between saturday and sunday",
    "the cool temperatures across the northwest will expand between friday and saturday",
    "temperatures will be hotter in the midlands on saturday than across the majority of the country on sunday",
}

with open("/home/george/Documents/phd-notes/texts-20.csv", "r") as f:
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

hs = list(texts_by_program_by_hyperparams.keys())
hs.sort()

for program, hyperparams_by_text in hyperparams_by_text_by_program.items():
    if program != "narration-6.lisp":
        continue
    print("program", program)
    ths = list(hyperparams_by_text.items())
    ths.sort(key=lambda x: len(x[1]), reverse=True)
    for text, hyperparams in ths:
        if len(hyperparams) < 8:
            continue
        # if text not in selected_texts:
        #    continue
        print(text)
        hyperparams_list = list(hyperparams)
        hyperparams_list.sort()
        print(",".join(hyperparams_list))
        h_vector = ["1" if h in hyperparams else "0" for h in hs]
        print("\t".join(h_vector))
