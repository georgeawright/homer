import pytest
from unittest.mock import Mock

from linguoplotter.codelets.suggesters import (
    ChunkSuggester,
    LabelSuggester,
    RelationSuggester,
)
from linguoplotter.codelets.suggesters.correspondence_suggesters import (
    SpaceToFrameCorrespondenceSuggester,
)
from linguoplotter.codelets.factories import ConceptDrivenFactory
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Correspondence, Label, Relation


def test_gets_appropriate_follow_up_class(bubble_chamber):
    example_correspondence_concept = Mock()
    example_correspondence_concept.structure_type = Correspondence
    bubble_chamber.concepts.add(example_correspondence_concept)

    example_label_concept = Mock()
    example_label_concept.structure_type = Label
    bubble_chamber.concepts.add(example_label_concept)

    example_relation_concept = Mock()
    example_relation_concept.structure_type = Relation
    bubble_chamber.concepts.add(example_relation_concept)

    example_rule = Mock()
    bubble_chamber.rules.add(example_rule)

    coderack = Mock()

    factory_codelet = ConceptDrivenFactory(
        Mock(), Mock(), bubble_chamber, coderack, Mock()
    )

    assert factory_codelet._get_follow_up_class(example_label_concept) == LabelSuggester
    assert (
        factory_codelet._get_follow_up_class(example_relation_concept)
        == RelationSuggester
    )
    assert factory_codelet._get_follow_up_class(example_rule) == ChunkSuggester
