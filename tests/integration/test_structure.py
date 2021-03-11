from unittest.mock import Mock

from homer.location import Location
from homer.structure import Structure
from homer.structures.links import Correspondence, Label, Relation


def test_has_link():
    parent_space = Mock()
    parent_space_2 = Mock()
    super_space = Mock()
    super_space.sub_spaces = [parent_space, parent_space_2]
    structure = Structure("", "", [Location([], parent_space)], 0)
    structure_2 = Structure("", "", [Location([], parent_space_2)], 0)
    label = Label("", "", structure, Mock(), parent_space, 0)
    relation_1 = Relation("", "", structure, Mock(), Mock(), parent_space, 0)
    relation_2 = Relation("", "", Mock(), structure, Mock(), parent_space, 0)
    correspondence = Correspondence(
        "",
        "",
        structure,
        structure_2,
        parent_space,
        parent_space_2,
        [structure.location, structure_2.location],
        Mock(),
        Mock(),
        Mock(),
        0,
    )

    assert not structure.has_link(label)
    structure.links_out.add(label)
    assert structure.has_link(label)
    assert structure.has_link(label.copy())

    assert not structure.has_link(relation_1)
    structure.links_out.add(relation_1)
    assert structure.has_link(relation_1)
    assert structure.has_link(relation_1.copy())

    assert not structure.has_link(relation_2)
    structure.links_in.add(relation_2)
    assert structure.has_link(relation_2)
    assert structure.has_link(relation_2.copy())

    assert not structure.has_link(correspondence)
    structure.links_in.add(correspondence)
    structure.links_out.add(correspondence)
    assert structure.has_link(correspondence)
    assert structure.has_link(correspondence.copy())

    label_copy = label.copy()
    relation_1_copy = relation_1.copy()
    relation_2_copy = relation_2.copy()
    correspondence_copy = correspondence.copy()

    new_structure = Structure("", "", [Location([], parent_space)], 0)

    assert not new_structure.has_link(label, start=structure)
    new_structure.links_out.add(label_copy)
    assert new_structure.has_link(label, start=structure)

    assert not new_structure.has_link(relation_1, start=structure)
    new_structure.links_out.add(relation_1_copy)
    assert new_structure.has_link(relation_1, start=structure)

    assert not new_structure.has_link(relation_2, start=structure)
    new_structure.links_in.add(relation_2_copy)
    assert new_structure.has_link(relation_2, start=structure)

    assert not new_structure.has_link(correspondence, start=structure)
    new_structure.links_in.add(correspondence_copy)
    new_structure.links_out.add(correspondence_copy)
    assert new_structure.has_link(correspondence, start=structure)
