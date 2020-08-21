from unittest.mock import Mock

from homer.codelets import CorrespondenceBuilder, CorrespondenceLabeler


def test_engender_follow_up():
    correspondence_labeler = CorrespondenceLabeler(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_labeler.confidence = Mock()
    follow_up = correspondence_labeler._engender_follow_up()
    assert CorrespondenceBuilder == type(follow_up)
