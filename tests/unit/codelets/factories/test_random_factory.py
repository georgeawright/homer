import pytest
from unittest.mock import Mock

from homer.codelets import Evaluator, Publisher, Suggester
from homer.codelets.factories import RandomFactory
from homer.structure_collection import StructureCollection


@pytest.fixture
def concepts():
    suggest_concept = Mock()
    suggest_concept.name = "suggest"
    evaluate_concept = Mock()
    evaluate_concept.name = "evaluate"
    publish_concept = Mock()
    publish_concept.name = "publish"
    inner_concept = Mock()
    inner_concept.name = "inner"
    outer_concept = Mock()
    outer_concept.name = "outer"
    forward_concept = Mock()
    forward_concept.name = "forward"
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
    return StructureCollection(
        {
            suggest_concept,
            evaluate_concept,
            publish_concept,
            inner_concept,
            outer_concept,
            forward_concept,
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


@pytest.mark.skip
def test_decide_follow_up_class_returns_codelet_class(
    bubble_chamber, coderack, concepts
):
    factory_codelet = RandomFactory(Mock(), Mock(), bubble_chamber, coderack, Mock())
    follow_up_class = factory_codelet._decide_follow_up_class()
    codelet_types = [Suggester, Evaluator, Publisher]
    assert (
        follow_up_class in codelet_types
        or follow_up_class.__bases__[0] in codelet_types
        or follow_up_class.__bases__[0].__bases__[0] in codelet_types
    )
