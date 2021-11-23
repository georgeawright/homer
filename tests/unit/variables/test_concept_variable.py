from unittest.mock import Mock

from homer.location import Location
from homer.variables import ConceptualSpaceVariable, ConceptVariable, NumberVariable


def test_subsumes():
    positive_concept = Mock()
    more_concept = Mock()
    temperature_space = Mock()
    cold_concept = Mock()
    cold_concept.location = Location([[5]], temperature_space)
    mild_concept = Mock()
    mild_concept.location = Location([[10]], temperature_space)
    warm_concept = Mock()
    warm_concept.location = Location([[15]], temperature_space)
    hot_concept = Mock()
    hot_concept.location = Location([[20]], temperature_space)
    location_space = Mock()
    north_concept = Mock()
    north_concept.location = Location([[0, 5]], location_space)

    hot_concept.has_relation_with.return_value = True
    warm_concept.has_relation_with.return_value = True
    mild_concept.has_relation_with.return_value = False
    cold_concept.has_relation_with.return_value = False

    any_concept = ConceptVariable(None, None, None)
    assert any_concept.subsumes(cold_concept)
    assert any_concept.subsumes(mild_concept)
    assert any_concept.subsumes(warm_concept)
    assert any_concept.subsumes(hot_concept)
    assert any_concept.subsumes(north_concept)

    located_concept = ConceptVariable(Location([[10]], temperature_space), None, None)
    assert located_concept.subsumes(mild_concept)
    assert not located_concept.subsumes(cold_concept)
    assert not located_concept.subsumes(warm_concept)
    assert not located_concept.subsumes(hot_concept)
    assert not located_concept.subsumes(north_concept)

    concept_with_variable_location = ConceptVariable(
        Location([[NumberVariable()]], temperature_space), None, None
    )
    assert concept_with_variable_location.subsumes(cold_concept)
    assert concept_with_variable_location.subsumes(mild_concept)
    assert concept_with_variable_location.subsumes(warm_concept)
    assert concept_with_variable_location.subsumes(hot_concept)
    assert not concept_with_variable_location.subsumes(north_concept)

    relation = Mock()
    relation.parent_concept = more_concept
    concept_with_relation = ConceptVariable(
        None, [(positive_concept, lambda: relation.parent_concept)], None
    )
    assert concept_with_relation.subsumes(hot_concept)
    assert concept_with_relation.subsumes(warm_concept)
    assert not concept_with_relation.subsumes(mild_concept)
    assert not concept_with_relation.subsumes(cold_concept)

    hot_or_warm_concept = ConceptVariable(None, None, [hot_concept, warm_concept])
    assert hot_or_warm_concept.subsumes(hot_concept)
    assert hot_or_warm_concept.subsumes(warm_concept)
    assert not hot_or_warm_concept.subsumes(mild_concept)
    assert not hot_or_warm_concept.subsumes(cold_concept)
    assert not hot_or_warm_concept.subsumes(north_concept)
