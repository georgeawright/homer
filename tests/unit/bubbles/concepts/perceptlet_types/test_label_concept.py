from unittest.mock import Mock, patch

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.codelets import BottomUpRawPerceptletLabeler
from homer.bubbles.concepts.perceptlet_types import LabelConcept
from homer.perceptlet_collection import PerceptletCollection


def test_spawn_codelet(target_perceptlet):
    with patch.object(
        PerceptletCollection, "get_unhappy", return_value=target_perceptlet
    ), patch.object(WorkspaceActivationPattern, "is_high", return_value=True):
        activation_pattern = WorkspaceActivationPattern(Mock())
        raw_perceptlets = PerceptletCollection()
        workspace = Mock()
        workspace.raw_perceptlets = raw_perceptlets
        bubble_chamber = Mock()
        bubble_chamber.workspace = workspace
        label_concept = LabelConcept()
        label_concept.activation_pattern = activation_pattern
        codelet = label_concept.spawn_codelet(bubble_chamber)
        assert BottomUpRawPerceptletLabeler == type(codelet)
