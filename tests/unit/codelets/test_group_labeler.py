from unittest.mock import Mock

from homer.codelets import GroupExtender, GroupLabeler


def test_engender_follow_up(target_perceptlet):
    codelet = GroupLabeler(Mock(), Mock(), target_perceptlet, Mock(), Mock())
    codelet.confidence = Mock()
    follow_up = codelet._engender_follow_up()
    assert GroupExtender == type(follow_up)


def test_engender_alternative_follow_up(target_perceptlet):
    codelet = GroupLabeler(Mock(), Mock(), target_perceptlet, 1, Mock())
    follow_up = codelet._engender_alternative_follow_up()
    assert GroupLabeler == type(follow_up)
