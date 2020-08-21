import math
import pytest
import random
from unittest.mock import Mock, patch

import numpy

from homer.activation_patterns import WorkspaceActivationPattern
from homer.workspace_location import WorkspaceLocation


FLOAT_COMPARISON_TOLERANCE = 1e-5


@pytest.mark.parametrize(
    "depth, height, width, workspace_depth, workspace_height, workspace_width, "
    + "expected_matrix, expected_depth_divisor, expected_height_divisor, "
    + "expected_width_divisor",
    [
        (1, 1, 1, 1, 1, 1, [[[0.0]]], 1, 1, 1),
        (
            3,
            3,
            3,
            30,
            30,
            30,
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            ],
            10,
            10,
            10,
        ),
    ],
)
def test_constructor(
    depth,
    height,
    width,
    workspace_depth,
    workspace_height,
    workspace_width,
    expected_matrix,
    expected_depth_divisor,
    expected_height_divisor,
    expected_width_divisor,
):
    activation_pattern = WorkspaceActivationPattern(
        Mock(),
        depth,
        height,
        width,
        workspace_depth=workspace_depth,
        workspace_height=workspace_height,
        workspace_width=workspace_width,
    )
    assert numpy.array_equal(expected_matrix, activation_pattern.activation_matrix)
    assert expected_depth_divisor == activation_pattern.depth_divisor
    assert expected_height_divisor == activation_pattern.height_divisor
    assert expected_width_divisor == activation_pattern.width_divisor


@pytest.mark.parametrize(
    "depth, height, width, workspace_depth, workspace_height, workspace_width, "
    + "activation_matrix, location, expected_activation",
    [
        (
            3,
            3,
            3,
            30,
            30,
            30,
            [
                [[0.7, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            ],
            [0, 0, 0],
            0.7,
        ),
        (
            3,
            3,
            3,
            30,
            30,
            30,
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.6, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            ],
            [1, 1, 1],
            0.6,
        ),
    ],
)
def test_at(
    depth,
    height,
    width,
    workspace_depth,
    workspace_height,
    workspace_width,
    activation_matrix,
    location,
    expected_activation,
):
    activation_pattern = WorkspaceActivationPattern(
        Mock(),
        depth,
        height,
        width,
        workspace_depth=workspace_depth,
        workspace_height=workspace_height,
        workspace_width=workspace_width,
    )
    activation_pattern.activation_matrix = activation_matrix
    activation = activation_pattern.at(
        WorkspaceLocation(location[0], location[1], location[2])
    )
    assert expected_activation == activation


@pytest.mark.parametrize(
    "activation_matrix, expected_signal",
    [([[[1, 0], [0.4, 1]]], [[[0.1, 0], [0, 0.1]]])],
)
def test_get_spreading_signal(activation_matrix, expected_signal):
    activation_pattern = WorkspaceActivationPattern(Mock())
    activation_pattern.activation_matrix = activation_matrix
    actual_signal = activation_pattern.get_spreading_signal()
    assert numpy.array_equal(expected_signal, actual_signal)


@pytest.mark.parametrize(
    "activation_matrix, expected_activation",
    [
        ([[[0.6, 0.4], [0.5, 0.4], [0.6, 0.5]]], 0.5),
        ([[[0.0, 1.0], [1.0, 0.0], [1.0, 0.0]]], 0.5),
        ([[[0.5, 0.0], [0.25, 0.25], [0.2, 0.3]]], 0.25),
    ],
)
def test_as_scalar(activation_matrix, expected_activation):
    activation_pattern = WorkspaceActivationPattern(Mock())
    activation_pattern.activation_matrix = activation_matrix
    actual_activation = activation_pattern.as_scalar()
    assert math.isclose(
        expected_activation, actual_activation, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


@pytest.mark.parametrize(
    "activation_matrix, expected_i, expected_j, expected_k",
    [
        ([[[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]], 0, 0, 0,),
        ([[[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]]], 0, 1, 1,),
        ([[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]], 0, 2, 2,),
    ],
)
def test_get_high_location(activation_matrix, expected_i, expected_j, expected_k):
    activation_pattern = WorkspaceActivationPattern(Mock())
    activation_pattern.activation_matrix = activation_matrix
    location = activation_pattern.get_high_location()
    assert (expected_i, expected_j, expected_k) == (location.i, location.j, location.k)


@pytest.mark.parametrize(
    "activation_coefficient, depth, height, width, workspace_depth, "
    + "workspace_height, workspace_width, amount, location, expected_matrix",
    [
        (
            0.1,
            3,
            3,
            3,
            30,
            30,
            30,
            0.6,
            [0, 0, 0],
            [
                [[0.06, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            ],
        ),
        (
            0.1,
            3,
            3,
            3,
            30,
            30,
            30,
            0.6,
            [1, 1, 1],
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.06, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            ],
        ),
    ],
)
def test_boost(
    activation_coefficient,
    depth,
    height,
    width,
    workspace_depth,
    workspace_height,
    workspace_width,
    amount,
    location,
    expected_matrix,
):
    activation_pattern = WorkspaceActivationPattern(
        activation_coefficient,
        depth,
        height,
        width,
        workspace_depth=workspace_depth,
        workspace_height=workspace_height,
        workspace_width=workspace_width,
    )
    with patch.object(random, "randint", return_value=0):
        activation_pattern.boost(
            amount, WorkspaceLocation(location[0], location[1], location[2])
        )
        activation_pattern.update()
        assert numpy.array_equal(expected_matrix, activation_pattern.activation_matrix)


@pytest.mark.parametrize(
    "activation_matrix, amount, expected_activation",
    [
        (
            [[[0.6, 0.4], [0.5, 0.4], [0.6, 0.5]]],
            0.5,
            [[[0.85, 0.65], [0.75, 0.65], [0.85, 0.75]]],
        ),
    ],
)
def test_boost_evenly(activation_matrix, amount, expected_activation):
    with patch.object(random, "randint", return_value=0):
        activation_pattern = WorkspaceActivationPattern(0.5, depth=1, height=3, width=2)
        activation_pattern.activation_matrix = numpy.array(activation_matrix)
        activation_pattern.boost_evenly(amount)
        activation_pattern.update()
        assert numpy.array_equal(
            expected_activation, activation_pattern.activation_matrix
        )


@pytest.mark.parametrize(
    "activation_matrix, signal, expected_activation",
    [
        (
            [[[0.6, 0.4], [0.5, 0.4], [0.6, 0.5]]],
            [[[0.1, 0], [0, 0], [0.1, 0.1]]],
            [[[0.7, 0.4], [0.5, 0.4], [0.7, 0.6]]],
        ),
    ],
)
def test_boost_with_signal(activation_matrix, signal, expected_activation):
    with patch.object(random, "randint", return_value=0):
        activation_pattern = WorkspaceActivationPattern(0.5, depth=1, height=3, width=2)
        activation_pattern.activation_matrix = numpy.array(activation_matrix)
        activation_pattern.boost_with_signal(signal)
        activation_pattern.update()
        assert numpy.array_equal(
            expected_activation, activation_pattern.activation_matrix
        )
