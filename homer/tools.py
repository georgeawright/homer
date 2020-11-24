import statistics
from typing import List, Union


def average_vector(vectors: List[List[Union[float, int]]]):
    return [
        statistics.fmean([vectors[j][i] for j in range(len(vectors))])
        for i in range(len(vectors[0]))
    ]
