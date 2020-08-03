import math
import pytest
from unittest.mock import Mock

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)


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
    assert expected_matrix == activation_pattern.activation_matrix
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
            [1, 1, 1],
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
            [11, 11, 11],
            0.6,
        ),
    ],
)
def test_get_activation(
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
    activation = activation_pattern.get_activation(location)
    assert expected_activation == activation


@pytest.mark.parametrize(
    "activation_matrix, expected_activation",
    [
        ([[[0.6, 0.4], [0.5, 0.4], [0.6, 0.5]]], 0.5),
        ([[[0.0, 1.0], [1.0, 0.0], [1.0, 0.0]]], 0.5),
        ([[[0.5, 0.0], [0.25, 0.25], [0.2, 0.3]]], 0.25),
    ],
)
def test_activation_as_scalar(activation_matrix, expected_activation):
    activation_pattern = WorkspaceActivationPattern(Mock())
    activation_pattern.activation_matrix = activation_matrix
    actual_activation = activation_pattern.get_activation_as_scalar()
    assert math.isclose(
        expected_activation, actual_activation, abs_tol=FLOAT_COMPARISON_TOLERANCE
    )


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
            [1, 1, 1],
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
            [11, 11, 11],
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.06, 0.0], [0.0, 0.0, 0.0]],
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            ],
        ),
    ],
)
def test_boost_activation(
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
    activation_pattern.boost_activation(amount, location)
    assert expected_matrix == activation_pattern.activation_matrix


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
def test_boost_activation_evenly(activation_matrix, amount, expected_activation):
    activation_pattern = WorkspaceActivationPattern(0.5)
    activation_pattern.activation_matrix = activation_matrix
    activation_pattern.boost_activation_evenly(amount)
    assert expected_activation == activation_pattern.activation_matrix
