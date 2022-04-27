import pytest
from unittest.mock import Mock

from linguoplotter.codelets.evaluators import LabelEvaluator
from linguoplotter.codelets.selectors import LabelSelector


@pytest.mark.parametrize("current_quality, classification", [(0.75, 0.5), (0.5, 0.75)])
def test_changes_target_structure_quality(
    bubble_chamber, current_quality, classification
):
    concept = Mock()
    concept.classifier.classify.return_value = classification
    label = Mock()
    label.start.is_label = False
    label.labels = bubble_chamber.new_structure_collection()
    label.quality = current_quality
    label.parent_concept = concept
    evaluator = LabelEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(label),
        Mock(),
    )
    evaluator.run()
    assert classification == label.quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], LabelSelector)


def test_changes_labeled_label_quality(bubble_chamber):
    label = Mock()
    label.start.is_label = False
    label.parent_concept.classifier.classify.return_value = 0.5
    label.quality = 0.5

    label_label = Mock()
    label_label.parent_concept.classifier.classify.return_value = 1.0
    label_label.labels = bubble_chamber.new_structure_collection()

    label.labels = bubble_chamber.new_structure_collection(label_label)

    evaluator = LabelEvaluator(
        Mock(),
        Mock(),
        bubble_chamber,
        bubble_chamber.new_structure_collection(label),
        Mock(),
    )
    evaluator.run()
    assert label.quality > 0.5
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], LabelSelector)
