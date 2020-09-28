from unittest.mock import Mock, patch

from homer.codelets import TextletBuilder
from homer.perceptlet_collection import PerceptletCollection


def test_engender_follow_up(target_perceptlet):
    with patch.object(
        PerceptletCollection, "get_exigent", return_value=target_perceptlet
    ):
        groups = PerceptletCollection(Mock())
        workspace = Mock()
        workspace.groups = groups
        bubble_chamber = Mock()
        bubble_chamber.workspace = workspace
        textlet_builder = TextletBuilder(
            bubble_chamber, Mock(), target_perceptlet, Mock(), Mock()
        )
        textlet_builder.confidence = 1.0
        follow_up = textlet_builder._engender_follow_up()
        assert type(follow_up) == TextletBuilder
