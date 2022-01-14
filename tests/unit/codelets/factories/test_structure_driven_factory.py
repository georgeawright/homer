import pytest
from unittest.mock import Mock

from homer.codelets.factories import StructureDrivenFactory
from homer.codelets.suggesters import ChunkSuggester, LabelSuggester, RelationSuggester
from homer.codelets.suggesters.correspondence_suggesters import (
    SpaceToFrameCorrespondenceSuggester,
)


def test_get_follow_up_class_returns_codelet_class(bubble_chamber):
    coderack = Mock()

    unlabeled_structure = Mock()
    unlabeled_structure.unlabeledness = 1.0
    unlabeled_structure.unrelatedness = 0.0
    unlabeled_structure.uncorrespondedness = 0.0
    unlabeled_structure.unchunkedness = 0.0

    unrelated_structure = Mock()
    unrelated_structure.unlabeledness = 0.0
    unrelated_structure.unrelatedness = 1.0
    unrelated_structure.uncorrespondedness = 0.0
    unrelated_structure.unchunkedness = 0.0

    uncorresponded_structure = Mock()
    uncorresponded_structure.unlabeledness = 0.0
    uncorresponded_structure.unrelatedness = 0.0
    uncorresponded_structure.uncorrespondedness = 1.0
    uncorresponded_structure.unchunkedness = 0.0

    unchunked_structure = Mock()
    unchunked_structure.unlabeledness = 0.0
    unchunked_structure.unrelatedness = 0.0
    unchunked_structure.uncorrespondedness = 0.0
    unchunked_structure.unchunkedness = 1.0

    factory_codelet = StructureDrivenFactory(
        Mock(), Mock(), bubble_chamber, coderack, Mock()
    )

    assert LabelSuggester == factory_codelet._get_follow_up_class(
        unlabeled_structure,
    )
    assert RelationSuggester == factory_codelet._get_follow_up_class(
        unrelated_structure,
    )
    assert SpaceToFrameCorrespondenceSuggester == factory_codelet._get_follow_up_class(
        uncorresponded_structure,
    )
    assert ChunkSuggester == factory_codelet._get_follow_up_class(
        unchunked_structure,
    )
