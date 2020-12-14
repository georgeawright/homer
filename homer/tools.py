import statistics
from typing import Iterable, List, Union


def average_vector(vectors: List[List[Union[float, int]]]):
    return [
        statistics.fmean([vectors[j][i] for j in range(len(vectors))])
        for i in range(len(vectors[0]))
    ]


def first_key_of_dict(dictionary: dict):
    try:
        return min(int(k) for k in dictionary.keys())
    except ValueError:
        return None


def last_value_of_dict(dictionary: dict):
    try:
        return dictionary[str(max(int(k) for k in dictionary.keys()))]
    except ValueError:
        return None


def hasinstance(items: Iterable, t: type) -> bool:
    for item in items:
        if isinstance(item, t):
            return True
    return False
