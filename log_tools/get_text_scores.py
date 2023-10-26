import csv

with open("/home/george/Documents/phd-notes/texts-20.csv", "r") as f:
    rows = csv.DictReader(
        f, fieldnames=("hyperparams", "seed", "program", "time", "text", "quality")
    )

    hyperparameters = [
        "h01",
        "h02",
        "h03",
        "h04",
        "h05",
        "h06",
        "h07",
        "h08",
        "h08",
        "h10",
        "h11",
        "h12",
        "h13",
        "h14",
        "h15",
        "h16",
        "h17",
        "h18",
        "h19",
        "h20",
        "h21",
        "h22",
        "h23",
        "h24",
        "h25",
        "h26",
        "h27",
        "h28",
        "h29",
        "h30",
        "h31",
        "h32",
        "h33",
        "h34",
        "h35",
        "h36",
        "h37",
        "h38",
        "h39",
        "h40",
    ]

    p = {
        "narration-1.lisp": {
            "temperatures will be cool in the country between saturday and sunday": {},
            "temperatures will be cold in the country between saturday and sunday": {},
            "temperatures will be cool in the country between saturday and sunday and they will be cold in the country between friday and saturday": {},
            "temperatures will be cold in the country between friday and saturday but they will be cool in the country between saturday and sunday": {},
            "temperatures will decrease in the country between saturday and sunday": {},
            "temperatures will be cold in the country between friday and saturday and they will be cool in the country between saturday and sunday": {},
            "temperatures will be cool in the southeast between saturday and sunday": {},
            "temperatures will be cool in the country between saturday and sunday and they will decrease in the country between saturday and sunday": {},
            "temperatures will be cold in the country on friday": {},
            "temperatures will be cool in the country between saturday and sunday meanwhile they will decrease in the country between saturday and sunday": {},
        },
        "narration-2.lisp": {
            "temperatures will increase in the country between friday and saturday": {},
            "temperatures will increase in the country between saturday and sunday": {},
            "temperatures will increase in the country between friday and saturday and they will increase in the country between saturday and sunday": {},
            "temperatures will be cool in the country between friday and saturday": {},
            "temperatures will be hotter in the country on sunday than in the country on saturday": {},
            "temperatures will be milder in the country on saturday than in the country on sunday": {},
            "temperatures will increase in the country between friday and saturday then they will increase in the country between saturday and sunday": {},
            "temperatures will be hot in the country on sunday": {},
            "temperatures will be hot across the west on sunday": {},
            "temperatures will be warm in the country on saturday": {},
        },
        "narration-3.lisp": {
            "temperatures will be cool across the north on sunday": {},
            "temperatures will increase across the south between friday and saturday": {},
            "the warm temperatures will move from the north southwards between saturday and sunday": {},
            "the warm temperatures will move from the southeast northwestwards between friday and saturday": {},
            "temperatures will be warm across the south on friday but they will be cool across the north on sunday": {},
            "the warm temperatures will move from the south northwards between friday and saturday then they will move from the north southwards between saturday and sunday": {},
            "temperatures will be colder across the north on friday than across the north on saturday": {},
            "temperatures will be warmer across the north on saturday than across the north on sunday": {},
            "temperatures will be cold in the north on friday": {},
            "temperatures will be warm across the north on saturday": {},
        },
        "narration-4.lisp": {
            "temperatures will be cool in the west on saturday": {},
            "the hot temperatures will move from the east westwards between saturday and sunday": {},
            "the hot temperatures across the southeast will shrink between saturday and sunday": {},
            "the cool temperatures will move from the not northeast northeastwards between saturday and sunday": {},
            "temperatures will decrease in the majority of the country between saturday and sunday": {},
            "the hot temperatures across the not majority of the country will shrink between saturday and sunday": {},
            "the hot temperatures across the east will shrink between saturday and sunday": {},
            "the cool temperatures will spread from the south northwards between saturday and sunday": {},
            "the mild temperatures will move from the southeast northwestwards between friday and saturday": {},
            "temperatures will be hot in the midlands between saturday and sunday": {},
        },
        "narration-5.lisp": {
            "the hot temperatures will move from the south northwards between friday and saturday": {},
            "the hot temperatures will spread from the south northwards between friday and saturday": {},
            "temperatures will be good across the southwest between friday and saturday": {},
            "temperatures will be hot in the south between friday and saturday": {},
            "the hot temperatures will move from the south northwards between friday and saturday and the cool temperatures will move from the north northwards between saturday and sunday": {},
            "the hot temperatures will spread from the south northwards between saturday and sunday and they will move from the south northwards between friday and saturday": {},
            "the good temperatures will move from the south northwards between friday and saturday and temperatures will be hot across the west between saturday and sunday": {},
            "the high temperatures will move from the south northwards between friday and saturday": {},
            "the hot temperatures will move from the south northwards between friday and saturday but the cool temperatures will move from the not east eastwards between friday and saturday": {},
            "temperatures will be mild across the east on saturday": {},
        },
        "narration-6.lisp": {
            "the hot temperatures will move from the southwest northeastwards between friday and saturday": {},
            "the hot temperatures will move from the south northwards between friday and saturday": {},
            "the hot temperatures will move from the west eastwards between friday and saturday": {},
            "the cool temperatures will move from the east westwards between friday and saturday": {},
            "temperatures will be cool in the majority of the country between friday and saturday": {},
            "temperatures will be hot across the north on sunday": {},
            "the hot temperatures will move from the northeast northeastwards between saturday and sunday": {},
            "the hot temperatures will move from the not northeast northeastwards between saturday and sunday": {},
            "the cool temperatures across the northwest will expand between friday and saturday": {},
            "temperatures will be hotter in the midlands on saturday than across the majority of the country on sunday": {},
        },
    }

    for row in rows:
        hyperparams = row["hyperparams"].split("/")[1].split(".")[0]
        program = row["program"]
        text = row["text"].replace(" ", "")
        quality = row["quality"]

        if text not in p[program]:
            continue
        if hyperparams not in p[program][text]:
            p[program][text][hyperparams] = quality
        else:
            if quality > p[program][text][hyperparams]:
                p[program][text][hyperparams] = quality

for program in p:
    print(program)
    for t in p[program]:
        print(
            "\t".join(
                [
                    p[program][t][h] if h in p[program][t] else ""
                    for h in hyperparameters
                ]
            )
        )
