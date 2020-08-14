import pytest

from homer.workspace_location import WorkspaceLocation


@pytest.mark.parametrize(
    "depth, height, width, workspace_depth, workspace_height, workspace_width, "
    + "coordinates, expected_i, expected_j, expected_k",
    [
        (1, 3, 3, 1, 6, 5, [0, 0, 0], 0, 0, 0),
        (1, 3, 3, 1, 6, 5, [0, 5, 4], 0, 2, 2),
        (1, 3, 3, 1, 6, 5, [0, 2.5, 2], 0, 1, 1),
    ],
)
def test_from_workspace_coordinates(
    depth,
    height,
    width,
    workspace_depth,
    workspace_height,
    workspace_width,
    coordinates,
    expected_i,
    expected_j,
    expected_k,
):
    WorkspaceLocation.DEPTH = depth
    WorkspaceLocation.HEIGHT = height
    WorkspaceLocation.WIDTH = width
    WorkspaceLocation.WORKSPACE_DEPTH = workspace_depth
    WorkspaceLocation.WORKSPACE_HEIGHT = workspace_height
    WorkspaceLocation.WORKSPACE_WIDTH = workspace_width
    workspace_location = WorkspaceLocation.from_workspace_coordinates(coordinates)
    assert (expected_i, expected_j, expected_k) == (
        workspace_location.i,
        workspace_location.j,
        workspace_location.k,
    )
