import pytest
from unittest.mock import Mock

from homer.codelets.suggesters import (
    ChunkSuggester,
    CorrespondenceSuggester,
    LabelSuggester,
    RelationSuggester,
)
from homer.codelets.factories import ConceptDrivenFactory
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation


@pytest.fixture
def concepts():
    suggest_concept = Mock()
    suggest_concept.name = "suggest"
    inner_concept = Mock()
    inner_concept.name = "inner"
    forward_concept = Mock()
    forward_concept.name = "forward"
    label_concept = Mock()
    label_concept.name = "label"
    relation_concept = Mock()
    relation_concept.name = "relation"
    correspondence_concept = Mock()
    correspondence_concept.name = "correspondence"
    chunk_concept = Mock()
    chunk_concept.name = "chunk"
    concepts = StructureCollection(
        {
            suggest_concept,
            inner_concept,
            forward_concept,
            label_concept,
            relation_concept,
            correspondence_concept,
            chunk_concept,
        }
    )
    for concept in concepts:
        concept.activation = 0.5
    return concepts


@pytest.fixture
def example_label_concept():
    concept = Mock()
    concept.name = "label"
    concept.structure_type = Label
    concept.activation = 1.0
    concept.instance_type = str
    return concept


@pytest.fixture
def example_correspondence_concept():
    concept = Mock()
    concept.name = "correspondence"
    concept.structure_type = Correspondence
    concept.activation = 1.0
    concept.instance_type = str
    return concept


@pytest.fixture
def example_relation_concept():
    concept = Mock()
    concept.name = "relation"
    concept.structure_type = Relation
    concept.activation = 1.0
    concept.instance_type = str
    return concept


@pytest.fixture
def example_rule():
    rule = Mock()
    rule.name = "rule"
    rule.activation = 1.0
    return rule


@pytest.fixture
def bubble_chamber(
    concepts,
    example_correspondence_concept,
    example_label_concept,
    example_relation_concept,
    example_rule,
):
    chamber = Mock()
    chamber.concepts = concepts
    chamber.concepts.add(example_correspondence_concept)
    chamber.concepts.add(example_label_concept)
    chamber.concepts.add(example_relation_concept)
    chamber.rules = StructureCollection({example_rule})
    input_node = Mock()
    input_node.value = ""
    chamber.input_nodes = StructureCollection({input_node})
    chamber.satisfaction = 0
    return chamber


@pytest.fixture
def coderack():
    rack = Mock()
    rack.number_of_codelets_of_type.return_value = 0.0
    return rack


@pytest.mark.skip
def test_gets_appropriate_follow_up_class(
    bubble_chamber,
    coderack,
    example_correspondence_concept,
    example_label_concept,
    example_relation_concept,
    example_rule,
):
    factory_codelet = ConceptDrivenFactory(
        Mock(), Mock(), bubble_chamber, coderack, Mock()
    )
    assert (
        factory_codelet._get_follow_up_class(example_correspondence_concept)
        == CorrespondenceSuggester
    )
    assert factory_codelet._get_follow_up_class(example_label_concept) == LabelSuggester
    assert (
        factory_codelet._get_follow_up_class(example_relation_concept)
        == RelationSuggester
    )
    assert factory_codelet._get_follow_up_class(example_rule) == ChunkSuggester
