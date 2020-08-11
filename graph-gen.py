import random
import statistics
from collections import defaultdict

from matplotlib import pyplot


def pretend_answer_generator():
    answer = random.randint(1, 10)
    satisfaction = random.random()
    return {"answer": answer, "satisfaction": satisfaction}


def collect_stats(times_to_run: int):
    answer_satisfactions = defaultdict(list)
    for i in range(times_to_run):
        result = pretend_answer_generator()
        answer = result["answer"]
        satisfaction = result["satisfaction"]
        answer_satisfactions[answer].append(satisfaction)
    answer_statistics = [
        {
            "answer": answer,
            "frequency": len(satisfactions),
            "mean_satisfaction": statistics.mean(satisfactions),
            # "mean_satisfaction": statistics.fmean(satisfactions),
            # fmean would be better but requires v3.8
            "median_statisfaction": statistics.median(satisfactions),
            "satisfaction_sd": statistics.stdev(satisfactions),
        }
        for answer, satisfactions in answer_satisfactions.items()
    ]
    answer_statistics.sort(reverse=True, key=lambda e: e["frequency"])
    return answer_statistics


def chart_stats(list_of_answers):
    data = [answer["frequency"] for answer in list_of_answers]
    labels = [answer["answer"] for answer in list_of_answers]
    pyplot.xticks(range(len(data)), labels)
    pyplot.xlabel("Answer")
    pyplot.ylabel("Frequency")
    pyplot.title("Results")
    pyplot.bar(range(len(data)), data)
    pyplot.show()


def line_graph(data):
    x = [element[0] for element in data]
    y = [element[1] for element in data]
    pyplot.plot(x, y)
    pyplot.show()


# stats = collect_stats(100)
# chart_stats(stats)

# possibly add a scatter graph plotting satisfaction against frequency

data = [[0, 0], [1, 0.5], [2, 1.0], [3, 1.0], [4, 0.8], [5, 0.2], [6, 0]]
line_graph(data)
