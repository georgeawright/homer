import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.suggesters.correspondence_suggesters import (
    PotentialSubFrameToFrameCorrespondenceSuggester,
)


def test_fizzles_if_view_cannot_accept_correspondence(bubble_chamber):
    frame_concept = Mock()

    sub_frame = Mock()
    sub_frame.parent_concept = frame_concept
    sub_frame.input_space.corresponding_exigency = 1.0
    sub_frame.output_space.corresponding_exigency = 0.0
    sub_view = Mock()
    sub_view.parent_frame = sub_frame
    sub_view.activation = 1.0
    sub_view.exigency = 1.0
    bubble_chamber.production_views = bubble_chamber.new_structure_collection(sub_view)

    target_view = Mock()
    target_view.matched_sub_frames = {}
    parent_sub_frame = Mock()
    parent_sub_frame.corresponding_exigency = 1.0
    parent_sub_frame.parent_concept = frame_concept
    target_view.parent_frame.sub_frames = bubble_chamber.new_structure_collection(
        parent_sub_frame
    )
    target_view.can_accept_member.return_value = False

    target_structure_one = Mock()

    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
    }

    correspondence_suggester = PotentialSubFrameToFrameCorrespondenceSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    correspondence_suggester.run()
    assert CodeletResult.FIZZLE == correspondence_suggester.result


def test_gets_second_target_structure_if_needed(bubble_chamber):
    frame_concept = Mock()

    sub_frame = Mock()
    sub_frame.parent_concept = frame_concept
    sub_frame.input_space.corresponding_exigency = 1.0
    sub_frame.output_space.corresponding_exigency = 0.0
    sub_view = Mock()
    sub_view.parent_frame = sub_frame
    sub_view.activation = 1.0
    bubble_chamber.production_views = bubble_chamber.new_structure_collection(sub_view)

    target_view = Mock()
    target_view.matched_sub_frames = {}
    parent_sub_frame = Mock()
    parent_sub_frame.corresponding_exigency = 1.0
    parent_sub_frame.parent_concept = frame_concept
    target_view.parent_frame.sub_frames = bubble_chamber.new_structure_collection(
        parent_sub_frame
    )
    target_view.can_accept_member.return_value = True

    target_structure_one = Mock()

    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
    }

    correspondence_suggester = PotentialSubFrameToFrameCorrespondenceSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    assert correspondence_suggester.target_space_two is None
    assert correspondence_suggester.target_structure_two is None
    correspondence_suggester.run()
    assert correspondence_suggester.target_space_two is not None
    assert correspondence_suggester.target_structure_two is not None
    assert CodeletResult.FINISH == correspondence_suggester.result


def test_gets_parent_concept_if_needed(bubble_chamber):
    frame_concept = Mock()

    sub_frame = Mock()
    sub_frame.parent_concept = frame_concept
    sub_frame.input_space.corresponding_exigency = 1.0
    sub_frame.output_space.corresponding_exigency = 0.0
    sub_view = Mock()
    sub_view.parent_frame = sub_frame
    sub_view.activation = 1.0
    bubble_chamber.production_views = bubble_chamber.new_structure_collection(sub_view)

    target_view = Mock()
    target_view.matched_sub_frames = {}
    parent_sub_frame = Mock()
    parent_sub_frame.corresponding_exigency = 1.0
    parent_sub_frame.parent_concept = frame_concept
    target_view.parent_frame.sub_frames = bubble_chamber.new_structure_collection(
        parent_sub_frame
    )
    target_view.can_accept_member.return_value = True

    target_structure_one = Mock()

    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
    }

    correspondence_suggester = PotentialSubFrameToFrameCorrespondenceSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    assert correspondence_suggester.parent_concept is None
    correspondence_suggester.run()
    assert correspondence_suggester.parent_concept is not None
    assert CodeletResult.FINISH == correspondence_suggester.result
