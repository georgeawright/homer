import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.spaces import ConceptualSpace, WorkingSpace


def test_instance_returns_working_space():
    conceptual_space = ConceptualSpace("name", Mock(), Mock())
    instance = conceptual_space.instance
    assert isinstance(instance, WorkingSpace)


@pytest.mark.parametrize(
    "activation_1, activation_2, activation_3, expected_activation",
    [(1.0, 1.0, 1.0, 1.0), (0.5, 0.2, 0.0, 0.5), (1.0, 0.0, 0.0, 1.0)],
)
def test_update_activation(
    activation_1, activation_2, activation_3, expected_activation
):
    concept_1 = Mock()
    concept_1.activation = activation_1
    concept_2 = Mock()
    concept_2.activation = activation_2
    concept_3 = Mock()
    concept_3.activation = activation_3
    conceptual_space = ConceptualSpace(
        "name", StructureCollection({concept_1, concept_2, concept_3}), Mock()
    )
    conceptual_space.update_activation()
    assert expected_activation == conceptual_space.activation
