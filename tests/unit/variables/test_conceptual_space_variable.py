from unittest.mock import Mock

from homer.variables import ConceptualSpaceVariable


def test_subsumes():
    location_space = Mock()
    temperature_space = Mock()
    height_space = Mock()
    goodness_space = Mock()

    any_space = ConceptualSpaceVariable()
    some_1d_space = ConceptualSpaceVariable(
        [temperature_space, height_space, goodness_space]
    )
    height_or_temperature_space = ConceptualSpaceVariable(
        [temperature_space, height_space]
    )

    assert any_space.subsumes(location_space)
    assert any_space.subsumes(temperature_space)
    assert any_space.subsumes(height_space)
    assert any_space.subsumes(goodness_space)
    assert any_space.subsumes(some_1d_space)
    assert any_space.subsumes(height_or_temperature_space)

    assert some_1d_space.subsumes(temperature_space)
    assert some_1d_space.subsumes(height_space)
    assert some_1d_space.subsumes(goodness_space)
    assert some_1d_space.subsumes(height_or_temperature_space)
    assert not some_1d_space.subsumes(location_space)
    assert not some_1d_space.subsumes(any_space)

    assert height_or_temperature_space.subsumes(temperature_space)
    assert height_or_temperature_space.subsumes(height_space)
    assert not height_or_temperature_space.subsumes(location_space)
    assert not height_or_temperature_space.subsumes(goodness_space)
    assert not height_or_temperature_space.subsumes(any_space)
    assert not height_or_temperature_space.subsumes(some_1d_space)
