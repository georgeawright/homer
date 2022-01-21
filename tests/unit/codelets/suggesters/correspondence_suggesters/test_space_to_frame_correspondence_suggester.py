from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.suggesters.correspondence_suggesters import (
    SpaceToFrameCorrespondenceSuggester,
)


def test_fizzles_if_view_cannot_accept_correspondence(bubble_chamber):
    target_view = Mock()
    target_view.can_accept_member.return_value = False

    target_structure_one = Mock()

    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
    }

    correspondence_suggester = SpaceToFrameCorrespondenceSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    correspondence_suggester.run()
    assert CodeletResult.FIZZLE == correspondence_suggester.result


def test_gets_second_target_structure_if_needed(bubble_chamber):
    target_view = Mock()
    target_view.can_accept_member.return_value = True

    target_structure_one = Mock()

    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
    }

    correspondence_suggester = SpaceToFrameCorrespondenceSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    assert correspondence_suggester.target_space_two is None
    assert correspondence_suggester.target_structure_two is None
    correspondence_suggester.run()
    assert correspondence_suggester.target_space_two is not None
    assert correspondence_suggester.target_structure_two is not None
    assert CodeletResult.FINISH == correspondence_suggester.result


def test_gets_parent_concept_if_needed(bubble_chamber):
    target_view = Mock()
    target_view.can_accept_member.return_value = True

    target_structure_one = Mock()

    target_structures = {
        "target_view": target_view,
        "target_structure_one": target_structure_one,
    }

    correspondence_suggester = SpaceToFrameCorrespondenceSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, Mock()
    )
    assert correspondence_suggester.parent_concept is None
    correspondence_suggester.run()
    assert correspondence_suggester.parent_concept is not None
    assert CodeletResult.FINISH == correspondence_suggester.result
