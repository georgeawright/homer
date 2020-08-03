from unittest.mock import Mock

from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.codelets.raw_perceptlet_labeler import RawPerceptletLabeler


def test_engender_follow_up():
    bottom_up_raw_perceptlet_labeler = BottomUpRawPerceptletLabeler(
        Mock(), Mock(), Mock(), Mock()
    )
    follow_up = bottom_up_raw_perceptlet_labeler._engender_follow_up(Mock(), Mock())
    assert RawPerceptletLabeler == type(follow_up)


def test_engender_alternative_follow_up():
    bottom_up_raw_perceptlet_labeler = BottomUpRawPerceptletLabeler(
        Mock(), Mock(), Mock(), Mock()
    )
    alternative_follow_up = bottom_up_raw_perceptlet_labeler._engender_alternative_follow_up(
        Mock()
    )
    assert BottomUpRawPerceptletLabeler == type(alternative_follow_up)
