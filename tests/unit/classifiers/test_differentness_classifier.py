import pytest
from unittest.mock import Mock

from homer.classifiers import DifferentnessClassifier
from homer.structure_collection import StructureCollection
from homer.structures import Chunk
from homer.structures.links import Correspondence, Label, Relation


def test_classify_labels_with_different_concept():
    start_concept = Mock()
    start_concept.proximity_to.return_value = 0.1
    start = Label(Mock(), start_concept, Mock(), 1.0)
    end_concept = Mock()
    end = Label(Mock(), end_concept, Mock(), 0.0)
    classifier = DifferentnessClassifier()
    assert 0.9 == classifier.classify({"start": start, "end": end, "concept": Mock()})


def test_classify_labels_with_same_concept():
    concept = Mock()
    concept.proximity_to.return_value = 1.0
    start = Label(Mock(), concept, Mock(), 1.0)
    end = Label(Mock(), concept, Mock(), 0.0)
    classifier = DifferentnessClassifier()
    assert 0.0 == classifier.classify({"start": start, "end": end, "concept": Mock()})


def test_classify_chunks_with_different_labels():
    start = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), links_out=StructureCollection()
    )
    start_label = Label(
        Mock(),
        Mock(),
        Mock(),
        1.0,
    )
    start.links_out.add(start_label)
    end = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), links_out=StructureCollection()
    )
    end_label = Label(
        Mock(),
        Mock(),
        Mock(),
        1.0,
    )
    end.links_out.add(end_label)
    differentness_concept = Mock()
    correspondence = Correspondence(
        start_label,
        end_label,
        Mock(),
        Mock(),
        differentness_concept,
        Mock(),
        Mock(),
        1.0,
    )
    start_label.links_in.add(correspondence)
    start_label.links_out.add(correspondence)
    end_label.links_in.add(correspondence)
    end_label.links_out.add(correspondence)
    classifier = DifferentnessClassifier()
    assert 1.0 == classifier.classify(
        {"start": start, "end": end, "concept": differentness_concept}
    )


def test_classify_chunks_without_different_labels():
    concept = Mock()
    start = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    end = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    differentness_concept = Mock()
    classifier = DifferentnessClassifier()
    assert 0.0 == classifier.classify(
        {"start": start, "end": end, "concept": differentness_concept}
    )


def test_classify_relations_with_different_arguments():
    differentness_concept = Mock()

    start_relation_start = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), links_out=StructureCollection()
    )
    start_relation_start_label = Label(
        Mock(),
        Mock(),
        Mock(),
        1.0,
    )
    start_relation_start.links_out.add(start_relation_start_label)
    end_relation_start = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), links_out=StructureCollection()
    )
    end_relation_start_label = Label(
        Mock(),
        Mock(),
        Mock(),
        1.0,
    )
    end_relation_start.links_out.add(end_relation_start_label)
    start_correspondence = Correspondence(
        start_relation_start_label,
        end_relation_start_label,
        Mock(),
        Mock(),
        differentness_concept,
        Mock(),
        Mock(),
        1.0,
    )
    start_relation_start_label.links_in.add(start_correspondence)
    start_relation_start_label.links_out.add(start_correspondence)
    end_relation_start_label.links_in.add(start_correspondence)
    end_relation_start_label.links_out.add(start_correspondence)

    start_relation_end = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), links_out=StructureCollection()
    )
    start_relation_end_label = Label(
        Mock(),
        Mock(),
        Mock(),
        1.0,
    )
    start_relation_end.links_out.add(start_relation_end_label)
    end_relation_end = Chunk(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), links_out=StructureCollection()
    )
    end_relation_end_label = Label(
        Mock(),
        Mock(),
        Mock(),
        1.0,
    )
    end_relation_end.links_out.add(end_relation_end_label)
    end_correspondence = Correspondence(
        start_relation_start_label,
        end_relation_start_label,
        Mock(),
        Mock(),
        differentness_concept,
        Mock(),
        Mock(),
        1.0,
    )
    start_relation_end_label.links_in.add(end_correspondence)
    start_relation_end_label.links_out.add(end_correspondence)
    end_relation_end_label.links_in.add(end_correspondence)
    end_relation_end_label.links_out.add(end_correspondence)

    start_relation_parent_concept = Mock()
    start_relation_parent_concept.proximity_to.return_value = 0.0
    end_relation_parent_concept = Mock()
    start_relation = Relation(
        start_relation_start,
        start_relation_end,
        start_relation_parent_concept,
        Mock(),
        1.0,
    )
    end_relation = Relation(
        end_relation_start,
        end_relation_end,
        end_relation_parent_concept,
        Mock(),
        1.0,
    )

    classifier = DifferentnessClassifier()
    assert 1.0 == classifier.classify(
        {
            "start": start_relation,
            "end": end_relation,
            "concept": differentness_concept,
        }
    )
