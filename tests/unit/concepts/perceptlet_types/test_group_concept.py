import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelets.group_builder import GroupBuilder
from homer.concepts.perceptlet_types.group_concept import GroupConcept


def test_spawn_codelet():
    perceptlet = Mock()
    perceptlet.exigency = 0.5
    with patch.object(
        BubbleChamber, "get_raw_perceptlet", return_value=perceptlet
    ), patch.object(random, "random", return_value=-1):
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), Mock())
        group_concept = GroupConcept()
        codelet = group_concept.spawn_codelet(bubble_chamber)
        assert GroupBuilder == type(codelet)
