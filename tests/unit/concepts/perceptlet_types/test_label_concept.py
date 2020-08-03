import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.concepts.perceptlet_types.label_concept import LabelConcept


def test_spawn_codelet():
    perceptlet = Mock()
    perceptlet.exigency = 0.5
    with patch.object(
        BubbleChamber, "get_raw_perceptlet", return_value=perceptlet
    ), patch.object(random, "random", return_value=-1):
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), Mock())
        label_concept = LabelConcept()
        codelet = label_concept.spawn_codelet(bubble_chamber)
        assert BottomUpRawPerceptletLabeler == type(codelet)
