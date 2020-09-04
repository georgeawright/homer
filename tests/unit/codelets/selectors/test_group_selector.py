from unittest.mock import Mock

from homer.codelets.selectors import GroupSelector

FLOAT_COMPARISON_TOLERANCE = 1e-3


def test_engender_follow_up():
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.activation.as_scalar.side_effect = [0.6]
    challenger = Mock()
    challenger.activation.as_scalar.side_effect = [0.5]
    selector = GroupSelector(
        Mock(), Mock(), Mock(), champion, Mock(), Mock(), challenger
    )
    follow_up = selector._engender_follow_up()
    assert GroupSelector == type(follow_up)
