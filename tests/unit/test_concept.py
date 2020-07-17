import math
import pytest

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
        Concept("hot", depth=depth, prototype=prototype, boundary=boundary)
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
        "hot", prototype=prototype, boundary=boundary, distance_metric=distance_metric
    )
    assert expected == concept.distance_from(candidate)


def test_distance_from_raises_exception_if_no_distance_metric():
    concept = Concept("hot")
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
    concept = Concept("hot", distance_metric=distance_metric)
    assert expected == concept.distance_between(a, b)


@pytest.mark.parametrize(
    "a, b, distance_metric, maximum_distance, expected",
    [
        ([22], [20], math.dist, 10, 0.2),
        ([10], [10], math.dist, 10, 0.0),
        ([0], [10], math.dist, 10, 1.0),
        ("hot", "hot", lambda a, b: 0 if a == b else math.inf, 10, 0.0),
        ("hot", "cold", lambda a, b: 0 if a == b else math.inf, 10, 1.0),
    ],
)
def test_distance_between_as_rating(a, b, distance_metric, maximum_distance, expected):
    concept = Concept("hot", distance_metric=distance_metric)
    assert expected == concept.distance_between_as_rating(a, b)


@pytest.mark.parametrize(
    "depth, maximum_depth, expected", [(1, 10, 0.1), (10, 10, 1.0), (13, 10, 1.0)]
)
def test_depth_rating(depth, maximum_depth, expected):
    concept = Concept("hot", depth=depth)
    concept.MAXIMUM_DEPTH = maximum_depth
    assert math.isclose(
        expected, concept.depth_rating, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize(
    "prototype,boundary,distance_metric,candidate,maximum_distance,expected",
    [
        ([22], [19], math.dist, [20], 10, 0.2),
        ([22], [19], math.dist, [21], 10, 0.1),
        ([22], [19], math.dist, [22], 10, 0.0),
        ([22], [19], math.dist, [23], 10, 0.0),
        ([16], None, math.dist, [16], 10, 0.0),
        ([16], None, math.dist, [10], 10, 0.6),
        ([16], None, math.dist, [26], 10, 1.0),
        ([4], [7], math.dist, [7], 10, 0.3),
        ([4], [7], math.dist, [-20], 10, 0.0),
        ("hot", None, lambda a, b: 0 if a == b else math.inf, "hot", 10, 0.0),
        ("cold", None, lambda a, b: 0 if a == b else math.inf, "hot", 10, 1.0),
    ],
)
def test_distance_rating(
    prototype, boundary, distance_metric, candidate, maximum_distance, expected
):
    concept = Concept(
        "hot", prototype=prototype, boundary=boundary, distance_metric=distance_metric
    )
    concept.MAXIMUM_DISTANCE = maximum_distance
    assert expected == concept.distance_rating(candidate)


@pytest.mark.parametrize(
    "depth,activation,amount,expected",
    [(2, 0.0, 0.1, 0.05), (2, 0.5, 0.5, 0.75), (2, 0.99, 0.1, 1)],
)
def test_boost_activation(depth, activation, amount, expected):
    concept = Concept("hot", depth=depth, activation=activation)
    concept.boost_activation(amount)
    assert math.isclose(
        expected, concept.activation, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize(
    "depth,activation,decay_rate,expected",
    [(2, 0.6, 0.1, 0.55), (2, 0.05, 0.1, 0.0), (2, 0.01, 0.1, 0.0)],
)
def test_decay_activation(depth, activation, decay_rate, expected):
    Concept.DECAY_RATE = decay_rate
    concept = Concept("hot", depth=depth, activation=activation)
    concept.decay_activation()
    assert math.isclose(
        expected, concept.activation, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )
