import pytest
import statistics
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import ProximityClassifier, SamenessClassifier
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Concept, Lexeme, Rule, Word
from homer.structures.spaces import ConceptualSpace
from homer.tools import centroid_euclidean_distance
from homer.word_form import WordForm


@pytest.fixture(scope="module")
def bubble_chamber():
    logger = Mock()
    chamber = BubbleChamber.setup(logger)
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
    chamber.concepts.add(chunk_concept)
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
    return chamber


@pytest.fixture(scope="module")
def grammar_vectors():
    vectors = {
        "sentence": [],
        "np": [],
        "vp": [],
        "pronoun": [],
        "adj": [],
        "cop": [],
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
    bubble_chamber.contextual_spaces.add(space)
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
def warm_lexeme():
    return Lexeme("", "", "warm", {WordForm.HEADWORD: "warm"})


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
def sameness_concept(bubble_chamber):
    concept = Concept(
        "",
        "",
        "sameness",
        [],
        SamenessClassifier(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    bubble_chamber.concepts.add(concept)
    return concept


@pytest.fixture(scope="module")
def sameness_rule(bubble_chamber, sameness_concept):
    rule = Rule("", "", "sameness", Mock(), sameness_concept, sameness_concept, None)
    bubble_chamber.rules.add(rule)
    return rule
