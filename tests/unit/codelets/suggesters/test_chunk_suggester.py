import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.suggesters import ChunkSuggester
from linguoplotter.codelets.builders import ChunkBuilder
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Label
from linguoplotter.structures.nodes import Chunk
from linguoplotter.tools import hasinstance


@pytest.fixture
def target_slot():
    chunk = Mock()
    chunk.is_slot = True
    return chunk


@pytest.fixture
def target_rule(bubble_chamber):
    rule = Mock()
    rule.compatibility_with.return_value = 1.0
    rule.root_concept.classifier.classify.return_value = 1.0
    rule.left_concept.classifier.classify.return_value = 1.0
    rule.right_concept.classifier.classify.return_value = 1.0
    return rule


@pytest.fixture
def target_root(bubble_chamber, target_slot, target_rule):
    chunk = Mock()
    chunk.name = "target_root"
    chunk.members = bubble_chamber.new_structure_collection(target_slot)
    chunk.rule = target_rule
    return chunk


@pytest.fixture
def target_node(bubble_chamber, target_root):
    chunk = Mock()
    chunk.is_slot = False
    chunk.super_chunks = bubble_chamber.new_structure_collection(target_root)
    target_root.members.add(chunk)
    return chunk


def test_bottom_up_chunk_suggester_gets_target_rule(bubble_chamber, target_node):
    target_structures = {
        "target_space": Mock(),
        "target_rule": None,
        "target_root": None,
        "target_node": target_node,
        "target_slot": None,
        "target_slot_filler": None,
    }
    urgency = 1
    suggester = ChunkSuggester("", "", bubble_chamber, target_structures, urgency)
    assert suggester.target_rule is None
    suggester.run()
    assert suggester.target_rule is not None


def test_bottom_up_chunk_suggester_with_root_gets_slot_and_filler(
    bubble_chamber, target_node
):
    target_structures = {
        "target_space": Mock(),
        "target_rule": None,
        "target_root": None,
        "target_node": target_node,
        "target_slot": None,
        "target_slot_filler": None,
    }
    urgency = 1
    suggester = ChunkSuggester("", "", bubble_chamber, target_structures, urgency)
    assert suggester.target_root is None
    assert suggester.target_slot is None
    assert suggester.target_slot_filler is None
    suggester.run()
    assert suggester.target_root is not None
    assert suggester.target_slot is not None
    assert suggester.target_slot_filler is not None


def test_fizzles_if_chunk_exists(bubble_chamber, target_node):
    target_rule = Mock()
    existing_chunk = Mock()
    existing_chunk.rule = target_rule
    target_slot_filler = Mock()
    existing_chunk.members = StructureCollection(
        Mock(), [target_node, target_slot_filler]
    )
    bubble_chamber.chunks.add(existing_chunk)
    target_space = Mock()
    contents_where = Mock()
    contents_where.at = StructureCollection(Mock(), [target_slot_filler])
    target_space.contents.where.return_value = contents_where
    target_structures = {
        "target_space": Mock(),
        "target_rule": target_rule,
        "target_root": None,
        "target_node": target_node,
        "target_slot": None,
        "target_slot_filler": None,
    }
    urgency = 1
    suggester = ChunkSuggester("", "", bubble_chamber, target_structures, urgency)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result


@pytest.mark.parametrize("compatibility", [(1.0), (0.5), (0.0)])
def test_has_high_confidence_for_root_compatible_with_rule(
    bubble_chamber,
    target_node,
    compatibility,
):
    target_rule = Mock()
    target_rule.root_concept.classifier.classify.return_value = compatibility
    target_rule.left_concept.classifier.classify.return_value = compatibility
    target_rule.right_concept.classifier.classify.return_value = compatibility
    target_rule.compatibility_with.return_value = compatibility
    target_structures = {
        "target_space": Mock(),
        "target_rule": target_rule,
        "target_root": None,
        "target_node": target_node,
        "target_slot": None,
        "target_slot_filler": None,
    }
    urgency = 1
    suggester = ChunkSuggester("", "", bubble_chamber, target_structures, urgency)
    suggester.run()
    assert CodeletResult.FINISH == suggester.result
    assert compatibility == suggester.confidence
    assert compatibility == suggester.child_codelets[0].urgency
