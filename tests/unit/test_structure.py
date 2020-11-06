from unittest.mock import Mock

from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Lexeme
from homer.structures.links import Label, Relation


def test_labels_returns_labels():
    number_of_labels = 10
    links_out = StructureCollection()
    for _ in range(number_of_labels):
        label = Label(Mock(), Mock(), Mock())
        links_out.add(label)
    for _ in range(number_of_labels):
        links_out.add(Mock())
    structure = Structure(Mock(), Mock(), links_out=links_out)
    assert number_of_labels == len(structure.labels)
    for label in structure.labels:
        assert isinstance(label, Label)


def test_lexemes_returns_lexemes():
    structure = Structure(Mock(), Mock())
    number_of_lexemes = 10
    for _ in range(number_of_lexemes):
        lexeme = Lexeme(Mock(), Mock())
        relation = Relation(structure, lexeme, Mock(), Mock())
        structure.links_out.add(relation)
    for _ in range(number_of_lexemes):
        structure.links_out.add(Mock())
    assert number_of_lexemes == len(structure.lexemes)
    for lexeme in structure.lexemes:
        assert isinstance(lexeme, Lexeme)
