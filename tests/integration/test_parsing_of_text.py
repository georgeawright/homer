import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import ProximityClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder
from homer.codelets.evaluators import ChunkEvaluator
from homer.codelets.selectors import ChunkSelector
from homer.codelets.suggesters import ChunkSuggester
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Rule, Word
from homer.structures.spaces import ConceptualSpace, ContextualSpace
from homer.tools import centroid_euclidean_distance
from homer.word_form import WordForm


def test_parsing_of_text(
    bubble_chamber,
    grammar_concept,
    grammar_space,
    sentence_concept,
    np_concept,
    vp_concept,
    pronoun_concept,
    cop_concept,
    adj_concept,
    s_np_vp_rule,
    np_pronoun_rule,
    vp_cop_adj_rule,
    vp_cop_rule,
    it_lexeme,
    is_lexeme,
    warm_lexeme,
    it_word,
    is_word,
    warm_word,
):
    output_space = ContextualSpace(
        "",
        "",
        "output",
        Mock(),
        bubble_chamber.new_structure_collection(),
        conceptual_spaces=bubble_chamber.new_structure_collection(grammar_space),
        links_in=bubble_chamber.new_structure_collection(),
        links_out=bubble_chamber.new_structure_collection(),
        parent_spaces=bubble_chamber.new_structure_collection(),
    )

    # create text to be parsed
    word_1 = Word(
        "",
        "",
        "it",
        it_lexeme,
        WordForm.HEADWORD,
        it_word.locations + [Location([[0]], output_space)],
        output_space,
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    output_space.add(word_1)
    grammar_space.add(word_1)
    word_2 = Word(
        "",
        "",
        "is",
        is_lexeme,
        WordForm.HEADWORD,
        is_word.locations + [Location([[1]], output_space)],
        output_space,
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    output_space.add(word_2)
    grammar_space.add(word_2)
    word_3 = Word(
        "",
        "",
        "warm",
        warm_lexeme,
        WordForm.HEADWORD,
        warm_word.locations + [Location([[2]], output_space)],
        output_space,
        1,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    output_space.add(word_3)
    grammar_space.add(word_3)

    # create chunk suggester
    suggester = ChunkSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_space": output_space,
            "target_node": word_1,
            "target_rule": None,
        },
        1,
    )

    # run chunk suggester
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result

    # assert follow up is chunk builder
    builder = suggester.child_codelets[0]
    assert isinstance(builder, ChunkBuilder)

    # run chunk builder
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    chunk = builder.child_structures.where(is_slot=False).get()
    original_chunk_quality = chunk.quality
    original_chunk_activation = chunk.activation

    # assert follow up is chunk evaluator
    evaluator = builder.child_codelets[0]
    assert isinstance(evaluator, ChunkEvaluator)

    # run chunk evaluator
    evaluator.run()

    # assert quality is increased and follow up is chunk selector
    assert chunk.quality > original_chunk_quality
    selector = evaluator.child_codelets[0]
    assert isinstance(selector, ChunkSelector)

    # build alternative chunk
    alternative_chunk = Chunk(
        "",
        "",
        [
            Location([[0]], output_space),
        ],
        bubble_chamber.new_structure_collection(word_1),
        output_space,
        0,
        bubble_chamber.new_structure_collection(word_1),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    original_alternative_chunk_activation = alternative_chunk.activation

    # run chunk selector
    selector.run()
    chunk.update_activation()
    alternative_chunk.update_activation()

    # assert high quality chunk is preferred and follow up is chunk suggester
    assert chunk.activation > original_chunk_activation
    assert alternative_chunk.activation <= original_alternative_chunk_activation
    suggester_2 = selector.child_codelets[0]
    assert isinstance(suggester_2, ChunkSuggester)

    # run chunk suggester
    suggester_2.run()
    if CodeletResult.SUCCESS == suggester_2.result:
        builder_2 = suggester_2.child_codelets[0]
        assert isinstance(builder_2, ChunkBuilder)
    else:
        assert CodeletResult.FIZZLE == suggester_2.result
