import statistics
from rouge_score.rouge_scorer import RougeScorer
from matplotlib import pyplot


def calculate_metrics(hypothesis_text, reference_texts):
    metrics = {}
    rouge_scores = {
        "rouge1-recall": [],
        "rouge1-precision": [],
        "rouge1-f1": [],
        "rouge2-recall": [],
        "rouge2-precision": [],
        "rouge2-f1": [],
        "rougeL-recall": [],
        "rougeL-precision": [],
        "rougeL-f1": [],
    }
    rouge_scorer = RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    for reference_text in reference_texts:
        individual_scores = rouge_scorer.score(reference_text, hypothesis_text)
        for metric in individual_scores:
            rouge_scores[metric + "-recall"].append(individual_scores[metric].recall)
            rouge_scores[metric + "-precision"].append(
                individual_scores[metric].precision
            )
            rouge_scores[metric + "-f1"].append(individual_scores[metric].fmeasure)
    for rouge_score in rouge_scores:
        metrics[rouge_score + "-max"] = max(rouge_scores[rouge_score])
        metrics[rouge_score + "-med"] = statistics.median(rouge_scores[rouge_score])
    return metrics


references = {
    "1": [
        "Temperatures are fairly consistently cool in all regions over the three days.",
        "Cool throughout the weekend.",
        "Cold weather",
        "The temperature remains fairly stable and cool throughout the weekend.",
        "On Friday it will be cool everywhere, 5-6, except in the north-west corner where it will be 3. On Saturday it will be two or three degrees warmer everywhere, falling back on Sunday",
        "You'll need a warm coat every day wherever you are. It's going to be uniformly cold, with temperatures between 3-8 degrees throughout.",
        "Temperature even across the country Friday to Sunday. Highest temperatures on Saturday.",
        "Cold everywhere over the weekend with temperatures between 3 and 6 degrees on Friday.  A little warmer on Saturday with lows of 6 and highs of 8.  Temperatures drop a little again on Sunday ranging from 4 to 6 degrees.",
    ],
    "2": [
        "Temperatures are only slightly higher in the south. In both regions they rise considerably on Sunday.",
        "The temperature is increasing through the weekend to highs of 23 on Sunday."
        "Cool on Friday, slightly improving on Saturday and warm on Sunday.",
        "Warming up over the weekend",
        "On Friday, temperatures will range between 8 and 10 in the north, 11 and 12 in the south. On Saturday there will be a rise of about three degrees everywhere. Sunday there will be a further rise of about 9 degrees.",
        "Cool temperatures, between 9-12 degrees, will dominate on Friday, but expect warmer temperatures, up to 15 degrees in the south, 9n Saturday. Come Sunday everywhere will enjoy temperatures in the 20s, with 22 degrees in the Midlands and South.",
        "Temperatures will increase across the country from a high of 11 on Friday to 22 on Sunday.",
        "Fairly cold on Friday with temperatures varying between 8 and 12 degrees.  A little warmer everywhere on Saturday with temperatures reaching 15 in some southern areas.  A big change on Sunday however with warm weather across the country ranging from 21 in the east and central areas to 23 in the south east.",
    ],
    "3": [
        "Temperatures are consistently much higher in the south. Temperatures increase on Saturday, then become cooler on Sunday, in both the north and the south. ",
        "Warm air moving from the south to the north and then retreating.",
        "A big difference in temperature between north and south on Friday, warming everywhere on Saturday. Cooling again on Sunday.",
        "Saturday will see a spike in warmer temperatures across the board, while Sunday will see a return to Friday's climate for the south. It will be somewhat warmer in the north on Sunday than it was on Friday.",
        "It's a tale of two halves. Starting with the North, temperatures will be cold on Friday, but climb to 17 degrees on saturday before dipping to 10 on Sunday. The South is much warmer, with temperatures reaching 25 in the south east on Saturday, but dipping again on Sunday.",
        "The south will have highs of 19 on Friday while the north will have lows of 3. The south will have similar highs of 22 on Saturday but the temperature in the north will rise to 17. Sunday will see Saturday temperatures drop everywhere but the south will still have the highest temperatures.",
        "A marked difference on Friday between north and south of the country with temperatures of 3-5 degrees in the north. The south however will be much warmer with temperatures of between 15 and 19 degrees. Better in the north on Saturday with highs of 25 in the south east.  Still cooler in the north but much higher than Friday, wiht temperatures between 17 and 17 degrees. Cooler for everyone on Sunday but still noticeably higher in the south with highs of 17 to 18, whereas the temperature will struggle to reach double figures in the north.",
    ],
    #    "4": [
    #        "Temperatures are generally higher in the central region and are fairly consistent over the three days. ",
    #        "Warm inland and on the east coast, slightly cooling on Saturday and only wam inland Sunday.",
    #        "Getting colder over the weekend",
    #        "The temperature is staying fairly stable in the centre of the country, with the east dropping by 10 degrees through the weekend",
    #        "On Friday and Saturday, temperatures will range between 10 and 24, cooler in the west and south-east. On Sunday temperatures will range between 9 and 12, except in some central areas where they will remain at 21/22.",
    #        "Over the next three days expect the eastern coast and the Midlands to be warm, but cooler elsewhere. On Friday parts of the northern coast will also enjoy this warmth. By Sunday cooler temperatures will encroach from the south east.",
    #        "The centre of the country and the east coast will have highs of 22 on Sat. The rest of the country will be 10 to 13 apart from odd spots on the north and south coast which will also experience 22. This will be the same on Friday although the highest temperature on the north and south coasts will be 15-17. On Sunday only the centre of the country will have highs of 22, the rest will be 9 to 11 with the north west being the coldest.",
    #        "On Friday it'll be cold in the west and generally much warmer elsewhere apart from the north and south east corners.  A similar pattern on Saturday with the highest temperatures in central areas although it will be a couple of degrees cooler in these areas than on Friday.  A much cooler picture on Sunday with only the central area staying at 21 or 22.  The rest of the country will be much colder wiht temperatures no higher than 12 and down to single figures in the north west.",
    #    ],
    #    "5": [
    #        "Temperatures are much higher on Friday and Saturday in the southwest. Then on Sunday the hotter weather also spreads further north and east",
    #        "Warmth moving inland from the south west from Friday to Sunday.",
    #        "The warmer temperatures will gradually radiate northeast from the Southwest as the weekend progresses",
    #        "Friday 8-11 everywhere, except far south-west where it will be 22. The warmer weather will spread north-eastwards on Saturday. The north-east will be cooler at 6. On Sunday the southern and western two thirds of the country will be warm (21-23), the northern and eastern peripheries cooler.",
    #        "On friday, a corner of warmth in the south west will move across the country over the next two days to bring temperatures in the 20s to the south west and Midlands by Sunday. The rest of the country will see temperatures drop from an average of 10 on Friday to 6 on Sunday.",
    #        "Highs of 22 in the south west on Friday with the rest of the country having 9 to 11. The higher temperatures will spread throughout the country on Saturday and Sunday apart from the north and east with the north east getting as low as 3.",
    #        "Warm weather moving up slowly from the south west over the weekend.  On friday the south west tip will see temperatures of 22, in marked contrast to the rest of the country which will struggle to reach double figures, 11 at best. Saturday will see the warm temperatures reaching further up the east coastal and central areas with most  the rest of the  country will experience a drop in temperature or stay the same as Friday. By Sunday the warm weather will have spread to most of the east coast and central areas although the far north and the east coast will remain cold.",
    #    ],
    #    "6": [
    #        "The hot weather starts in the southwest on Friday, then moves in a northeasterly direction to the northeast of the region by Sunday. ",
    #        "Warm Weather moving from the south west through to the north east.",
    #        "A warm front moving over",
    #        "Warmer temperatures will push up through the country from the Southwest moving in a north-easterly direction over the course of the weekend.",
    #        "Hot (21-23) in the south-west, between 8 and 12 elsewhere on Friday. On Saturday it will be warmer (21-24) in central areas, averaging 12 on the periphery. On Sunday it will be between 10 and 14 everywhere except the north-west where it will be 20 or 21.",
    #        "Over the next three days a band of warm air, bringing temperatures in the 20s, will move from South West to north east. Otherwise cooler temperatures between 10-14 degrees, will dominate.",
    #        "Highs of 23 will start in the south west on Fri and move to the centre of the country on Sat and then the north east on Sunday. Outside the region of high temperature it will be 8 to 14.",
    #        "Cold everywhere on Friday apart from the south west corner where it could reach 23 degrees. Low temperatures everywhere else ranging fro 8 degrees in the north west to around 12 in inland areas in the north and south east.  Central areas very warm on Saturday with temperatures reaching as high as 24 with the rest of the country between 11 and 14 degrees. The warm pocket moves to the north east on Sunday with highs of 21 in from the coast.",
    #    ],
}

hypothesis_texts = {
    "1": [
        "temperatures will be cold in the country between friday and saturday",
        "temperatures will be cold in the country between friday and saturday",
    ],
    "2": [
        "temperatures will increase in the country between friday and sunday",
        "temperatures will increase in the country between friday and sunday",
        "temperatures will increase in the country between saturday and sunday",
        "temperatures will increase in the country between saturday and sunday",
        "temperatures will increase in the country between friday and saturday",
    ],
    "3": [
        "temperatures will increase in the not east between friday and sunday",
        "temperatures will increase in the north between friday and sunday",
    ],
}

# scores_for_each_hypothesis = {"1": [], "2": [], "3": []}
# for sequence_number, texts in hypothesis_texts.items():
#    for text in texts:
#        metrics = calculate_metrics(text, references[sequence_number])
#        scores_for_each_hypothesis[sequence_number].append(metrics)
#
# print(scores_for_each_hypothesis)
#
# score_averages_for_each_sequence = {}
# for sequence_number, scores in scores_for_each_hypothesis.items():
#    score_averages_for_each_sequence[sequence_number] = {
#        metric_name: statistics.fmean([x[metric_name] for x in scores])
#        for metric_name in scores[0]
#    }
#
# print(score_averages_for_each_sequence)
#
# figure = pyplot.figure()
# ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
# for sequence_number, scores in score_averages_for_each_sequence.items():
#    score_name = "rougeL-f1-med"
#    score = scores[score_name]
#    ax.bar(sequence_number, score)
#
# ax.set_title(f"Average {score_name} for each sequence")
# ax.set_xlabel("Sequence")
# ax.set_ylabel(score_name)
# ax.set_xticks([])
#
# pyplot.savefig(f"{score_name}.png")

pairwise_rouges = []
for text_a in references["1"]:
    for text_b in references["1"]:
        if text_a == text_b:
            continue
        metrics = calculate_metrics(text_a, [text_b])
        pairwise_rouges.append(metrics["rougeL-recall-max"])

        print(text_a)
        print(text_b)
        print(metrics["rougeL-recall-max"])
        print(metrics["rougeL-precision-max"])

mean_rouge = statistics.fmean(pairwise_rouges)
sd_rouge = statistics.stdev(pairwise_rouges)
print(f"mean: {mean_rouge}, sd: {sd_rouge}")
