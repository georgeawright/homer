import pytest
from unittest.mock import Mock

from linguoplotter.codelets.factories import ViewDrivenFactory
from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    LabelSuggester,
    RelationSuggester,
)
from linguoplotter.codelets.suggesters.view_suggesters import SimplexViewSuggester
from linguoplotter.structure_collection import StructureCollection


def test_get_follow_up_class_returns_codelet_class(bubble_chamber):
    coderack = Mock()

    label = Mock()
    label.is_label = True
    label.is_relation = False
    label.is_chunk = False
    label.is_view = False

    relation = Mock()
    relation.is_label = False
    relation.is_relation = True
    relation.is_chunk = False
    relation.is_view = False

    chunk = Mock()
    chunk.is_label = False
    chunk.is_relation = False
    chunk.is_chunk = True
    chunk.is_view = False

    view = Mock()
    view.is_label = False
    view.is_relation = False
    view.is_chunk = False
    view.is_view = True

    factory_codelet = ViewDrivenFactory(
        Mock(), Mock(), bubble_chamber, coderack, Mock()
    )

    assert LabelSuggester == factory_codelet._get_follow_up_class(label)
    assert RelationSuggester == factory_codelet._get_follow_up_class(relation)
    assert ChunkSuggester == factory_codelet._get_follow_up_class(chunk)
    assert SimplexViewSuggester == factory_codelet._get_follow_up_class(view)
