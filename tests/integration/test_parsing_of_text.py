# setup bubble chamber with input words "it is hot"
# label words
# run chunk suggester
# assert follow up is chunk builder
# run chunk builder
# assert vp chunk is built and follow up is chunk evaluator
# assert quality is increased and follow up is chunk selector
# run chunk selector
# assert activation of phrase is increased and follow up is chunk suggester
# run chunk suggester
# assert relevant word is suggested to be added to chunk
# label chunk with vp label
# check s is eventually created

import statistics
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


def test_parsing_of_text():
    logger = Mock()
    bubble_chamber = BubbleChamber.setup(logger)
    chunk_concept = Concept(
        "", "", "chunk", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    suggest_concept = Concept(
        "", "", "suggest", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    build_concept = Concept(
        "", "", "build", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    evaluate_concept = Concept(
        "", "", "evaluate", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    select_concept = Concept(
        "", "", "select", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    bubble_chamber.concepts.add(chunk_concept)
    bubble_chamber.concepts.add(suggest_concept)
    bubble_chamber.concepts.add(build_concept)
    bubble_chamber.concepts.add(evaluate_concept)
    bubble_chamber.concepts.add(select_concept)
    chunk_suggest_link = Relation(
        "", "", chunk_concept, suggest_concept, Mock(), None, Mock()
    )
    chunk_concept.links_out.add(chunk_suggest_link)
    suggest_concept.links_in.add(chunk_suggest_link)
    chunk_build_link = Relation(
        "", "", chunk_concept, build_concept, Mock(), None, Mock()
    )
    chunk_concept.links_out.add(chunk_build_link)
    build_concept.links_in.add(chunk_build_link)
    chunk_evaluate_link = Relation(
        "", "", chunk_concept, evaluate_concept, Mock(), None, Mock()
    )
    chunk_concept.links_out.add(chunk_evaluate_link)
    evaluate_concept.links_in.add(chunk_evaluate_link)
    chunk_select_link = Relation(
        "", "", chunk_concept, select_concept, Mock(), None, Mock()
    )
    chunk_concept.links_out.add(chunk_select_link)
    select_concept.links_in.add(chunk_select_link)

    grammar_vectors = {
        "sentence": [],
        "np": [],
        "vp": [],
        "pronoun": [],
        "adj": [],
        "cop": [],
    }
    for index, concept in enumerate(grammar_vectors):
        grammar_vectors[concept] = [0 for _ in grammar_vectors]
        grammar_vectors[concept][index] = 1

    grammar_concept = Concept(
        "",
        "",
        "grammar",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    grammar_space = ConceptualSpace(
        "",
        "",
        "grammar",
        grammar_concept,
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    bubble_chamber.contextual_spaces.add(grammar_space)
    sentence_concept = Concept(
        "",
        "",
        "sentence",
        [Location([grammar_vectors["sentence"]], grammar_space)],
        ProximityClassifier(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(sentence_concept)
    np_concept = Concept(
        "",
        "",
        "np",
        [Location([grammar_vectors["np"]], grammar_space)],
        ProximityClassifier(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(np_concept)
    vp_concept = Concept(
        "",
        "",
        "vp",
        [Location([grammar_vectors["vp"]], grammar_space)],
        ProximityClassifier(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(vp_concept)
    pronoun_concept = Concept(
        "",
        "",
        "pronoun",
        [Location([grammar_vectors["pronoun"]], grammar_space)],
        ProximityClassifier(),
        Word,
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(pronoun_concept)
    cop_concept = Concept(
        "",
        "",
        "cop",
        [Location([grammar_vectors["cop"]], grammar_space)],
        ProximityClassifier(),
        Word,
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(cop_concept)
    adj_concept = Concept(
        "",
        "",
        "adj",
        [Location([grammar_vectors["adj"]], grammar_space)],
        ProximityClassifier(),
        Word,
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(adj_concept)
    s_np_vp_rule = Rule(
        "",
        "",
        "s-->np,vp",
        Location([], grammar_space),
        sentence_concept,
        np_concept,
        vp_concept,
    )
    bubble_chamber.rules.add(s_np_vp_rule)
    sentence_to_s_np_vp = Relation(
        "", "", sentence_concept, s_np_vp_rule, Mock(), grammar_space, Mock()
    )
    sentence_concept.links_out.add(sentence_to_s_np_vp)
    s_np_vp_rule.links_in.add(sentence_to_s_np_vp)
    s_np_vp_to_np = Relation(
        "", "", s_np_vp_rule, np_concept, Mock(), grammar_space, Mock()
    )
    s_np_vp_rule.links_out.add(s_np_vp_to_np)
    np_concept.links_in.add(s_np_vp_to_np)
    s_np_vp_to_vp = Relation(
        "", "", s_np_vp_rule, vp_concept, Mock(), grammar_space, Mock()
    )
    s_np_vp_rule.links_out.add(s_np_vp_to_vp)
    vp_concept.links_in.add(s_np_vp_to_vp)
    np_pronoun_rule = Rule(
        "",
        "",
        "np-->pronoun",
        Location([], grammar_space),
        np_concept,
        pronoun_concept,
        None,
    )
    bubble_chamber.rules.add(np_pronoun_rule)
    np_to_np_pronoun = Relation(
        "", "", np_concept, np_pronoun_rule, Mock(), grammar_space, Mock()
    )
    np_concept.links_out.add(np_to_np_pronoun)
    np_pronoun_rule.links_in.add(np_to_np_pronoun)
    np_pronoun_to_pronoun = Relation(
        "", "", np_pronoun_rule, pronoun_concept, Mock(), grammar_space, Mock()
    )
    np_pronoun_rule.links_out.add(np_pronoun_to_pronoun)
    pronoun_concept.links_in.add(np_pronoun_to_pronoun)
    vp_cop_adj_rule = Rule(
        "",
        "",
        "vp-->cop,adj",
        Location([], grammar_space),
        vp_concept,
        cop_concept,
        adj_concept,
    )
    bubble_chamber.rules.add(vp_cop_adj_rule)
    vp_to_vp_cop_adj = Relation(
        "", "", vp_concept, vp_cop_adj_rule, Mock(), grammar_space, Mock()
    )
    vp_concept.links_out.add(vp_to_vp_cop_adj)
    vp_cop_adj_rule.links_in.add(vp_to_vp_cop_adj)
    vp_cop_adj_to_cop = Relation(
        "", "", vp_cop_adj_rule, cop_concept, Mock(), grammar_space, Mock()
    )
    vp_cop_adj_rule.links_out.add(vp_cop_adj_to_cop)
    cop_concept.links_in.add(vp_cop_adj_to_cop)
    vp_cop_adj_to_adj = Relation(
        "", "", vp_cop_adj_rule, adj_concept, Mock(), grammar_space, Mock()
    )
    vp_cop_adj_rule.links_out.add(vp_cop_adj_to_adj)
    adj_concept.links_in.add(vp_cop_adj_to_adj)
    vp_cop_rule = Rule(
        "",
        "",
        "vp-->cop",
        Location([], grammar_space),
        vp_concept,
        cop_concept,
        None,
    )
    bubble_chamber.rules.add(vp_cop_rule)
    vp_to_vp_cop = Relation(
        "", "", vp_concept, vp_cop_rule, Mock(), grammar_space, Mock()
    )
    vp_concept.links_out.add(vp_to_vp_cop)
    vp_cop_rule.links_in.add(vp_to_vp_cop)
    vp_cop_to_cop = Relation(
        "", "", vp_cop_rule, cop_concept, Mock(), grammar_space, Mock()
    )
    vp_cop_rule.links_out.add(vp_cop_to_cop)
    cop_concept.links_in.add(vp_cop_rule)
    # how to make a rule with one branch that doesn't have unlimited members?
    # maybe that isn't necessary as there won't be a load of the same thing next to each other
    # except adjectives
    it_lexeme = Lexeme("", "", "it", {WordForm.HEADWORD: "it"})
    is_lexeme = Lexeme("", "", "is", {WordForm.HEADWORD: "is"})
    warm_lexeme = Lexeme("", "", "warm", {WordForm.HEADWORD: "warm"})
    it_word = Word(
        "",
        "",
        "it",
        it_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["pronoun"]], grammar_space)],
        grammar_space,
        1,
    )
    is_word = Word(
        "",
        "",
        "is",
        is_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["cop"]], grammar_space)],
        grammar_space,
        1,
    )
    warm_word = Word(
        "",
        "",
        "warm",
        warm_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["adj"]], grammar_space)],
        grammar_space,
        1,
    )
    output_space = ContextualSpace(
        "",
        "",
        "output",
        Mock(),
        StructureCollection(),
        conceptual_spaces=StructureCollection({grammar_space}),
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
        StructureCollection({word_1}),
        output_space,
        0,
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
