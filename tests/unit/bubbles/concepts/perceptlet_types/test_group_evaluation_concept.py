import random
from unittest.mock import Mock, patch

from homer.activation_patterns import WorkspaceActivationPattern
from homer.bubbles.concepts.perceptlet_types import GroupEvaluationConcept
from homer.codelets.evaluators import GroupEvaluator
from homer.perceptlet_collection import PerceptletCollection


def test_spawn_codelet():
    champion = Mock()
    champion.location = [0, 0, 0]
    challenger = Mock()
    with patch.object(random, "random", return_value=-1), patch.object(
        PerceptletCollection, "get_active", return_value=champion
    ), patch.object(PerceptletCollection, "get_random", return_value=challenger):
        at = PerceptletCollection()
        with patch.object(
            WorkspaceActivationPattern, "get_high_location", return_value=Mock()
        ), patch.object(PerceptletCollection, "at", return_value=at):
            bubble_chamber = Mock()
            bubble_chamber.workspace.groups = PerceptletCollection()
            group_concept = GroupEvaluationConcept()
            codelet = group_concept.spawn_codelet(bubble_chamber)
            assert GroupEvaluator == type(codelet)
