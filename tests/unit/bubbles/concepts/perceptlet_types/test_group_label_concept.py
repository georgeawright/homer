import random
from unittest.mock import Mock, patch

from homer.bubbles.concepts.perceptlet_types import GroupLabelConcept
from homer.codelets.group_labeler import GroupLabeler
from homer.perceptlet_collection import PerceptletCollection


def test_spawn_codelet(target_perceptlet):
    with patch.object(
        PerceptletCollection, "get_active", return_value=target_perceptlet
    ), patch.object(random, "random", return_value=-1):
        bubble_chamber = Mock()
        bubble_chamber.workspace.groups = PerceptletCollection()
        group_label_concept = GroupLabelConcept()
        codelet = group_label_concept.spawn_codelet(bubble_chamber)
        assert GroupLabeler == type(codelet)
