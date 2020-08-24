from unittest.mock import Mock, patch

from homer.activation_patterns import WorkspaceActivationPattern
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets import BottomUpRawPerceptletLabeler
from homer.codelets import RawPerceptletLabeler
from homer.perceptlet_collection import PerceptletCollection


def test_engender_follow_up(target_perceptlet):
    with patch.object(
        PerceptletCollection, "get_unhappy", return_value=target_perceptlet
    ):
        target_perceptlet.neighbours = PerceptletCollection()
        bottom_up_raw_perceptlet_labeler = BottomUpRawPerceptletLabeler(
            Mock(), Mock(), target_perceptlet, Mock(), Mock()
        )
        bottom_up_raw_perceptlet_labeler.parent_concept = Mock()
        bottom_up_raw_perceptlet_labeler.confidence = Mock()
        follow_up = bottom_up_raw_perceptlet_labeler._engender_follow_up()
        assert RawPerceptletLabeler == type(follow_up)


def test_engender_alternative_follow_up(target_perceptlet):
    with patch.object(
        PerceptletCollection, "get_unhappy", return_value=target_perceptlet
    ), patch.object(WorkspaceActivationPattern, "at", return_value=1):
        raw_perceptlets = PerceptletCollection
        bubble_chamber = Mock()
        bubble_chamber.workspace.raw_perceptlets = raw_perceptlets
        activation_pattern = WorkspaceActivationPattern(Mock())
        perceptlet_type = PerceptletType("name", 1)
        perceptlet_type.activation = activation_pattern
        bottom_up_raw_perceptlet_labeler = BottomUpRawPerceptletLabeler(
            bubble_chamber, perceptlet_type, target_perceptlet, 1, Mock()
        )
        alternative_follow_up = (
            bottom_up_raw_perceptlet_labeler._engender_alternative_follow_up()
        )
        assert BottomUpRawPerceptletLabeler == type(alternative_follow_up)
