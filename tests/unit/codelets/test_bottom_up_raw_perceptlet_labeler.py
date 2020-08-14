from unittest.mock import Mock, patch

from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.codelets.raw_perceptlet_labeler import RawPerceptletLabeler
from homer.concepts.perceptlet_type import PerceptletType
from homer.perceptlet_collection import PerceptletCollection


def test_engender_follow_up():
    bottom_up_raw_perceptlet_labeler = BottomUpRawPerceptletLabeler(
        Mock(), Mock(), Mock(), Mock(), Mock()
    )
    bottom_up_raw_perceptlet_labeler.parent_concept = Mock()
    bottom_up_raw_perceptlet_labeler.confidence = Mock()
    follow_up = bottom_up_raw_perceptlet_labeler._engender_follow_up()
    assert RawPerceptletLabeler == type(follow_up)


def test_engender_alternative_follow_up():
    raw_perceptlet = Mock()
    with patch.object(
        PerceptletCollection, "get_unhappy", return_value=raw_perceptlet
    ), patch.object(PerceptletType, "get_activation", return_value=1):
        raw_perceptlets = PerceptletCollection
        workspace = Mock()
        workspace.raw_perceptlets = raw_perceptlets
        bubble_chamber = Mock()
        bubble_chamber.workspace = workspace
        perceptlet_type = PerceptletType("name", 1)
        bottom_up_raw_perceptlet_labeler = BottomUpRawPerceptletLabeler(
            bubble_chamber, perceptlet_type, raw_perceptlet, 1, Mock()
        )
        alternative_follow_up = (
            bottom_up_raw_perceptlet_labeler._engender_alternative_follow_up()
        )
        assert BottomUpRawPerceptletLabeler == type(alternative_follow_up)
