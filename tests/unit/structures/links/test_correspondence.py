import pytest
from unittest.mock import Mock

from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Correspondence


def test_node_pairs(bubble_chamber):
    start_node_1 = Mock()
    start_node_1.is_node = True
    start_node_2 = Mock()
    start_node_2.is_node = True
    end_node_1 = Mock()
    end_node_1.is_node = True
    end_node_2 = Mock()
    end_node_2.is_node = True

    start_label = Mock()
    start_label.is_node = False
    start_label.is_label = True
    start_label.start = start_node_1
    end_label = Mock()
    end_label.is_node = False
    end_label.is_label = True
    end_label.start = end_node_1

    start_relation = Mock()
    start_relation.is_node = False
    start_relation.is_label = False
    start_relation.start = start_node_1
    start_relation.end = start_node_2
    end_relation = Mock()
    end_relation.is_node = False
    end_relation.is_label = False
    end_relation.start = end_node_1
    end_relation.end = end_node_2

    node_correspondence = Correspondence(
        "",
        "",
        start_node_1,
        end_node_1,
        bubble_chamber.new_structure_collection(start_node_1, end_node_1),
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert [(start_node_1, end_node_1)] == node_correspondence.node_pairs
    label_correspondence = Correspondence(
        "",
        "",
        start_label,
        end_label,
        bubble_chamber.new_structure_collection(start_label, end_label),
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert [(start_node_1, end_node_1)] == label_correspondence.node_pairs
    relation_correspondence = Correspondence(
        "",
        "",
        start_relation,
        end_relation,
        bubble_chamber.new_structure_collection(start_relation, end_relation),
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    assert [
        (start_node_1, end_node_1),
        (start_node_2, end_node_2),
    ] == relation_correspondence.node_pairs


def test_copy(bubble_chamber):
    start_space = Mock()
    start_space.parent_concept = Mock()
    end_space = Mock()
    end_space.parent_concept = Mock()
    start_location = Mock()
    start_location.coordinates = [1, 1]
    start_location.space = start_space
    end_location = Mock()
    end_location.coordinates = [1, 1]
    end_location.space = end_space
    old_start = Mock()
    old_start.location_in_space.return_value = start_location
    old_start.locations = [start_location]
    old_end = Mock()
    old_end.location_in_space.return_value = end_location
    old_end.locations = [end_location]
    new_start = Mock()
    new_start.location_in_space.return_value = start_location
    new_start.locations = [start_location]
    new_end = Mock()
    new_end.location_in_space.return_value = end_location
    new_end.locations = [end_location]
    parent_id = "id"
    location = Mock()
    location.space.sub_spaces = [start_space, end_space]
    correspondence = Correspondence(
        Mock(),
        Mock(),
        old_start,
        old_end,
        bubble_chamber.new_structure_collection(old_start, old_end),
        [start_location, end_location],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    copy = correspondence.copy(
        old_arg=old_start,
        new_arg=new_start,
        parent_id=parent_id,
        bubble_chamber=bubble_chamber,
    )
    assert correspondence.start == old_start
    assert correspondence.end == old_end
    assert copy.start == new_start
    assert copy.end == old_end
    assert copy.parent_id == parent_id
    copy = correspondence.copy(
        old_arg=old_end,
        new_arg=new_end,
        parent_id=parent_id,
        bubble_chamber=bubble_chamber,
    )
    assert correspondence.start == old_start
    assert correspondence.end == old_end
    assert copy.start == old_start
    assert copy.end == new_end
    assert copy.parent_id == parent_id


def test_nearby(bubble_chamber):
    start_space = Mock()
    end_space = Mock()

    start = Structure(
        "",
        "",
        [Location([], start_space)],
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    end = Structure(
        "",
        "",
        [Location([], end_space)],
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    other = Structure(
        "",
        "",
        [Location([], end_space)],
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )

    start_end_correspondence_1 = Correspondence(
        "1",
        "",
        start,
        end,
        bubble_chamber.new_structure_collection(start, end),
        [],
        Mock(),
        Mock(),
        Mock(),
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    start.links_out.add(start_end_correspondence_1)
    start.links_in.add(start_end_correspondence_1)
    end.links_out.add(start_end_correspondence_1)
    end.links_in.add(start_end_correspondence_1)
    start_end_correspondence_2 = Correspondence(
        "2",
        "",
        start,
        end,
        bubble_chamber.new_structure_collection(start, end),
        [],
        Mock(),
        Mock(),
        Mock(),
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    start.links_out.add(start_end_correspondence_2)
    start.links_in.add(start_end_correspondence_2)
    end.links_out.add(start_end_correspondence_2)
    end.links_in.add(start_end_correspondence_2)
    start_other_correspondence = Correspondence(
        "3",
        "",
        start,
        other,
        bubble_chamber.new_structure_collection(start, other),
        [],
        Mock(),
        Mock(),
        Mock(),
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    start.links_out.add(start_other_correspondence)
    start.links_in.add(start_other_correspondence)
    other.links_out.add(start_other_correspondence)
    other.links_in.add(start_other_correspondence)

    assert start_end_correspondence_1.nearby() == StructureCollection(
        Mock(), {start_other_correspondence}
    )
    assert start_end_correspondence_2.nearby() == StructureCollection(
        Mock(), {start_other_correspondence}
    )
    assert start_other_correspondence.nearby() == StructureCollection(
        Mock(), {start_end_correspondence_1, start_end_correspondence_2}
    )


def test_get_slot_argument_returns_slot(bubble_chamber):
    location = Mock()
    slot = Mock()
    slot.is_slot = True
    non_slot = Mock()
    non_slot.is_slot = False
    correspondence = Correspondence(
        Mock(),
        Mock(),
        slot,
        non_slot,
        bubble_chamber.new_structure_collection(slot, non_slot),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    assert slot == correspondence.slot_argument
    correspondence = Correspondence(
        Mock(),
        Mock(),
        non_slot,
        slot,
        bubble_chamber.new_structure_collection(non_slot, slot),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    assert slot == correspondence.slot_argument


def test_get_non_slot_argument_returns_non_slot(bubble_chamber):
    location = Mock()
    slot = Mock()
    slot.is_slot = True
    non_slot = Mock()
    non_slot.is_slot = False
    correspondence = Correspondence(
        Mock(),
        Mock(),
        slot,
        non_slot,
        bubble_chamber.new_structure_collection(slot, non_slot),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    assert non_slot == correspondence.non_slot_argument
    correspondence = Correspondence(
        Mock(),
        Mock(),
        non_slot,
        slot,
        bubble_chamber.new_structure_collection(non_slot, slot),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    assert non_slot == correspondence.non_slot_argument


def test_common_arguments_with(bubble_chamber):
    arg_1 = Mock()
    arg_2 = Mock()
    arg_3 = Mock()
    arg_4 = Mock()
    correspondence_1 = Correspondence(
        Mock(),
        Mock(),
        arg_1,
        arg_2,
        bubble_chamber.new_structure_collection(arg_1, arg_2),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    correspondence_2 = Correspondence(
        Mock(),
        Mock(),
        arg_1,
        arg_2,
        bubble_chamber.new_structure_collection(arg_1, arg_2),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    correspondence_3 = Correspondence(
        Mock(),
        Mock(),
        arg_1,
        arg_3,
        bubble_chamber.new_structure_collection(arg_1, arg_3),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    correspondence_4 = Correspondence(
        Mock(),
        Mock(),
        arg_2,
        arg_3,
        bubble_chamber.new_structure_collection(arg_2, arg_3),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    correspondence_5 = Correspondence(
        Mock(),
        Mock(),
        arg_3,
        arg_4,
        bubble_chamber.new_structure_collection(arg_3, arg_4),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    assert 2 == len(correspondence_1.common_arguments_with(correspondence_2))
    assert 1 == len(correspondence_1.common_arguments_with(correspondence_3))
    assert 1 == len(correspondence_1.common_arguments_with(correspondence_4))
    assert 0 == len(correspondence_1.common_arguments_with(correspondence_5))
