from unittest.mock import Mock

from homer.codelets import GroupExtender, TopDownGroupLabeler


def test_engender_follow_up(target_perceptlet):
    codelet = TopDownGroupLabeler(
        Mock(), Mock(), Mock(), target_perceptlet, Mock(), Mock()
    )
    codelet.confidence = Mock()
    follow_up = codelet._engender_follow_up()
    assert GroupExtender == type(follow_up)
