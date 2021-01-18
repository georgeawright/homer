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
        Location([], super_space),
        parent_space,
        parent_space_2,
        Mock(),
        Mock(),
        0,
    )
    structure.links_out.add(label)
    structure.links_out.add(relation_1)
    structure.links_in.add(relation_2)
    structure.links_in.add(correspondence)
    structure.links_out.add(correspondence)

    assert structure.has_link(label.copy())
    assert structure.has_link(correspondence.copy())
    assert structure.has_link(relation_1.copy())
    assert structure.has_link(relation_2.copy())
