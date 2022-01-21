import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.correspondence_builders import (
    PotentialSubFrameToFrameCorrespondenceBuilder,
)


def test_fizzles_when_target_view_cannot_accept_it(bubble_chamber):
    target_view = Mock()
    target_view.can_accept_member.return_value = False

    target_structures = {
        "target_view": target_view,
        "target_space_one": Mock(),
        "target_space_two": Mock(),
        "target_structure_one": Mock(),
        "target_structure_two": Mock(),
        "target_conceptual_space": Mock(),
        "parent_concept": Mock(),
    }

    correspondence_builder = PotentialSubFrameToFrameCorrespondenceBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, 1
    )
    result = correspondence_builder.run()
    assert CodeletResult.FIZZLE == result
    assert correspondence_builder.child_structures is None


def test_builds_correspondence_when_view_can_accept_it(bubble_chamber):
    input_space = Mock()

    target_view = Mock()
    target_view.input_spaces = bubble_chamber.new_structure_collection(input_space)
    target_view.frames = bubble_chamber.new_structure_collection(Mock())
    target_view.can_accept_member.return_value = True

    sub_view = Mock()
    sub_view.frames = bubble_chamber.new_structure_collection(Mock())
    sub_view.members = bubble_chamber.new_structure_collection()

    target_structure_one_correspondence = Mock()
    target_structure_one_correspondence.parent_view = sub_view
    sub_view.members.add(target_structure_one_correspondence)

    target_structure_one = Mock()
    target_structure_one.correspondences = bubble_chamber.new_structure_collection(
        target_structure_one_correspondence
    )
    target_structure_one_correspondence.end = target_structure_one
    target_structure_one_correspondence.start.parent_space = input_space

    target_structure_two = Mock()
    target_structure_two.is_link = False

    target_structures = {
        "target_view": target_view,
        "target_space_one": Mock(),
        "target_space_two": Mock(),
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": Mock(),
        "parent_concept": Mock(),
    }

    correspondence_builder = PotentialSubFrameToFrameCorrespondenceBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, 1
    )
    result = correspondence_builder.run()
    assert CodeletResult.FINISH == result
    assert 2 == len(correspondence_builder.child_structures)


def test_fills_in_target_structure_two_parent_concept(bubble_chamber):
    input_space = Mock()

    target_view = Mock()
    target_view.input_spaces = bubble_chamber.new_structure_collection(input_space)
    target_view.frames = bubble_chamber.new_structure_collection(Mock())
    target_view.can_accept_member.return_value = True

    sub_view = Mock()
    sub_view.frames = bubble_chamber.new_structure_collection(Mock())
    sub_view.members = bubble_chamber.new_structure_collection()

    target_structure_one_correspondence = Mock()
    target_structure_one_correspondence.parent_view = sub_view
    sub_view.members.add(target_structure_one_correspondence)

    target_structure_one = Mock()
    target_structure_one.correspondences = bubble_chamber.new_structure_collection(
        target_structure_one_correspondence
    )
    target_structure_one_correspondence.end = target_structure_one
    target_structure_one_correspondence.start.parent_space = input_space

    target_structure_two = Mock()
    target_structure_two.is_link = True
    target_structure_two.parent_concept.is_filled_in = False

    target_structures = {
        "target_view": target_view,
        "target_space_one": Mock(),
        "target_space_two": Mock(),
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": Mock(),
        "parent_concept": Mock(),
    }

    correspondence_builder = PotentialSubFrameToFrameCorrespondenceBuilder(
        Mock(), Mock(), bubble_chamber, target_structures, 1
    )
    result = correspondence_builder.run()
    assert CodeletResult.FINISH == result
    assert 3 == len(correspondence_builder.child_structures)
