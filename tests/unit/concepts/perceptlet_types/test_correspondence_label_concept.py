import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelets.correspondence_labeler import CorrespondenceLabeler
from homer.concepts.perceptlet_types.correspondence_label_concept import (
    CorrespondenceLabelConcept,
)


def test_spawn_codelet():
    correspondence = Mock()
    correspondence.exigency = 0.5
    with patch.object(
        BubbleChamber, "get_random_correspondence", return_value=correspondence
    ), patch.object(random, "random", return_value=-1):
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), Mock(), Mock())
        correspondence_label_concept = CorrespondenceLabelConcept()
        codelet = correspondence_label_concept.spawn_codelet(bubble_chamber)
        assert CorrespondenceLabeler == type(codelet)
