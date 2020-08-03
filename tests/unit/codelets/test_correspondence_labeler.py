from unittest.mock import Mock

from homer.codelets.correspondence_builder import CorrespondenceBuilder
from homer.codelets.correspondence_labeler import CorrespondenceLabeler


def test_engender_follow_up():
    correspondence_labeler = CorrespondenceLabeler(Mock(), Mock(), Mock(), Mock())
    follow_up = correspondence_labeler._engender_follow_up(Mock())
    assert CorrespondenceBuilder == type(follow_up)
