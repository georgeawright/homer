from unittest.mock import Mock

from homer.codelets import CorrespondenceBuilder, CorrespondenceLabeler


def test_engender_follow_up(target_perceptlet):
    correspondence_builder = CorrespondenceBuilder(
        Mock(), Mock(), Mock(), target_perceptlet, target_perceptlet, Mock(), Mock()
    )
    correspondence_builder.correspondence = target_perceptlet
    correspondence_builder.confidence = Mock()
    follow_up = correspondence_builder._engender_follow_up()
    assert CorrespondenceLabeler == type(follow_up)
