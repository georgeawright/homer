import random
from unittest.mock import Mock, patch

from homer.activation_patterns import WorkspaceActivationPattern
from homer.bubbles.concepts.perceptlet_types import GroupLabelSelectionConcept
from homer.codelets.selectors import GroupLabelSelector
from homer.perceptlet_collection import PerceptletCollection
from homer.workspace_location import WorkspaceLocation


def test_spawn_codelet():
    target_group = Mock()
    target_group.location = [0, 0, 0]
    with patch.object(random, "random", return_value=-1), patch.object(
        PerceptletCollection, "get_active", return_value=target_group
    ):
        at = PerceptletCollection()
        with patch.object(PerceptletCollection, "at", return_value=at), patch.object(
            WorkspaceActivationPattern,
            "get_high_location",
            return_value=WorkspaceLocation(0, 0, 0),
        ):
            bubble_chamber = Mock()
            bubble_chamber.concept_space = {"group-label": Mock()}
            bubble_chamber.workspace.groups = PerceptletCollection()
            group_label_selection_concept = GroupLabelSelectionConcept()
            codelet = group_label_selection_concept.spawn_codelet(bubble_chamber)
            assert GroupLabelSelector == type(codelet)
