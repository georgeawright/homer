import pytest
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import LabelBuilder
from homer.codelets.evaluators import LabelEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Concept
from homer.tools import hasinstance


def test_fizzles_if_label_exists(bubble_chamber):
    bubble_chamber.conceptual_spaces = {"magnitude": Mock()}
    target_node = Mock()
    target_node.has_label.return_value = True

    target_structures = {"target_node": target_node}

    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_structures, 1.0)
    label_builder.run()
    assert CodeletResult.FIZZLE == label_builder.result


def test_creates_new_label(bubble_chamber):
    bubble_chamber.conceptual_spaces = {"magnitude": Mock()}
    target_node = Mock()
    target_node.is_link = False
    target_node.has_label.return_value = False

    parent_concept = Mock()
    parent_concept.has_relation_with.return_value = False
    parent_concept.parent_space.contents = [target_node]

    target_structures = {"target_node": target_node, "parent_concept": parent_concept}

    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_structures, 1.0)
    label_builder.run()
    assert 1 == len(label_builder.child_structures)
    assert CodeletResult.FINISH == label_builder.result


def test_copies_label_and_adds_label(bubble_chamber):
    bubble_chamber.conceptual_spaces = {"magnitude": Mock()}
    node = Mock()
    node.is_link = False
    node.is_node = True
    label = Mock()
    label.is_link = True
    label.is_node = False
    label.start = node
    label.has_label.return_value = False
    node.labels = bubble_chamber.new_structure_collection(label)
    label.labels = bubble_chamber.new_structure_collection()

    parent_concept = Mock()
    parent_concept.has_relation_with.return_value = False
    parent_concept.parent_space.contents = [label]

    target_structures = {"target_node": label, "parent_concept": parent_concept}

    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_structures, 1.0)
    label_builder.run()
    assert 2 == len(label_builder.child_structures)
    assert CodeletResult.FINISH == label_builder.result


def test_copies_labels_label_and_adds_label(bubble_chamber):
    bubble_chamber.conceptual_spaces = {"magnitude": Mock()}
    node = Mock()
    node.is_link = False
    node.is_node = True

    label = Mock()
    label.is_link = True
    label.is_node = False
    label.start = node
    node.labels = bubble_chamber.new_structure_collection(label)

    label_label = Mock()
    label_label.is_link = True
    label_label.is_node = False
    label_label.start = label
    label_label.has_label.return_value = False
    label.labels = bubble_chamber.new_structure_collection(label_label)
    label_label.labels = bubble_chamber.new_structure_collection()

    parent_concept = Mock()
    parent_concept.has_relation_with.return_value = False
    parent_concept.parent_space.contents = [label_label]

    target_structures = {"target_node": label_label, "parent_concept": parent_concept}

    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_structures, 1.0)
    label_builder.run()
    assert 3 == len(label_builder.child_structures)
    assert CodeletResult.FINISH == label_builder.result
