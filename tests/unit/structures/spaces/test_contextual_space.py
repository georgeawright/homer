import pytest
from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures.spaces import ContextualSpace


@pytest.mark.parametrize(
    "activation_1, activation_2, activation_3, expected_activation",
    [
        (1.0, 1.0, 1.0, 1.0),
        (0.5, 0.2, 0.0, 0.2),
        (1.0, 0.0, 0.0, 0.0),
        (1.0, 1.0, 0.0, 1.0),
    ],
)
def test_update_activation(
    activation_1, activation_2, activation_3, expected_activation
):
    structure_1 = Mock()
    structure_1.activation = activation_1
    structure_2 = Mock()
    structure_2.activation = activation_2
    structure_3 = Mock()
    structure_3.activation = activation_3
    contextual_space = ContextualSpace(
        Mock(),
        Mock(),
        "name",
        Mock(),
        StructureCollection({structure_1, structure_2, structure_3}),
    )
    contextual_space.update_activation()
    assert expected_activation == contextual_space.activation


def test_copy():
    node_1 = Mock()
    node_1.is_node = True
    node_2 = Mock()
    node_2.is_node = True
    label_1 = Mock()
    label_1.is_label = True
    label_2 = Mock()
    label_2.is_label = True
    relation_1 = Mock()
    relation_1.is_relation = True
    relation_1.start = node_1
    relation_1.end = node_2
    relation_2 = Mock()
    relation_2.is_relation = True
    relation_2.start = node_2
    relation_2.end = node_1
    node_1.labels = StructureCollection({label_1})
    node_1.links_out = StructureCollection({label_1, relation_1})
    node_1.links_in = StructureCollection({relation_2})
    node_2.labels = StructureCollection({label_2})
    node_2.links_out = StructureCollection({label_2, relation_2})
    node_2.links_in = StructureCollection({relation_1})
    space_contents = StructureCollection(
        {node_1, node_2, label_1, label_2, relation_1, relation_2}
    )
    space = ContextualSpace("", "", "", Mock(), space_contents, Mock())
    copied_space, copies = space.copy(bubble_chamber=Mock(), parent_id="")
    assert len(copied_space.contents) == len(space.contents)
    assert node_1 not in copied_space.contents
    assert node_2 not in copied_space.contents
    assert label_1 not in copied_space.contents
    assert label_2 not in copied_space.contents
    assert relation_1 not in copied_space.contents
    assert relation_2 not in copied_space.contents
    assert node_1 in copies
    assert node_2 in copies
    assert label_1 in copies
    assert label_2 in copies
    assert relation_1 in copies
    assert relation_2 in copies
