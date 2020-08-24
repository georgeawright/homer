import random
from unittest.mock import Mock, patch

from homer.codelets.group_builder import GroupBuilder
from homer.bubbles.concepts.perceptlet_types import GroupConcept
from homer.perceptlet_collection import PerceptletCollection


def test_spawn_codelet(target_perceptlet):
    with patch.object(
        PerceptletCollection, "get_active", return_value=target_perceptlet
    ), patch.object(random, "random", return_value=-1):
        bubble_chamber = Mock()
        bubble_chamber.workspace.raw_perceptlets = PerceptletCollection()
        group_concept = GroupConcept()
        codelet = group_concept.spawn_codelet(bubble_chamber)
        assert GroupBuilder == type(codelet)
