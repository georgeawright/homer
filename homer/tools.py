import math
import statistics
from typing import Iterable, List, Union


def centroid_euclidean_distance(a, b) -> float:
    return math.dist(average_vector(a), average_vector(b))


def average_vector(vectors: List[List[Union[float, int]]]):
    return [
        statistics.fmean([vectors[j][i] for j in range(len(vectors))])
        for i in range(len(vectors[0]))
    ]


def add_vectors(a: list, b: list) -> list:
    # TODO
    pass


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


def correspond(a, b, view=None) -> bool:
    from homer.structure_collection import StructureCollection

    if a is None and b is None:
        return True
    view_members = StructureCollection() if view is None else view.members
    intersection = StructureCollection.intersection(
        a.correspondences, b.correspondences, view_members
    )
    return len(intersection) > 0


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


def arrange_text_fragments(fragments) -> dict:
    """Takes 2-3 text fragments and works out which is root, left branch, and right branch"""
    for potential_root in fragments:
        if not hasattr(potential_root, "left_branch"):
            continue
        potential_arrangement = {"root": potential_root}
        potential_members = [f for f in fragments if f != potential_root]
        if potential_root.left_branch in potential_members:
            potential_arrangement["left"] = potential_root.left_branch
        if potential_root.right_branch in potential_members:
            potential_arrangement["right"] = potential_root.right_branch
        if len(potential_arrangement) == len(fragments):
            if "left" not in potential_arrangement:
                potential_arrangement["left"] = None
            if "right" not in potential_arrangement:
                potential_arrangement["right"] = None
            return potential_arrangement
    if len(fragments) == 2:
        if (
            fragments[0].location.coordinates[-1][0] + 1
            == fragments[1].location.coordinates[0][0]
        ):
            return {"root": None, "left": fragments[0], "right": fragments[1]}
        if (
            fragments[1].location.coordinates[-1][0] + 1
            == fragments[0].location.coordinates[0][0]
        ):
            return {"root": None, "left": fragments[1], "right": fragments[0]}
    raise Exception("No acceptable arrangement")
