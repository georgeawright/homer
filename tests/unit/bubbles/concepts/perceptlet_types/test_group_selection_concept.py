import random
from unittest.mock import Mock, patch

from homer.activation_patterns import WorkspaceActivationPattern
from homer.bubbles.concepts.perceptlet_types import GroupSelectionConcept
from homer.codelets.selectors import GroupSelector
from homer.perceptlet_collection import PerceptletCollection


def test_spawn_codelet():
    champion = Mock()
    champion.location = [0, 0, 0]
    with patch.object(random, "random", return_value=-1), patch.object(
        PerceptletCollection, "get_most_active", return_value=champion
    ):
        at = PerceptletCollection()
        with patch.object(
            WorkspaceActivationPattern, "get_high_location", return_value=Mock()
        ), patch.object(
            WorkspaceActivationPattern, "at", return_value=Mock()
        ), patch.object(
            PerceptletCollection, "at", return_value=at
        ):
            bubble_chamber = Mock()
            bubble_chamber.workspace.groups = PerceptletCollection()
            group_concept = GroupSelectionConcept()
            codelet = group_concept.spawn_codelet(bubble_chamber)
            assert GroupSelector == type(codelet)
