import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import StretchyProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators import RelationEvaluator
from homer.codelets.selectors import RelationSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Relation
from homer.structures.spaces import WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    return chamber


@pytest.fixture
def good_relation(bubble_chamber):
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    temperature_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    input_space = WorkingSpace("input", StructureCollection(), 0, location_concept)
    temperature_space = WorkingSpace(
        "temperature", StructureCollection(), 0, temperature_concept
    )
    more_concept = Concept(
        "more",
        [5],
        StretchyProximityClassifier(),
        temperature_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    parent_spaces = StructureCollection({input_space, temperature_space})
    start = Chunk(
        [15],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    end = Chunk(
        [10],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    quality = 0.0
    relation = Relation(start, end, more_concept, temperature_space, quality)
    return relation


@pytest.fixture
def bad_relation(bubble_chamber):
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    temperature_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    input_space = WorkingSpace("input", StructureCollection(), 0, location_concept)
    temperature_space = WorkingSpace(
        "temperature", StructureCollection(), 0, temperature_concept
    )
    more_concept = Concept(
        "more",
        [5],
        StretchyProximityClassifier(),
        temperature_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    parent_spaces = StructureCollection({input_space, temperature_space})
    start = Chunk(
        [10],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    end = Chunk(
        [15],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    quality = 1.0
    relation = Relation(start, end, more_concept, temperature_space, quality)
    return relation


def test_increases_quality_of_good_relation(bubble_chamber, good_relation):
    original_quality = good_relation.quality
    parent_id = ""
    urgency = 1.0
    evaluator = RelationEvaluator.spawn(
        parent_id, bubble_chamber, good_relation, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_relation.quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], RelationSelector)


def test_decreases_quality_of_bad_label(bubble_chamber, bad_relation):
    original_quality = bad_relation.quality
    parent_id = ""
    urgency = 1.0
    evaluator = RelationEvaluator.spawn(
        parent_id, bubble_chamber, bad_relation, urgency
    )
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_relation.quality < original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], RelationSelector)
