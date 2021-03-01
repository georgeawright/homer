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


def areinstances(items: Iterable, t: type) -> bool:
    for item in items:
        if not isinstance(item, t):
            return False
    return True


def project_item_into_space(item: "Structure", space: "Space"):
    from homer.location import Location

    item.locations.append(
        Location(getattr(item, space.parent_concept.relevant_value), space)
    )
    space.add(item)


def equivalent_space(structure, space):
    for location in structure.locations:
        if location is None:
            continue
        if location.space.parent_concept == space.parent_concept:
            return location.space
    raise Exception(
        f"{structure.structure_id} does not exist "
        + f"in any space equivalent to {space.structure_id}"
    )
