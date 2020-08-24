from unittest.mock import Mock

from homer.concept_space import ConceptSpace


def test_get_perceptlet_type_by_name():
    perceptlet_type = Mock()
    perceptlet_type.name = "label"
    concept_space = ConceptSpace(set(), {perceptlet_type}, set(), set(), set(), Mock())
    assert perceptlet_type == concept_space.get_perceptlet_type_by_name("label")
