from unittest.mock import Mock

from homer.perceptlet_collection import PerceptletCollection


def test_get_random():
    perceptlets = {Mock() for _ in range(10)}
    collection = PerceptletCollection(perceptlets)
    random_perceptlet = collection.get_random()
    assert random_perceptlet in perceptlets
