import pytest
from unittest.mock import Mock

from homer.activation_patterns.workspace_activation_pattern import (
    WorkspaceActivationPattern,
)


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
