import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_types import GroupLabelConcept
from homer.codelets.group_labeler import GroupLabeler


def test_spawn_codelet():
    group = Mock()
    group.exigency = 0.5
    with patch.object(
        BubbleChamber, "get_random_groups", return_value=[group]
    ), patch.object(random, "random", return_value=-1):
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), Mock(), Mock())
        group_label_concept = GroupLabelConcept()
        codelet = group_label_concept.spawn_codelet(bubble_chamber)
        assert GroupLabeler == type(codelet)
