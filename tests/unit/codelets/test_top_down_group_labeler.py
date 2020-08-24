import math
import pytest
from unittest.mock import Mock

from homer.codelets import GroupExtender, TopDownGroupLabeler

FLOAT_COMPARISON_TOLERANCE = 1e-1


@pytest.mark.parametrize(
    "label_strengths, group_size, expected",
    [([0.5, 0.5], 2, 0.5), ([0.5, 0.5], 4, 0.25)],
)
def test_calculate_confidence(label_strengths, group_size, expected, target_perceptlet):
    concept = Mock()
    target_perceptlet.size = group_size
    target_perceptlet.members = set()
    for label_strength in label_strengths:
        label = Mock()
        label.parent_concept = concept
        label.activation.as_scalar.side_effect = [label_strength]
        member = Mock()
        member.labels = {label}
        target_perceptlet.members.add(member)
    codelet = TopDownGroupLabeler(
        Mock(), Mock(), concept, target_perceptlet, Mock(), Mock()
    )
    codelet._calculate_confidence()
    assert math.isclose(
        expected, codelet.confidence, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


def test_engender_follow_up(target_perceptlet):
    codelet = TopDownGroupLabeler(
        Mock(), Mock(), Mock(), target_perceptlet, Mock(), Mock()
    )
    codelet.confidence = Mock()
    follow_up = codelet._engender_follow_up()
    assert GroupExtender == type(follow_up)
