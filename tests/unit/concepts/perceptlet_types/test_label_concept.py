import random
from unittest.mock import Mock, patch

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)
from homer.bubble_chamber import BubbleChamber
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.concepts.perceptlet_types.label_concept import LabelConcept


def test_spawn_codelet():
    perceptlet = Mock()
    perceptlet.exigency = 0.5
    with patch.object(
        BubbleChamber, "get_unhappy_raw_perceptlet", return_value=perceptlet
    ), patch.object(WorkspaceActivationPattern, "is_high", return_value=True):
        activation_pattern = WorkspaceActivationPattern(Mock())
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), Mock(), Mock())
        label_concept = LabelConcept()
        label_concept.activation_pattern = activation_pattern
        codelet = label_concept.spawn_codelet(bubble_chamber)
        assert BottomUpRawPerceptletLabeler == type(codelet)
