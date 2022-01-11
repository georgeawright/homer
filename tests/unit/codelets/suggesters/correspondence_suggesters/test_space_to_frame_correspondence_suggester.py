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


def test_gets_second_target_structure_if_needed():
    pass


def test_gets_parent_concept_if_needed():
    pass
