from unittest.mock import Mock, patch

from homer.codelets import RawPerceptletLabeler
from homer.perceptlet_collection import PerceptletCollection


def test_engender_follow_up(target_perceptlet):
    with patch.object(
        PerceptletCollection, "get_unhappy", return_value=target_perceptlet
    ):
        neighbours = PerceptletCollection()
        target_perceptlet.neighbours = neighbours
        codelet = RawPerceptletLabeler(
            Mock(), Mock(), Mock(), target_perceptlet, Mock(), Mock()
        )
        codelet.confidence = Mock()
        follow_up = codelet._engender_follow_up()
        assert RawPerceptletLabeler == type(follow_up)
