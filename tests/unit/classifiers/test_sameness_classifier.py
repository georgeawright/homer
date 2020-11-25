from unittest.mock import Mock

from homer.classifiers import SamenessClassifier
from homer.structure_collection import StructureCollection
from homer.structures import Chunk
from homer.structures.links import Correspondence, Label, Relation


def test_classify_labels_with_same_concept():
    concept = Mock()
    start = Label(Mock(), Mock(), Mock(), concept, Mock(), 1.0)
    end = Label(Mock(), Mock(), Mock(), concept, Mock(), 0.0)
    classifier = SamenessClassifier()
    assert 0.5 == classifier.classify({"start": start, "end": end, "concept": Mock()})


def test_classify_labels_with_different_concept():
    start = Label(Mock(), Mock(), Mock(), Mock(), Mock(), 1.0)
    end = Label(Mock(), Mock(), Mock(), Mock(), Mock(), 0.0)
    classifier = SamenessClassifier()
    assert 0.0 == classifier.classify({"start": start, "end": end, "concept": Mock()})


def test_classify_chunks_with_same_labels():
    concept = Mock()
    start = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        links_out=StructureCollection(),
    )
    start_label = Label(
        Mock(),
        Mock(),
        Mock(),
        concept,
        Mock(),
        1.0,
    )
    start.links_out.add(start_label)
    end = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        links_out=StructureCollection(),
    )
    end_label = Label(
        Mock(),
        Mock(),
        Mock(),
        concept,
        Mock(),
        1.0,
    )
    end.links_out.add(end_label)
    sameness_concept = Mock()
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start_label,
        end_label,
        Mock(),
        Mock(),
        sameness_concept,
        Mock(),
        Mock(),
        1.0,
    )
    start_label.links_in.add(correspondence)
    start_label.links_out.add(correspondence)
    end_label.links_in.add(correspondence)
    end_label.links_out.add(correspondence)
    classifier = SamenessClassifier()
    assert 1.0 == classifier.classify(
        {"start": start, "end": end, "concept": sameness_concept}
    )


def test_classify_chunks_without_same_labels():
    concept = Mock()
    start = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    end = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    sameness_concept = Mock()
    classifier = SamenessClassifier()
    assert 0.0 == classifier.classify(
        {"start": start, "end": end, "concept": sameness_concept}
    )


def test_classify_relations_with_same_arguments():
    sameness_concept = Mock()

    start_concept = Mock()
    start_relation_start = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        links_out=StructureCollection(),
    )
    start_relation_start_label = Label(
        Mock(),
        Mock(),
        Mock(),
        start_concept,
        Mock(),
        1.0,
    )
    start_relation_start.links_out.add(start_relation_start_label)
    end_relation_start = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        links_out=StructureCollection(),
    )
    end_relation_start_label = Label(
        Mock(),
        Mock(),
        Mock(),
        start_concept,
        Mock(),
        1.0,
    )
    end_relation_start.links_out.add(end_relation_start_label)
    start_correspondence = Correspondence(
        Mock(),
        Mock(),
        start_relation_start_label,
        end_relation_start_label,
        Mock(),
        Mock(),
        sameness_concept,
        Mock(),
        Mock(),
        1.0,
    )
    start_relation_start_label.links_in.add(start_correspondence)
    start_relation_start_label.links_out.add(start_correspondence)
    end_relation_start_label.links_in.add(start_correspondence)
    end_relation_start_label.links_out.add(start_correspondence)

    end_concept = Mock()
    start_relation_end = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        links_out=StructureCollection(),
    )
    start_relation_end_label = Label(
        Mock(),
        Mock(),
        Mock(),
        end_concept,
        Mock(),
        1.0,
    )
    start_relation_end.links_out.add(start_relation_end_label)
    end_relation_end = Chunk(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        links_out=StructureCollection(),
    )
    end_relation_end_label = Label(
        Mock(),
        Mock(),
        Mock(),
        end_concept,
        Mock(),
        1.0,
    )
    end_relation_end.links_out.add(end_relation_end_label)
    end_correspondence = Correspondence(
        Mock(),
        Mock(),
        start_relation_start_label,
        end_relation_start_label,
        Mock(),
        Mock(),
        sameness_concept,
        Mock(),
        Mock(),
        1.0,
    )
    start_relation_end_label.links_in.add(end_correspondence)
    start_relation_end_label.links_out.add(end_correspondence)
    end_relation_end_label.links_in.add(end_correspondence)
    end_relation_end_label.links_out.add(end_correspondence)

    relation_parent_concept = Mock()
    start_relation = Relation(
        Mock(),
        Mock(),
        start_relation_start,
        start_relation_end,
        relation_parent_concept,
        Mock(),
        1.0,
    )
    end_relation = Relation(
        Mock(),
        Mock(),
        end_relation_start,
        end_relation_end,
        relation_parent_concept,
        Mock(),
        1.0,
    )

    classifier = SamenessClassifier()
    assert 1.0 == classifier.classify(
        {"start": start_relation, "end": end_relation, "concept": sameness_concept}
    )
