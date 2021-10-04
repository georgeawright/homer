import math
import pytest
import statistics
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import ProximityClassifier, SamenessClassifier
from homer.id import ID
from homer.location import Location
from homer.locations import TwoPointLocation
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Lexeme, Rule, Word
from homer.structures.spaces import ConceptualSpace, ContextualSpace, Frame
from homer.tools import add_vectors, centroid_euclidean_distance
from homer.word_form import WordForm


@pytest.fixture(scope="module")
def bubble_chamber():
    logger = Mock()
    chamber = BubbleChamber.setup(logger)
    chunk_concept = Concept(
        "", "", "chunk", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    correspondence_concept = Concept(
        "", "", "correspondence", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    label_concept = Concept(
        "", "", "label", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    relation_concept = Concept(
        "", "", "relation", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    view_simplex_concept = Concept(
        "", "", "view-simplex", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    )
    view_monitoring_concept = Concept(
        "",
        "",
        "view-monitoring",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    word_concept = Concept(
        "", "", "word", Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
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
    chamber.concepts.add(chunk_concept)
    chamber.concepts.add(correspondence_concept)
    chamber.concepts.add(label_concept)
    chamber.concepts.add(relation_concept)
    chamber.concepts.add(view_simplex_concept)
    chamber.concepts.add(view_monitoring_concept)
    chamber.concepts.add(word_concept)
    chamber.concepts.add(suggest_concept)
    chamber.concepts.add(build_concept)
    chamber.concepts.add(evaluate_concept)
    chamber.concepts.add(select_concept)
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
    correspondence_suggest_link = Relation(
        "", "", correspondence_concept, suggest_concept, Mock(), None, Mock()
    )
    correspondence_concept.links_out.add(correspondence_suggest_link)
    suggest_concept.links_in.add(correspondence_suggest_link)
    correspondence_build_link = Relation(
        "", "", correspondence_concept, build_concept, Mock(), None, Mock()
    )
    correspondence_concept.links_out.add(correspondence_build_link)
    build_concept.links_in.add(correspondence_build_link)
    correspondence_evaluate_link = Relation(
        "", "", correspondence_concept, evaluate_concept, Mock(), None, Mock()
    )
    correspondence_concept.links_out.add(correspondence_evaluate_link)
    evaluate_concept.links_in.add(correspondence_evaluate_link)
    correspondence_select_link = Relation(
        "", "", correspondence_concept, select_concept, Mock(), None, Mock()
    )
    correspondence_concept.links_out.add(correspondence_select_link)
    select_concept.links_in.add(correspondence_select_link)
    label_suggest_link = Relation(
        "", "", label_concept, suggest_concept, Mock(), None, Mock()
    )
    label_concept.links_out.add(label_suggest_link)
    suggest_concept.links_in.add(label_suggest_link)
    label_build_link = Relation(
        "", "", label_concept, build_concept, Mock(), None, Mock()
    )
    label_concept.links_out.add(label_build_link)
    build_concept.links_in.add(label_build_link)
    label_evaluate_link = Relation(
        "", "", label_concept, evaluate_concept, Mock(), None, Mock()
    )
    label_concept.links_out.add(label_evaluate_link)
    evaluate_concept.links_in.add(label_evaluate_link)
    label_select_link = Relation(
        "", "", label_concept, select_concept, Mock(), None, Mock()
    )
    label_concept.links_out.add(label_select_link)
    select_concept.links_in.add(label_select_link)
    relation_suggest_link = Relation(
        "", "", relation_concept, suggest_concept, Mock(), None, Mock()
    )
    relation_concept.links_out.add(relation_suggest_link)
    suggest_concept.links_in.add(relation_suggest_link)
    relation_build_link = Relation(
        "", "", relation_concept, build_concept, Mock(), None, Mock()
    )
    relation_concept.links_out.add(relation_build_link)
    build_concept.links_in.add(relation_build_link)
    relation_evaluate_link = Relation(
        "", "", relation_concept, evaluate_concept, Mock(), None, Mock()
    )
    relation_concept.links_out.add(relation_evaluate_link)
    evaluate_concept.links_in.add(relation_evaluate_link)
    relation_select_link = Relation(
        "", "", relation_concept, select_concept, Mock(), None, Mock()
    )
    relation_concept.links_out.add(relation_select_link)
    select_concept.links_in.add(relation_select_link)
    view_simplex_suggest_link = Relation(
        "", "", view_simplex_concept, suggest_concept, Mock(), None, Mock()
    )
    view_simplex_concept.links_out.add(view_simplex_suggest_link)
    suggest_concept.links_in.add(view_simplex_suggest_link)
    view_simplex_build_link = Relation(
        "", "", view_simplex_concept, build_concept, Mock(), None, Mock()
    )
    view_simplex_concept.links_out.add(view_simplex_build_link)
    build_concept.links_in.add(view_simplex_build_link)
    view_simplex_evaluate_link = Relation(
        "", "", view_simplex_concept, evaluate_concept, Mock(), None, Mock()
    )
    view_simplex_concept.links_out.add(view_simplex_evaluate_link)
    evaluate_concept.links_in.add(view_simplex_evaluate_link)
    view_simplex_select_link = Relation(
        "", "", view_simplex_concept, select_concept, Mock(), None, Mock()
    )
    view_simplex_concept.links_out.add(view_simplex_select_link)
    select_concept.links_in.add(view_simplex_select_link)
    view_monitoring_suggest_link = Relation(
        "", "", view_monitoring_concept, suggest_concept, Mock(), None, Mock()
    )
    view_monitoring_concept.links_out.add(view_monitoring_suggest_link)
    suggest_concept.links_in.add(view_monitoring_suggest_link)
    view_monitoring_build_link = Relation(
        "", "", view_monitoring_concept, build_concept, Mock(), None, Mock()
    )
    view_monitoring_concept.links_out.add(view_monitoring_build_link)
    build_concept.links_in.add(view_monitoring_build_link)
    view_monitoring_evaluate_link = Relation(
        "", "", view_monitoring_concept, evaluate_concept, Mock(), None, Mock()
    )
    view_monitoring_concept.links_out.add(view_monitoring_evaluate_link)
    evaluate_concept.links_in.add(view_monitoring_evaluate_link)
    view_monitoring_select_link = Relation(
        "", "", view_monitoring_concept, select_concept, Mock(), None, Mock()
    )
    view_monitoring_concept.links_out.add(view_monitoring_select_link)
    select_concept.links_in.add(view_monitoring_select_link)
    word_suggest_link = Relation(
        "", "", word_concept, suggest_concept, Mock(), None, Mock()
    )
    word_concept.links_out.add(word_suggest_link)
    suggest_concept.links_in.add(word_suggest_link)
    word_build_link = Relation(
        "", "", word_concept, build_concept, Mock(), None, Mock()
    )
    word_concept.links_out.add(word_build_link)
    build_concept.links_in.add(word_build_link)
    word_evaluate_link = Relation(
        "", "", word_concept, evaluate_concept, Mock(), None, Mock()
    )
    word_concept.links_out.add(word_evaluate_link)
    evaluate_concept.links_in.add(word_evaluate_link)
    word_select_link = Relation(
        "", "", word_concept, select_concept, Mock(), None, Mock()
    )
    word_concept.links_out.add(word_select_link)
    select_concept.links_in.add(word_select_link)
    views_space = ContextualSpace("", "", "views", None, StructureCollection())
    chamber.contextual_spaces.add(views_space)
    return chamber


@pytest.fixture(scope="module")
def input_concept(bubble_chamber):
    concept = Concept(
        "",
        "",
        "input",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def text_concept():
    concept = Concept(
        "",
        "",
        "text",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    return concept


@pytest.fixture(scope="module")
def grammar_vectors():
    vectors = {
        "sentence": [],
        "np": [],
        "vp": [],
        "pronoun": [],
        "adj": [],
        "noun": [],
        "jjr": [],
        "cop": [],
        "prep": [],
        "det": [],
    }
    for index, concept in enumerate(vectors):
        vectors[concept] = [0 for _ in vectors]
        vectors[concept][index] = 1
    return vectors


@pytest.fixture(scope="module")
def grammar_concept():
    concept = Concept(
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
    return concept


@pytest.fixture(scope="module")
def grammar_space(bubble_chamber, grammar_concept):
    space = ConceptualSpace(
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
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture(scope="module")
def sentence_concept(bubble_chamber, grammar_vectors, grammar_space):
    concept = Concept(
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
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def np_concept(bubble_chamber, grammar_vectors, grammar_space):
    concept = Concept(
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
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def vp_concept(bubble_chamber, grammar_vectors, grammar_space):
    concept = Concept(
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
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def pronoun_concept(bubble_chamber, grammar_vectors, grammar_space):
    concept = Concept(
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
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def cop_concept(bubble_chamber, grammar_vectors, grammar_space):
    concept = Concept(
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
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def adj_concept(bubble_chamber, grammar_vectors, grammar_space):
    concept = Concept(
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
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def s_np_vp_rule(
    bubble_chamber, grammar_space, sentence_concept, np_concept, vp_concept
):
    rule = Rule(
        "",
        "",
        "s-->np,vp",
        Location([], grammar_space),
        sentence_concept,
        np_concept,
        vp_concept,
    )
    bubble_chamber.rules.add(rule)
    sentence_to_s_np_vp = Relation(
        "", "", sentence_concept, rule, Mock(), grammar_space, Mock()
    )
    sentence_concept.links_out.add(sentence_to_s_np_vp)
    rule.links_in.add(sentence_to_s_np_vp)
    s_np_vp_to_np = Relation("", "", rule, np_concept, Mock(), grammar_space, Mock())
    rule.links_out.add(s_np_vp_to_np)
    np_concept.links_in.add(s_np_vp_to_np)
    s_np_vp_to_vp = Relation("", "", rule, vp_concept, Mock(), grammar_space, Mock())
    rule.links_out.add(s_np_vp_to_vp)
    vp_concept.links_in.add(s_np_vp_to_vp)
    return rule


@pytest.fixture(scope="module")
def np_pronoun_rule(bubble_chamber, grammar_space, np_concept, pronoun_concept):
    rule = Rule(
        "",
        "",
        "np-->pronoun",
        Location([], grammar_space),
        np_concept,
        pronoun_concept,
        None,
    )
    bubble_chamber.rules.add(rule)
    np_to_np_pronoun = Relation("", "", np_concept, rule, Mock(), grammar_space, Mock())
    np_concept.links_out.add(np_to_np_pronoun)
    rule.links_in.add(np_to_np_pronoun)
    np_pronoun_to_pronoun = Relation(
        "", "", rule, pronoun_concept, Mock(), grammar_space, Mock()
    )
    rule.links_out.add(np_pronoun_to_pronoun)
    pronoun_concept.links_in.add(np_pronoun_to_pronoun)
    return rule


@pytest.fixture(scope="module")
def vp_cop_adj_rule(
    bubble_chamber, grammar_space, vp_concept, cop_concept, adj_concept
):
    rule = Rule(
        "",
        "",
        "vp-->cop,adj",
        Location([], grammar_space),
        vp_concept,
        cop_concept,
        adj_concept,
    )
    bubble_chamber.rules.add(rule)
    vp_to_vp_cop_adj = Relation("", "", vp_concept, rule, Mock(), grammar_space, Mock())
    vp_concept.links_out.add(vp_to_vp_cop_adj)
    rule.links_in.add(vp_to_vp_cop_adj)
    vp_cop_adj_to_cop = Relation(
        "", "", rule, cop_concept, Mock(), grammar_space, Mock()
    )
    rule.links_out.add(vp_cop_adj_to_cop)
    cop_concept.links_in.add(vp_cop_adj_to_cop)
    vp_cop_adj_to_adj = Relation(
        "", "", rule, adj_concept, Mock(), grammar_space, Mock()
    )
    rule.links_out.add(vp_cop_adj_to_adj)
    adj_concept.links_in.add(vp_cop_adj_to_adj)
    return rule


@pytest.fixture(scope="module")
def vp_cop_rule(bubble_chamber, grammar_space, vp_concept, cop_concept):
    rule = Rule(
        "",
        "",
        "vp-->cop",
        Location([], grammar_space),
        vp_concept,
        cop_concept,
        None,
    )
    bubble_chamber.rules.add(rule)
    vp_to_vp_cop = Relation("", "", vp_concept, rule, Mock(), grammar_space, Mock())
    vp_concept.links_out.add(vp_to_vp_cop)
    rule.links_in.add(vp_to_vp_cop)
    vp_cop_to_cop = Relation("", "", rule, cop_concept, Mock(), grammar_space, Mock())
    rule.links_out.add(vp_cop_to_cop)
    cop_concept.links_in.add(vp_cop_rule)
    return rule


@pytest.fixture(scope="module")
def it_lexeme():
    return Lexeme("", "", "it", {WordForm.HEADWORD: "it"})


@pytest.fixture(scope="module")
def is_lexeme():
    return Lexeme("", "", "is", {WordForm.HEADWORD: "is"})


@pytest.fixture(scope="module")
def in_lexeme():
    return Lexeme("", "", "in", {WordForm.HEADWORD: "in"})


@pytest.fixture(scope="module")
def the_lexeme():
    return Lexeme("", "", "the", {WordForm.HEADWORD: "the"})


@pytest.fixture(scope="module")
def than_lexeme():
    return Lexeme("", "", "than", {WordForm.HEADWORD: "than"})


@pytest.fixture(scope="module")
def north_lexeme(north_concept):
    lexeme = Lexeme("", "", "north", {WordForm.HEADWORD: "north"})
    link = Relation("", "", north_concept, lexeme, None, [], 1.0)
    north_concept.links_out.add(link)
    lexeme.links_in.add(link)
    return lexeme


@pytest.fixture(scope="module")
def south_lexeme(south_concept):
    lexeme = Lexeme("", "", "south", {WordForm.HEADWORD: "south"})
    link = Relation("", "", south_concept, lexeme, None, [], 1.0)
    south_concept.links_out.add(link)
    lexeme.links_in.add(link)
    return lexeme


@pytest.fixture(scope="module")
def warm_lexeme(warm_concept):
    lexeme = Lexeme("", "", "warm", {WordForm.HEADWORD: "warm"})
    link = Relation("", "", warm_concept, lexeme, None, [], 1.0)
    warm_concept.links_out.add(link)
    lexeme.links_in.add(link)
    return lexeme


@pytest.fixture(scope="module")
def hotter_lexeme(hotter_concept):
    lexeme = Lexeme("", "", "hotter", {WordForm.HEADWORD: "hotter"})
    link = Relation("", "", hotter_concept, lexeme, None, [], 1.0)
    hotter_concept.links_out.add(link)
    lexeme.links_in.add(link)
    return lexeme


@pytest.fixture(scope="module")
def it_word(grammar_vectors, grammar_space, it_lexeme):
    return Word(
        "",
        "",
        "it",
        it_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["pronoun"]], grammar_space)],
        grammar_space,
        1,
    )


@pytest.fixture(scope="module")
def is_word(grammar_vectors, grammar_space, is_lexeme):
    return Word(
        "",
        "",
        "is",
        is_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["cop"]], grammar_space)],
        grammar_space,
        1,
    )


@pytest.fixture(scope="module")
def in_word(grammar_vectors, grammar_space, in_lexeme):
    return Word(
        "",
        "",
        "in",
        in_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["prep"]], grammar_space)],
        grammar_space,
        1,
    )


@pytest.fixture(scope="module")
def the_word(grammar_vectors, grammar_space, the_lexeme):
    return Word(
        "",
        "",
        "the",
        the_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["det"]], grammar_space)],
        grammar_space,
        1,
    )


@pytest.fixture(scope="module")
def than_word(grammar_vectors, grammar_space, than_lexeme):
    return Word(
        "",
        "",
        "than",
        than_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["prep"]], grammar_space)],
        grammar_space,
        1,
    )


@pytest.fixture(scope="module")
def north_word(grammar_vectors, grammar_space, north_lexeme):
    return Word(
        "",
        "",
        "north",
        north_lexeme,
        WordForm.HEADWORD,
        [
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammar_space,
            )
        ],
        grammar_space,
        1,
    )


@pytest.fixture(scope="module")
def south_word(grammar_vectors, grammar_space, south_lexeme):
    return Word(
        "",
        "",
        "south",
        south_lexeme,
        WordForm.HEADWORD,
        [
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammar_space,
            )
        ],
        grammar_space,
        1,
    )


@pytest.fixture(scope="module")
def warm_word(grammar_vectors, grammar_space, warm_lexeme):
    return Word(
        "",
        "",
        "warm",
        warm_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["adj"]], grammar_space)],
        grammar_space,
        1,
    )


@pytest.fixture(scope="module")
def hotter_word(bubble_chamber, grammar_vectors, grammar_space, hotter_lexeme):
    word = Word(
        "",
        "",
        "hotter",
        hotter_lexeme,
        WordForm.HEADWORD,
        [Location([grammar_vectors["jjr"]], grammar_space)],
        grammar_space,
        1,
    )
    bubble_chamber.words.add(word)
    return word


@pytest.fixture(scope="module")
def location_concept(bubble_chamber):
    concept = Concept(
        "",
        "",
        "location",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def north_south_space(bubble_chamber, location_concept):
    space = ConceptualSpace(
        "",
        "",
        "north-south",
        location_concept,
        StructureCollection(),
        1,
        [],
        [],
        super_space_to_coordinate_function_map={
            "location": lambda location: [[c[0]] for c in location.coordinates]
        },
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture(scope="module")
def west_east_space(bubble_chamber, location_concept):
    space = ConceptualSpace(
        "",
        "",
        "west-east",
        location_concept,
        StructureCollection(),
        1,
        [],
        [],
        super_space_to_coordinate_function_map={
            "location": lambda location: [[c[1]] for c in location.coordinates]
        },
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture(scope="module")
def nw_se_space(bubble_chamber, location_concept):
    space = ConceptualSpace(
        "",
        "",
        "nw-se",
        location_concept,
        StructureCollection(),
        1,
        [],
        [],
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                [statistics.fmean(c)] for c in location.coordinates
            ]
        },
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture(scope="module")
def ne_sw_space(bubble_chamber, location_concept):
    space = ConceptualSpace(
        "",
        "",
        "ne-sw",
        location_concept,
        StructureCollection(),
        1,
        [],
        [],
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                [statistics.fmean([c[0], 4 - c[1]])] for c in location.coordinates
            ]
        },
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture(scope="module")
def location_space(
    bubble_chamber,
    location_concept,
    north_south_space,
    west_east_space,
    nw_se_space,
    ne_sw_space,
):
    space = ConceptualSpace(
        "",
        "",
        "location",
        location_concept,
        StructureCollection(),
        2,
        [north_south_space, west_east_space],
        [north_south_space, west_east_space, nw_se_space, ne_sw_space],
        is_basic_level=True,
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture(scope="module")
def south_concept(bubble_chamber, location_space):
    concept = Concept(
        "",
        "",
        "south",
        [Location([[5, 2]], location_space)],
        Mock(),
        Mock(),
        Mock(),
        location_space,
        Mock(),
        centroid_euclidean_distance,
    )
    location_space.add(concept)
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def north_concept(bubble_chamber, location_space):
    concept = Concept(
        "",
        "",
        "north",
        [Location([[0, 2]], location_space)],
        Mock(),
        Mock(),
        Mock(),
        location_space,
        Mock(),
        centroid_euclidean_distance,
    )
    location_space.add(concept)
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def temperature_concept(bubble_chamber):
    concept = Concept(
        "",
        "",
        "temperature",
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        centroid_euclidean_distance,
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def temperature_space(bubble_chamber, temperature_concept):
    space = ConceptualSpace(
        "",
        "",
        "temperature",
        temperature_concept,
        StructureCollection(),
        1,
        [],
        [],
        is_basic_level=True,
    )
    bubble_chamber.conceptual_spaces.add(space)
    return space


@pytest.fixture(scope="module")
def same_concept(bubble_chamber):
    concept = Concept(
        "",
        "",
        "same",
        [],
        SamenessClassifier(),
        Mock(),
        Correspondence,
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def same_rule(bubble_chamber, same_concept):
    rule = Rule("", "", "same", Mock(), same_concept, same_concept, None)
    bubble_chamber.rules.add(rule)
    return rule


@pytest.fixture(scope="module")
def hot_concept(bubble_chamber, temperature_space):
    concept = Concept(
        "",
        "",
        "hot",
        [Location([[22]], temperature_space)],
        Mock(),
        Mock(),
        Mock(),
        temperature_space,
        Mock(),
        centroid_euclidean_distance,
    )
    temperature_space.add(concept)
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def warm_concept(bubble_chamber, temperature_space):
    concept = Concept(
        "",
        "",
        "warm",
        [Location([[16]], temperature_space)],
        Mock(),
        Mock(),
        Mock(),
        temperature_space,
        Mock(),
        centroid_euclidean_distance,
    )
    temperature_space.add(concept)
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def cold_concept(bubble_chamber, temperature_space):
    concept = Concept(
        "",
        "",
        "cold",
        [Location([[4]], temperature_space)],
        Mock(),
        Mock(),
        Mock(),
        temperature_space,
        Mock(),
        centroid_euclidean_distance,
    )
    temperature_space.add(concept)
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def hotter_concept(bubble_chamber, temperature_space):
    concept = Concept(
        "",
        "",
        "hotter",
        [TwoPointLocation([[math.nan]], [[math.nan]], temperature_space)],
        Mock(),
        Mock(),
        Mock(),
        temperature_space,
        Mock(),
        centroid_euclidean_distance,
    )
    temperature_space.add(concept)
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def comparison_frame(
    bubble_chamber,
    input_concept,
    location_space,
    temperature_space,
    grammar_space,
    it_word,
    is_word,
    in_word,
    the_word,
    than_word,
    hotter_word,
    south_word,
):
    frame_input_space = ContextualSpace(
        "",
        "",
        "",
        input_concept,
        StructureCollection(),
        [location_space, temperature_space],
    )
    chunk_one = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], frame_input_space),
            Location([[None, None]], location_space),
            Location([[None]], temperature_space),
        ],
        StructureCollection(),
        frame_input_space,
        1.0,
    )
    frame_input_space.add(chunk_one)
    chunk_two = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], frame_input_space),
            Location([[None, None]], location_space),
            Location([[None]], temperature_space),
        ],
        StructureCollection(),
        frame_input_space,
        1.0,
    )
    frame_input_space.add(chunk_two)
    label_one = Label(
        ID.new(Label),
        "",
        chunk_one,
        None,
        [Location([[]], frame_input_space), Location([[None, None]], location_space)],
        1.0,
    )
    chunk_one.links_out.add(label_one)
    label_two = Label(
        ID.new(Label),
        "",
        chunk_two,
        None,
        [Location([[]], frame_input_space), Location([[None, None]], location_space)],
        1.0,
    )
    chunk_two.links_out.add(label_two)
    one_to_two_relation = Relation(
        ID.new(Relation),
        "",
        chunk_one,
        chunk_two,
        None,
        [
            TwoPointLocation([[]], [[]], frame_input_space),
            TwoPointLocation([[None]], [[None]], temperature_space),
        ],
        1.0,
    )
    chunk_one.links_out.add(one_to_two_relation)
    chunk_two.links_in.add(one_to_two_relation)
    frame_output_space = ContextualSpace(
        "", "", "", text_concept, StructureCollection(), [grammar_space]
    )
    word_0 = it_word.copy_to_location(Location([[0]], frame_output_space), quality=1.0)
    word_1 = is_word.copy_to_location(Location([[1]], frame_output_space), quality=1.0)
    word_2 = Word(
        ID.new(Word),
        "",
        None,
        None,
        WordForm.HEADWORD,
        [
            Location([[2]], frame_output_space),
            hotter_word.location_in_space(grammar_space),
        ],
        frame_output_space,
        1.0,
    )
    frame_output_space.add(word_2)
    word_3 = in_word.copy_to_location(Location([[3]], frame_output_space), quality=1.0)
    word_4 = the_word.copy_to_location(Location([[4]], frame_output_space), quality=1.0)
    word_5 = Word(
        ID.new(Word),
        "",
        None,
        None,
        WordForm.HEADWORD,
        [
            Location([[5]], frame_output_space),
            south_word.location_in_space(grammar_space),
        ],
        frame_output_space,
        1.0,
    )
    frame_output_space.add(word_5)
    word_6 = than_word.copy_to_location(
        Location([[6]], frame_output_space), quality=1.0
    )
    word_7 = the_word.copy_to_location(Location([[7]], frame_output_space), quality=1.0)
    word_8 = Word(
        ID.new(Word),
        "",
        None,
        None,
        WordForm.HEADWORD,
        [
            Location([[8]], frame_output_space),
            south_word.location_in_space(grammar_space),
        ],
        frame_output_space,
        1.0,
    )
    frame_output_space.add(word_8)
    word_2_correspondence = Correspondence(
        "",
        "",
        one_to_two_relation,
        word_2,
        [
            one_to_two_relation.location_in_space(one_to_two_relation.parent_space),
            word_2.location_in_space(word_2.parent_space),
        ],
        same_concept,
        temperature_space,
        None,
        1.0,
    )
    word_5_correspondence = Correspondence(
        "",
        "",
        label_one,
        word_5,
        [
            label_one.location_in_space(label_one.parent_space),
            word_5.location_in_space(word_5.parent_space),
        ],
        same_concept,
        location_space,
        None,
        1.0,
    )
    word_8_correspondence = Correspondence(
        "",
        "",
        label_two,
        word_8,
        [
            label_two.location_in_space(label_two.parent_space),
            word_8.location_in_space(word_8.parent_space),
        ],
        same_concept,
        location_space,
        None,
        1.0,
    )
    frame_contents = StructureCollection(
        {word_2_correspondence, word_5_correspondence, word_8_correspondence}
    )
    frame = Frame(
        "", "", "", Mock(), frame_contents, frame_input_space, frame_output_space
    )
    bubble_chamber.frames.add(frame)
