import math
import pytest
from unittest.mock import Mock

from homer.concept import Concept

FLOAT_COMPARISON_TOLERANCE = 1e-5


@pytest.mark.parametrize(
    "depth,boundary,prototype,exception_message",
    [
        (0, None, None, "depth 0 is less than 1."),
        (1, [1], "hot", "a concept with a symbolic prototype cannot have a boundary."),
        (1, [1, 2], [2, 2], "boundary [1, 2] is multidimensional."),
        (1, [1], [2, 2], "have different dimensionality."),
        (1, [1], [1], "prototype and boundary are equal [1]."),
    ],
)
def test_concept_constructor_exceptions(depth, boundary, prototype, exception_message):
    with pytest.raises(Exception) as excinfo:
        Concept("hot", Mock(), depth=depth, prototype=prototype, boundary=boundary)
    assert exception_message in str(excinfo.value)


@pytest.mark.parametrize(
    "prototype,boundary,distance_metric,candidate,expected",
    [
        ([22], [19], math.dist, [20], 2),
        ([22], [19], math.dist, [21], 1),
        ([22], [19], math.dist, [22], 0),
        ([22], [19], math.dist, [23], 0),
        ([16], None, math.dist, [16], 0),
        ([16], None, math.dist, [10], 6),
        ([16], None, math.dist, [26], 10),
        ([4], [7], math.dist, [7], 3),
        ([4], [7], math.dist, [-20], 0),
        ("hot", None, lambda a, b: 0 if a == b else math.inf, "hot", 0),
        ("cold", None, lambda a, b: 0 if a == b else math.inf, "hot", math.inf),
    ],
)
def test_distance_from(prototype, boundary, distance_metric, candidate, expected):
    concept = Concept(
        "hot",
        Mock(),
        prototype=prototype,
        boundary=boundary,
        distance_metric=distance_metric,
    )
    assert expected == concept.distance_from(candidate)


def test_distance_from_raises_exception_if_no_distance_metric():
    concept = Concept("hot", Mock())
    with pytest.raises(Exception) as excinfo:
        concept.distance_from([1])
    assert "Concept hot has no distance metric." in str(excinfo.value)


@pytest.mark.parametrize(
    "a, b, distance_metric, expected",
    [
        ([22], [20], math.dist, 2),
        ([10], [10], math.dist, 0),
        ([0], [10], math.dist, 10),
        ("hot", "hot", lambda a, b: 0 if a == b else math.inf, 0),
        ("hot", "cold", lambda a, b: 0 if a == b else math.inf, math.inf),
    ],
)
def test_distance_between(a, b, distance_metric, expected):
    concept = Concept("hot", Mock(), distance_metric=distance_metric)
    assert expected == concept.distance_between(a, b)


@pytest.mark.parametrize(
    "a, b, distance_metric, distance_to_proximity_weight, expected",
    [
        ([22], [20], math.dist, 1.5, 0.75),
        ([10], [10], math.dist, 1.5, 1.0),
        ([0], [10], math.dist, 1.5, 0.15),
        ("hot", "hot", lambda a, b: 0 if a == b else math.inf, 1.5, 1.0),
        ("hot", "cold", lambda a, b: 0 if a == b else math.inf, 1.5, 0.0),
    ],
)
def test_proximity_between(
    a, b, distance_metric, distance_to_proximity_weight, expected
):
    concept = Concept("hot", Mock(), distance_metric=distance_metric)
    concept.DISTANCE_TO_PROXIMITY_WEIGHT = 1.5
    assert math.isclose(
        expected, concept.proximity_between(a, b), abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize("depth, expected", [(1, 1.0), (10, 0.1), (5, 0.2)])
def test_depth_rating(depth, expected):
    concept = Concept("hot", Mock(), depth=depth)
    assert math.isclose(
        expected, concept.depth_rating, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize(
    "prototype,boundary,distance_metric,candidate,distance_to_proximity_weight,expected",
    [
        ([22], [19], math.dist, [20], 1.5, 0.75),
        ([22], [19], math.dist, [21], 1.5, 1.0),
        ([22], [19], math.dist, [22], 1.5, 1.0),
        ([22], [19], math.dist, [23], 1.5, 1.0),
        ([16], None, math.dist, [16], 1.5, 1.0),
        ([16], None, math.dist, [10], 1.5, 0.25),
        ([16], None, math.dist, [26], 1.5, 0.15),
        ([4], [7], math.dist, [7], 1.5, 0.5),
        ([4], [7], math.dist, [-20], 1.5, 1.0),
        ("hot", None, lambda a, b: 0 if a == b else math.inf, "hot", 1.5, 1.0),
        ("cold", None, lambda a, b: 0 if a == b else math.inf, "hot", 1.5, 0.0),
    ],
)
def test_proximity_to(
    prototype,
    boundary,
    distance_metric,
    candidate,
    distance_to_proximity_weight,
    expected,
):
    concept = Concept(
        "hot",
        Mock(),
        prototype=prototype,
        boundary=boundary,
        distance_metric=distance_metric,
    )
    concept.DISTANCE_TO_PROXIMITY_WEIGHT = distance_to_proximity_weight
    assert math.isclose(
        expected, concept.proximity_to(candidate), abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize("a_activation, b_activation, expected", [(1.0, 0.0, 1.0)])
def test_most_active(a_activation, b_activation, expected):
    a_activation_pattern = Mock()
    a_activation_pattern.get_activation_as_scalar = Mock()
    a_activation_pattern.get_activation_as_scalar.side_effect = [a_activation]
    b_activation_pattern = Mock()
    b_activation_pattern.get_activation_as_scalar = Mock()
    b_activation_pattern.get_activation_as_scalar.side_effect = [b_activation]
    a = Concept("a", a_activation_pattern)
    b = Concept("b", b_activation_pattern)
    result = Concept.most_active(a, b)
    assert a == result
