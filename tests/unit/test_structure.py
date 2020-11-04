from unittest.mock import Mock

from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures.links import Label


def test_labels_returns_labels():
    number_of_labels = 10
    links_out = StructureCollection()
    for _ in range(number_of_labels):
        label = Label(Mock(), Mock())
        links_out.add(label)
    for _ in range(number_of_labels):
        non_label = Mock()
        links_out.add(non_label)
    structure = Structure(Mock(), links_out=links_out)
    assert number_of_labels == len(structure.labels)
    for label in structure.labels:
        assert isinstance(label, Label)
