import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.label_builders import LabelProjectionBuilder
from homer.codelets.suggesters.label_suggesters import LabelProjectionSuggester
from homer.structure_collection import StructureCollection
from homer.structures.links import Label


@pytest.fixture
def target_view():
    potential_labeling_word = Mock()
    potential_labeling_word.unlinkedness = 0.5
    potential_labeling_word.correspondences_to_space.return_value = StructureCollection(
        {Mock()}
    )
    potential_labeling_word.name = "potential labeling word"
    word = Mock()
    word.name = "existing word"
    word.potential_labeling_words = StructureCollection({potential_labeling_word})
    correspondence = Mock()
    correspondence.name = "existing correspondence"
    chunk = Mock()
    chunk.unlinkedness = 0.5
    chunk.name = "existing chunk"
    correspondence.arguments = StructureCollection({chunk, word})
    chunk.is_chunk = True
    chunk.correspondences_to_space.return_value = StructureCollection({correspondence})
    view = Mock()
    view.name = "monitoring view"
    view.interpretation_space.contents = StructureCollection({chunk})
    return view


@pytest.fixture
def bubble_chamber(target_view):
    chamber = Mock()
    chamber.concepts = {
        "suggest": Mock(),
        "label": Mock(),
        "noun": Mock(),
        "same": Mock(),
        "text": Mock(),
    }
    chamber.monitoring_views = StructureCollection({target_view})
    return chamber


@pytest.fixture
def parent_concept(bubble_chamber):
    concept = Mock()
    label_concepts = Mock()
    label_concepts.contents = StructureCollection({concept.parent_space})
    bubble_chamber.spaces = {"label concepts": label_concepts}
    target_space = Mock()
    target_space.parent_concept.relevant_value = "value"
    target_space.contents = StructureCollection()
    concept.parent_space.instance_in_space.return_value = target_space
    return concept


@pytest.fixture
def target_word(bubble_chamber, parent_concept):
    word = Mock()
    word.correspondences_to_space.return_value = StructureCollection()
    word.lexeme.concepts.get.return_value = parent_concept
    return word


def test_gives_high_confidence_for_word_with_labeling_concept(
    bubble_chamber, target_view, target_word
):
    target_chunk = Mock()
    target_chunk.has_label.return_value = False
    target_word.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_chunk": target_chunk,
        "target_word": target_word,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1)
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert suggester.confidence == 1
    assert len(suggester.child_codelets) == 1
    assert isinstance(suggester.child_codelets[0], LabelProjectionBuilder)


def test_fizzles_if_target_word_already_has_correspondence_in_interpretation(
    bubble_chamber, target_view, target_word
):
    target_chunk = Mock()
    target_chunk.has_label.return_value = False
    correspondence = Mock()
    label = Label(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    correspondence.arguments = StructureCollection({target_word, label})
    target_word.correspondences_to_space.return_value = StructureCollection(
        {correspondence}
    )
    target_structures = {
        "target_view": target_view,
        "target_chunk": target_chunk,
        "target_word": target_word,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result


def test_fizzles_if_target_chunk_already_has_corresponding_label(
    bubble_chamber, target_view, target_word
):
    target_chunk = Mock()
    target_chunk.has_label.return_value = True
    target_word.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_chunk": target_chunk,
        "target_word": target_word,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result
