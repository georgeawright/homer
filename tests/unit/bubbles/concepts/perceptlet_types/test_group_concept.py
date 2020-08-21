import random
from unittest.mock import Mock, patch

from homer.codelets.group_builder import GroupBuilder
from homer.bubbles.concepts.perceptlet_types import GroupConcept
from homer.perceptlet_collection import PerceptletCollection


def test_spawn_codelet():
    perceptlet = Mock()
    perceptlet.exigency = 0.5
    with patch.object(
        PerceptletCollection, "get_important", return_value=perceptlet
    ), patch.object(random, "random", return_value=-1):
        raw_perceptlets = PerceptletCollection()
        workspace = Mock()
        workspace.raw_perceptlets = raw_perceptlets
        bubble_chamber = Mock()
        bubble_chamber.workspace = workspace
        group_concept = GroupConcept()
        codelet = group_concept.spawn_codelet(bubble_chamber)
        assert GroupBuilder == type(codelet)
