from unittest.mock import Mock

from homer.codelets.selectors import GroupLabelSelector


def test_engender_follow_up():
    target_group = Mock()
    target_group.location = [0, 0, 0]
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.activation.as_scalar.side_effect = [0.6]
    challenger = Mock()
    challenger.activation.as_scalar.side_effect = [0.5]
    selector = GroupLabelSelector(
        Mock(), Mock(), Mock(), target_group, Mock(), Mock(), champion, challenger
    )
    follow_up = selector._engender_follow_up()
    assert GroupLabelSelector == type(follow_up)
