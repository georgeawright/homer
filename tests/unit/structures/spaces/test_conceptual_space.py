import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.spaces import ConceptualSpace, WorkingSpace


def test_instance_returns_working_space():
    conceptual_space = ConceptualSpace(
        "id", "", "name", Mock(), [Mock()], Mock(), 0, [], []
    )
    instance = conceptual_space.instance_in_space(None, name="")
    assert isinstance(instance, WorkingSpace)


def test_instance_returns_working_space_with_working_sub_spaces():
    parent_space = Mock()
    parent_space.name = "parent"
    sub_space = ConceptualSpace("sub", "", "sub", Mock(), [Mock()], Mock(), 1, [], [])
    super_space = ConceptualSpace(
        "super",
        [],
        "super",
        Mock(),
        [Mock()],
        Mock(),
        2,
        [sub_space, Mock()],
        [sub_space, Mock()],
    )
    super_instance = super_space.instance_in_space(parent_space)
    assert isinstance(super_instance, WorkingSpace)
    assert "super IN parent" == super_instance.name
    assert len(super_space.sub_spaces) == len(super_instance.sub_spaces)
    sub_instance = super_instance.sub_spaces[0]
    assert isinstance(sub_instance, WorkingSpace)
    assert "sub IN parent" == sub_instance.name


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
        "",
        "",
        "name",
        Mock(),
        Mock(),
        StructureCollection({concept_1, concept_2, concept_3}),
        Mock(),
        Mock(),
        Mock(),
    )
    conceptual_space.update_activation()
    assert expected_activation == conceptual_space.activation
