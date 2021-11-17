import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import LabelBuilder
from homer.codelets.evaluators import LabelEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Concept
from homer.tools import hasinstance


@pytest.fixture
def parent_concept():
    concept = Mock()
    concept.is_concept = True
    concept.relevant_value = "value"
    return concept


@pytest.fixture
def target_chunk():
    chunk = Mock()
    chunk.is_chunk = True
    chunk.is_word = False
    chunk.has_label.return_value = False
    chunk.nearby.get_unhappy.return_value = Mock()
    chunk.value = ""
    return chunk


def test_successful_creates_label_and_spawns_follow_up(
    bubble_chamber, target_chunk, parent_concept
):
    target_structures = {"target_node": target_chunk, "parent_concept": parent_concept}
    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_structures, 1.0)
    result = label_builder.run()
    assert CodeletResult.SUCCESS == result
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelEvaluator)


def test_fizzles_when_label_exists(bubble_chamber, target_chunk, parent_concept):
    target_chunk.has_label.return_value = True
    target_structures = {"target_node": target_chunk, "parent_concept": parent_concept}
    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_structures, 1.0)
    result = label_builder.run()
    assert CodeletResult.FIZZLE == result
    assert label_builder.child_structures is None
