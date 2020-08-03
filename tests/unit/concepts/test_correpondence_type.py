import pytest
from unittest.mock import Mock

from homer.concepts.correspondence_type import CorrespondenceType


@pytest.mark.parametrize(
    "affinity_calculation, number_of_same_labels, proximity, expected_affinity",
    [
        (
            lambda number_of_same_labels, proximity: number_of_same_labels * proximity,
            1,
            1.0,
            1,
        ),
        (
            lambda number_of_same_labels, proximity: number_of_same_labels * proximity,
            2,
            0.9,
            1,
        ),
        (
            lambda number_of_same_labels, proximity: number_of_same_labels + proximity,
            0,
            0.5,
            0.5,
        ),
        (
            lambda number_of_same_labels, proximity: number_of_same_labels - proximity,
            0,
            0.5,
            0.0,
        ),
    ],
)
def test_calculate_affinity(
    affinity_calculation, number_of_same_labels, proximity, expected_affinity
):
    correspondence_concept = CorrespondenceType(Mock(), affinity_calculation)
    actual_affinity = correspondence_concept.calculate_affinity(
        number_of_same_labels, proximity
    )
    assert expected_affinity == actual_affinity
