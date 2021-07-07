from unittest.mock import Mock

from homer.structure_collection import StructureCollection
from homer.structures import Node


def test_nearby():
    space_1 = Mock()
    space_1_object_location = Mock()
    space_1_object_location.space = space_1
    space_1_object = Node(
        Mock(),
        Mock(),
        [space_1_object_location],
        space_1,
        Mock(),
        Mock(),
        Mock(),
    )
    space_1_contents_of_type = Mock()
    space_1_contents_of_type.near.return_value = StructureCollection({space_1_object})
    space_1.contents.of_type.return_value = space_1_contents_of_type
    space_2 = Mock()
    space_2_object_location = Mock()
    space_2_object_location.space = space_2
    space_2_object = Node(
        Mock(),
        Mock(),
        [space_2_object_location],
        space_2,
        Mock(),
        Mock(),
        Mock(),
    )
    space_2_contents_of_type = Mock()
    space_2_contents_of_type.near.return_value = StructureCollection(
        {space_2_object, space_1_object}
    )
    space_2.contents.of_type.return_value = space_2_contents_of_type
    node = Node(
        Mock(),
        Mock(),
        [space_1_object_location, space_2_object_location],
        space_1,
        Mock(),
        Mock(),
        Mock(),
    )
    assert space_1_object in node.nearby()
    assert space_2_object in node.nearby()
    assert space_1_object in node.nearby(space_1)
    assert space_2_object not in node.nearby(space_1)
    assert space_1_object in node.nearby(space_2)
    assert space_2_object in node.nearby(space_2)
