import pytest
import statistics
from unittest.mock import Mock

from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Space


@pytest.mark.skip
@pytest.mark.parametrize(
    "coordinates, n_s_coordinates, w_e_coordinates, nw_se_coordinates, ne_sw_coordinates",
    [([0, 0], [0], [0], [0], [2])],
)
def test_add(
    coordinates, n_s_coordinates, w_e_coordinates, nw_se_coordinates, ne_sw_coordinates
):
    location_space = Space("", "", "location", StructureCollection(), Mock(), Mock())
    north_south_space = Space(
        "north-south",
        "",
        "north-south",
        StructureCollection(),
        Mock(),
        Mock(),
        coordinates_from_super_space_location=lambda location: [
            location.coordinates[0]
        ],
    )
    west_east_space = Space(
        "west-east",
        "",
        "west-east",
        StructureCollection(),
        Mock(),
        Mock(),
        coordinates_from_super_space_location=lambda location: [
            location.coordinates[1]
        ],
    )
    nw_se_space = Space(
        "nw-se",
        "",
        "nw-se",
        StructureCollection(),
        Mock(),
        Mock(),
        coordinates_from_super_space_location=lambda location: [
            statistics.fmean(location.coordinates)
        ],
    )
    ne_sw_space = Space(
        "ne-sw",
        "",
        "ne-sw",
        StructureCollection(),
        Mock(),
        Mock(),
        coordinates_from_super_space_location=lambda location: [
            statistics.fmean([location.coordinates[0], 4 - location.coordinates[1]])
        ],
    )
    location_space.sub_spaces.add(north_south_space)
    location_space.sub_spaces.add(west_east_space)
    location_space.sub_spaces.add(nw_se_space)
    location_space.sub_spaces.add(ne_sw_space)
    location = Location(coordinates, location_space)
    parent_spaces = StructureCollection({location_space})
    chunk = Chunk("", "", Mock(), location, Mock(), Mock(), Mock(), parent_spaces)
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
