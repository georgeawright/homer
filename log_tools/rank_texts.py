import csv

results_file = "/home/george/Documents/phd-notes/satisfaction-survey-results.csv"
output_file = "/home/george/Documents/phd-notes/satisfaction-survey-results-ranks.csv"
rankings = []

with open(results_file, "r") as f, open(output_file, "w") as output_file:
    csvwriter = csv.writer(output_file)
    rows = csv.DictReader(f)

    for row in rows:
        rankings_row = {"WorkerId": row["WorkerId"], "image": row["Input.img_url"]}
        text_ranks = {
            "1": row["Answer.t01"],
            "2": row["Answer.t02"],
            "3": row["Answer.t03"],
            "4": row["Answer.t04"],
            "5": row["Answer.t05"],
            "6": row["Answer.t06"],
            "7": row["Answer.t07"],
            "8": row["Answer.t08"],
            "9": row["Answer.t09"],
            "10": row["Answer.t10"],
        }
        rankings_row["A"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_a"]
        ][0]
        rankings_row["B"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_b"]
        ][0]
        rankings_row["C"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_c"]
        ][0]
        rankings_row["D"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_d"]
        ][0]
        rankings_row["E"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_e"]
        ][0]
        rankings_row["F"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_f"]
        ][0]
        rankings_row["G"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_g"]
        ][0]
        rankings_row["H"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_h"]
        ][0]
        rankings_row["I"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_i"]
        ][0]
        rankings_row["J"] = [
            rank for rank in text_ranks if text_ranks[rank] == row["Input.text_j"]
        ][0]
        rankings.append(rankings_row)
        csvwriter.writerow(rankings_row.values())
