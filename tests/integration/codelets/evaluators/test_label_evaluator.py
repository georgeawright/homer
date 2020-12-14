import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import StretchyProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.evaluators import LabelEvaluator
from homer.codelets.selectors import LabelSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Label, Relation
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
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    label_concept = Concept(
        Mock(),
        Mock(),
        "label",
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(label_concept)
    evaluate_concept = Concept(
        Mock(),
        Mock(),
        "evaluate",
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(evaluate_concept)
    relation = Relation(Mock(), Mock(), label_concept, evaluate_concept, None, None, 1)
    label_concept.links_out.add(relation)
    evaluate_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def good_label(bubble_chamber):
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    temperature_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    input_space = WorkingSpace(
        Mock(), Mock(), "input", StructureCollection(), 0, location_concept
    )
    temperature_space = WorkingSpace(
        Mock(), Mock(), "temperature", StructureCollection(), 0, temperature_concept
    )
    warm_concept = Concept(
        Mock(),
        Mock(),
        "warm",
        [15],
        StretchyProximityClassifier(),
        temperature_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    parent_spaces = StructureCollection({input_space, temperature_space})
    start = Chunk(
        Mock(),
        Mock(),
        [15],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    quality = 0.0
    label = Label(Mock(), Mock(), start, warm_concept, temperature_space, quality)
    return label


@pytest.fixture
def bad_label(bubble_chamber):
    location_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "coordinates", Mock(), math.dist
    )
    temperature_concept = Concept(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), "value", Mock(), math.dist
    )
    input_space = WorkingSpace(
        Mock(), Mock(), "input", StructureCollection(), 0, location_concept
    )
    temperature_space = WorkingSpace(
        Mock(), Mock(), "temperature", StructureCollection(), 0, temperature_concept
    )
    warm_concept = Concept(
        Mock(),
        Mock(),
        "warm",
        [15],
        StretchyProximityClassifier(),
        temperature_space,
        "value",
        StructureCollection(),
        math.dist,
    )
    parent_spaces = StructureCollection({input_space, temperature_space})
    start = Chunk(
        Mock(),
        Mock(),
        [10],
        Location([0, 0], input_space),
        StructureCollection(),
        StructureCollection(),
        0.0,
        parent_spaces,
    )
    quality = 1.0
    label = Label(Mock(), Mock(), start, warm_concept, temperature_space, quality)
    return label


def test_increases_quality_of_good_label(bubble_chamber, good_label):
    original_quality = good_label.quality
    parent_id = ""
    urgency = 1.0
    evaluator = LabelEvaluator.spawn(parent_id, bubble_chamber, good_label, urgency)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert good_label.quality > original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], LabelSelector)


def test_decreases_quality_of_bad_label(bubble_chamber, bad_label):
    original_quality = bad_label.quality
    parent_id = ""
    urgency = 1.0
    evaluator = LabelEvaluator.spawn(parent_id, bubble_chamber, bad_label, urgency)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert bad_label.quality < original_quality
    assert 1 == len(evaluator.child_codelets)
    assert isinstance(evaluator.child_codelets[0], LabelSelector)
