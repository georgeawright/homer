import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_types import CorrespondenceConcept
from homer.codelets.correspondence_suggester import CorrespondenceSuggester


def test_spawn_codelet():
    perceptlet_a = Mock()
    perceptlet_a.exigency = 0.5
    perceptlet_b = Mock()
    perceptlet_b.exigency = 0.5
    groups = [perceptlet_a, perceptlet_b]
    with patch.object(
        BubbleChamber, "get_random_groups", return_value=groups
    ), patch.object(random, "random", return_value=-1):
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), Mock(), Mock())
        correspondence_concept = CorrespondenceConcept()
        codelet = correspondence_concept.spawn_codelet(bubble_chamber)
        assert CorrespondenceSuggester == type(codelet)
