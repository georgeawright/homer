import pytest
from unittest.mock import Mock, patch

from homer.codelets import Builder, Evaluator, Selector
from homer.codelets.factories import RationalFactory
from homer.structure_collection import StructureCollection


@pytest.fixture
def concepts():
    build_concept = Mock()
    build_concept.name = "build"
    evaluate_concept = Mock()
    evaluate_concept.name = "evaluate"
    select_concept = Mock()
    select_concept.name = "select"
    inner_concept = Mock()
    inner_concept.name = "inner"
    outer_concept = Mock()
    outer_concept.name = "outer"
    forward_concept = Mock()
    forward_concept.name = "forward"
    reverse_concept = Mock()
    reverse_concept.name = "reverse"
    correspondence_concept = Mock()
    correspondence_concept.name = "correspondence"
    chunk_concept = Mock()
    chunk_concept.name = "chunk"
    label_concept = Mock()
    label_concept.name = "label"
    phrase_concept = Mock()
    phrase_concept.name = "phrase"
    relation_concept = Mock()
    relation_concept.name = "relation"
    view_monitoring_concept = Mock()
    view_monitoring_concept.name = "view-monitoring"
    view_simplex_concept = Mock()
    view_simplex_concept.name = "view-simplex"
    word_concept = Mock()
    word_concept.name = "word"
    concepts = StructureCollection(
        {
            build_concept,
            evaluate_concept,
            select_concept,
            inner_concept,
            outer_concept,
            forward_concept,
            reverse_concept,
            correspondence_concept,
            chunk_concept,
            label_concept,
            phrase_concept,
            relation_concept,
            view_monitoring_concept,
            view_simplex_concept,
            word_concept,
        }
    )
    for concept in concepts:
        concept.activation = 0.5
    return concepts


@pytest.fixture
def bubble_chamber(concepts):
    bubble_chamber = Mock()
    bubble_chamber.concepts = concepts
    bubble_chamber.satisfaction = 0
    return bubble_chamber


@pytest.fixture
def coderack():
    rack = Mock()
    rack.number_of_codelets_of_type.return_value = 0.0
    return rack


def test_decide_follow_up_class_returns_codelet_class(
    bubble_chamber, coderack, concepts
):
    factory_codelet = RationalFactory(Mock(), Mock(), bubble_chamber, coderack, Mock())
    follow_up_class = factory_codelet._decide_follow_up_class()
    codelet_types = [Builder, Evaluator, Selector]
    assert (
        follow_up_class.__bases__[0] in codelet_types
        or follow_up_class.__bases__[0].__bases__[0] in codelet_types
    )