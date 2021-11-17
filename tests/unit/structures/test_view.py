from unittest.mock import Mock

from homer.structures import View


def test_add(bubble_chamber):
    view = View(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(Mock(), Mock()),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    node_1 = Mock()
    node_2 = Mock()
    correspondence = Mock()
    correspondence.node_pairs = [(node_1, node_2)]

    assert view.members.is_empty()
    assert [] == view.input_node_pairs

    view.add(correspondence)
    assert correspondence in view.members
    assert [(node_1, node_2)] == view.input_node_pairs


def test_can_accept_member(bubble_chamber):
    view = View(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(Mock(), Mock()),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )

    node_1 = Mock()
    node_2 = Mock()
    node_3 = Mock()
    node_4 = Mock()

    correspondence_1 = Mock()
    correspondence_1.start = node_1
    correspondence_1.end = node_2
    correspondence_1.node_pairs = [(node_1, node_2)]
    node_2.correspondences = bubble_chamber.new_structure_collection()

    assert view.can_accept_member(correspondence_1)
    node_2.correspondences.add(correspondence_1)
    view.add(correspondence_1)

    correspondence_2 = Mock()
    correspondence_2.start = node_1
    correspondence_2.end = node_2
    correspondence_2.node_pairs = [(node_1, node_2)]

    assert not view.can_accept_member(correspondence_2)

    correspondence_3 = Mock()
    correspondence_3.start = node_1
    correspondence_3.end = node_4
    correspondence_3.node_pairs = [(node_1, node_4)]
    node_4.correspondences = bubble_chamber.new_structure_collection()

    assert not view.can_accept_member(correspondence_3)

    start_relation = Mock()
    end_relation = Mock()
    end_relation.correspondences = bubble_chamber.new_structure_collection()
    assert end_relation.correspondences.is_empty()
    correspondence_4 = Mock()
    correspondence_4.start = start_relation
    correspondence_4.end = end_relation
    correspondence_4.node_pairs = [(node_1, node_2), (node_3, node_4)]

    assert view.can_accept_member(correspondence_4)
