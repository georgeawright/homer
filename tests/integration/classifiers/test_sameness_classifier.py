import pytest
from unittest.mock import Mock

from homer.classifiers import SamenessClassifier
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node
from homer.structures.links import Correspondence, Label, Relation


def test_classify_nodes():
    conceptual_space_1 = Mock()
    conceptual_space_2 = Mock()
    working_space_1 = Mock()
    working_space_1.conceptual_space = conceptual_space_1
    working_space_2 = Mock()
    working_space_2.conceptual_space = conceptual_space_2
    working_space_3 = Mock()
    node_1 = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), working_space_1), Location(Mock(), working_space_2)],
        Mock(),
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_2 = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), working_space_1), Location(Mock(), working_space_2)],
        Mock(),
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_3 = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), working_space_1), Location(Mock(), working_space_3)],
        Mock(),
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_1_label_1 = Label(Mock(), Mock(), node_1, Mock(), working_space_1, Mock())
    node_1.links_out.add(node_1_label_1)
    node_1_label_2 = Label(Mock(), Mock(), node_1, Mock(), working_space_2, Mock())
    node_1.links_out.add(node_1_label_2)
    node_2_label_1 = Label(Mock(), Mock(), node_2, Mock(), working_space_1, Mock())
    node_2.links_out.add(node_2_label_1)
    node_2_label_2 = Label(Mock(), Mock(), node_2, Mock(), working_space_2, Mock())
    node_2.links_out.add(node_2_label_2)
    node_3_label_1 = Label(Mock(), Mock(), node_3, Mock(), working_space_1, Mock())
    node_3.links_out.add(node_3_label_1)
    node_3_label_2 = Label(Mock(), Mock(), node_3, Mock(), working_space_3, Mock())
    node_3.links_out.add(node_3_label_2)
    classifier = SamenessClassifier()
    assert classifier.classify(start=node_1, end=node_2) > classifier.classify(
        start=node_1, end=node_3
    )


def test_classify_labels_of_corresponding_nodes():
    space_1 = Mock()
    space_2 = Mock()
    node_1 = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_1)],
        space_1,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_1_label = Label(Mock(), Mock(), node_1, Mock(), space_1, 1)
    node_1.links_out.add(node_1_label)
    node_2 = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_2)],
        space_2,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_2_label = Label(Mock(), Mock(), node_2, Mock(), space_2, 1)
    node_2.links_out.add(node_2_label)
    nodes_correspondence = Correspondence(
        Mock(),
        Mock(),
        node_1,
        node_2,
        space_1,
        space_2,
        [Location(Mock(), space_1), Location(Mock(), space_2)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    node_1.links_out.add(nodes_correspondence)
    node_1.links_in.add(nodes_correspondence)
    node_2.links_out.add(nodes_correspondence)
    node_2.links_in.add(nodes_correspondence)
    classifier = SamenessClassifier()
    assert classifier.classify(start=node_1_label, end=node_2_label) > 0


def test_classify_labels_of_non_corresponding_nodes():
    space_1 = Mock()
    space_2 = Mock()
    node_1 = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_1)],
        space_1,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_1_label = Label(Mock(), Mock(), node_1, Mock(), space_1, 1)
    node_1.links_out.add(node_1_label)
    node_2 = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_2)],
        space_2,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_2_label = Label(Mock(), Mock(), node_2, Mock(), space_2, 1)
    node_2.links_out.add(node_2_label)
    classifier = SamenessClassifier()
    assert classifier.classify(start=node_1_label, end=node_2_label) == 0


def test_classify_relations_of_corresponding_nodes():
    space_1 = Mock()
    space_2 = Mock()
    node_1_a = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_1)],
        space_1,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_1_b = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_1)],
        space_1,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    space_1_relation = Relation(Mock(), Mock(), node_1_a, node_1_b, Mock(), space_1, 1)
    node_1_a.links_out.add(space_1_relation)
    node_1_b.links_in.add(space_1_relation)
    node_2_a = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_2)],
        space_2,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_2_b = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_2)],
        space_2,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    space_2_relation = Relation(Mock(), Mock(), node_2_a, node_2_b, Mock(), space_2, 1)
    node_2_a.links_out.add(space_2_relation)
    node_2_b.links_in.add(space_2_relation)
    nodes_a_correspondence = Correspondence(
        Mock(),
        Mock(),
        node_1_a,
        node_2_a,
        space_1,
        space_2,
        [Location(Mock(), space_1), Location(Mock(), space_2)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    node_1_a.links_out.add(nodes_a_correspondence)
    node_1_a.links_in.add(nodes_a_correspondence)
    node_2_a.links_out.add(nodes_a_correspondence)
    node_2_a.links_in.add(nodes_a_correspondence)
    nodes_b_correspondence = Correspondence(
        Mock(),
        Mock(),
        node_1_b,
        node_2_b,
        space_1,
        space_2,
        [Location(Mock(), space_1), Location(Mock(), space_2)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    node_1_b.links_out.add(nodes_b_correspondence)
    node_1_b.links_in.add(nodes_b_correspondence)
    node_2_b.links_out.add(nodes_b_correspondence)
    node_2_b.links_in.add(nodes_b_correspondence)
    classifier = SamenessClassifier()
    assert classifier.classify(start=space_1_relation, end=space_2_relation) > 0


def test_classify_relations_of_non_corresponding_nodes():
    space_1 = Mock()
    space_2 = Mock()
    node_1_a = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_1)],
        space_1,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_1_b = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_1)],
        space_1,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    space_1_relation = Relation(Mock(), Mock(), node_1_a, node_1_b, Mock(), space_1, 1)
    node_1_a.links_out.add(space_1_relation)
    node_1_b.links_in.add(space_1_relation)
    node_2_a = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_2)],
        space_2,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    node_2_b = Node(
        Mock(),
        Mock(),
        Mock(),
        [Location(Mock(), space_2)],
        space_2,
        Mock(),
        StructureCollection(),
        StructureCollection(),
    )
    space_2_relation = Relation(Mock(), Mock(), node_2_a, node_2_b, Mock(), space_2, 1)
    node_2_a.links_out.add(space_2_relation)
    node_2_b.links_in.add(space_2_relation)
    nodes_a_correspondence = Correspondence(
        Mock(),
        Mock(),
        node_1_a,
        node_2_a,
        space_1,
        space_2,
        [Location(Mock(), space_1), Location(Mock(), space_2)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    node_1_a.links_out.add(nodes_a_correspondence)
    node_1_a.links_in.add(nodes_a_correspondence)
    node_2_a.links_out.add(nodes_a_correspondence)
    node_2_a.links_in.add(nodes_a_correspondence)
    classifier = SamenessClassifier()
    assert classifier.classify(start=space_1_relation, end=space_2_relation) == 0
