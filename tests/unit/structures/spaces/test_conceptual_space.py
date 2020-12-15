import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.spaces import ConceptualSpace, WorkingSpace


def test_instance_returns_working_space():
    conceptual_space = ConceptualSpace("id", Mock(), "name", Mock(), Mock())
    instance = conceptual_space.instance
    assert isinstance(instance, WorkingSpace)


def test_instance_returns_working_space_with_working_sub_spaces():
    super_space = ConceptualSpace("super", Mock(), "super", Mock(), Mock())
    sub_space = ConceptualSpace("sub", Mock(), "sub", Mock(), Mock())
    super_space.sub_spaces.add(sub_space)
    super_instance = super_space.instance
    assert isinstance(super_instance, WorkingSpace)
    assert "super working" == super_instance.name
    assert 1 == len(super_instance.sub_spaces)
    sub_instance = super_instance.sub_spaces.get_random()
    assert isinstance(sub_instance, WorkingSpace)
    assert "sub working" == sub_instance.name


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
        Mock(),
        Mock(),
        "name",
        StructureCollection({concept_1, concept_2, concept_3}),
        Mock(),
    )
    conceptual_space.update_activation()
    assert expected_activation == conceptual_space.activation
