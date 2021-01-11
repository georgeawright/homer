import pytest
import statistics
from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Space


@pytest.mark.parametrize(
    "coordinates, n_s_coordinates, w_e_coordinates, nw_se_coordinates, ne_sw_coordinates",
    [([0, 0], [0], [0], [0], [2])],
)
def test_add(
    coordinates, n_s_coordinates, w_e_coordinates, nw_se_coordinates, ne_sw_coordinates
):

    north_south_space = Space(
        "",
        "",
        "north-south",
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
        1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [location.coordinates[0]],
        },
    )
    west_east_space = Space(
        "",
        "",
        "west-east",
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
        1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [location.coordinates[1]]
        },
    )
    nw_se_space = Space(
        "",
        "",
        "nw-se",
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
        1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [statistics.fmean(location.coordinates)]
        },
    )
    ne_sw_space = Space(
        "",
        "",
        "ne-sw",
        Mock(),
        [],
        StructureCollection(),
        1,
        [],
        [],
        1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                statistics.fmean([location.coordinates[0], 4 - location.coordinates[1]])
            ]
        },
    )
    location_concept = Mock()
    location_concept.name = "location"
    location_space = Space(
        "",
        "",
        "location",
        location_concept,
        [],
        StructureCollection(),
        2,
        [north_south_space, west_east_space],
        [north_south_space, west_east_space, nw_se_space, ne_sw_space],
        1,
        is_basic_level=True,
    )
    location = Location(coordinates, location_space)
    chunk = Chunk("", "", Mock(), [location], Mock(), Mock())
    location_space.add(chunk)

    assert chunk in location_space.contents
    assert chunk.location_in_space(location_space) == Location(
        coordinates, location_space
    )
    assert chunk in north_south_space.contents
    assert chunk.location_in_space(north_south_space) == Location(
        n_s_coordinates, north_south_space
    )
    assert chunk in west_east_space.contents
    assert chunk.location_in_space(west_east_space) == Location(
        w_e_coordinates, west_east_space
    )
    assert chunk in nw_se_space.contents
    assert chunk.location_in_space(nw_se_space) == Location(
        nw_se_coordinates, nw_se_space
    )
    assert chunk in ne_sw_space.contents
    assert chunk.location_in_space(ne_sw_space) == Location(
        ne_sw_coordinates, ne_sw_space
    )
