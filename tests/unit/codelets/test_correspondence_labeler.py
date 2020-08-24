from unittest.mock import Mock

from homer.codelets import CorrespondenceBuilder, CorrespondenceLabeler


def test_engender_follow_up(target_perceptlet):
    target_perceptlet.first_argument.location = [0, 0, 0]
    target_perceptlet.second_argument.location = [0, 0, 0]
    correspondence_labeler = CorrespondenceLabeler(
        Mock(), Mock(), Mock(), target_perceptlet, Mock(), Mock()
    )
    correspondence_labeler.confidence = Mock()
    follow_up = correspondence_labeler._engender_follow_up()
    assert CorrespondenceBuilder == type(follow_up)
