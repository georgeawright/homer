import math
import random
import statistics

from homer import fuzzy
from homer import Homer, StructureCollection
from homer.classifiers import (
    DifferenceClassifier,
    DifferentnessClassifier,
    SamenessClassifier,
    ProximityClassifier,
    RuleClassifier,
)
from homer.id import ID
from homer.location import Location
from homer.locations import TwoPointLocation

random.seed(123)
from homer.loggers import DjangoLogger
from homer.structures.links import Label, Relation
from homer.structures.nodes import Chunk, Word
from homer.tools import add_vectors, centroid_euclidean_distance
from homer.word_form import WordForm


def setup_homer() -> Homer:
    problem = [
        [4, 5, 6, 4, 3],
        [10, 10, 7, 4, 4],
        [10, 11, 13, 16, 17],
        [10, 13, 16, 16, 19],
        [13, 20, 22, 19, 21],
        [22, 22, 24, 23, 22],
    ]

    path_to_logs = "logs"
    logger = DjangoLogger.setup(path_to_logs)
    homer = Homer.setup(logger)

    top_level_conceptual_space = homer.bubble_chamber.spaces["top level"]
    top_level_working_space = top_level_conceptual_space.instance_in_space(
        None, name="top level working"
    )

    input_concept = homer.def_concept(
        name="input",
        parent_space=top_level_conceptual_space,
        distance_function=centroid_euclidean_distance,
    )
    input_space = homer.def_working_space(
        name="input",
        parent_concept=input_concept,
        locations=[Location([], top_level_working_space)],
    )
    interpretation_concept = homer.def_concept(
        name="interpretation",
        parent_space=top_level_conceptual_space,
    )
    activity_concept = homer.def_concept(
        name="activity",
        parent_space=top_level_conceptual_space,
    )
    activities_space = homer.def_conceptual_space(
        name="activities",
        parent_concept=activity_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    suggest_concept = homer.def_concept(
        name="suggest",
        parent_space=activities_space,
        activation=1.0,
    )
    build_concept = homer.def_concept(
        name="build",
        parent_space=activities_space,
        activation=1.0,
    )
    evaluate_concept = homer.def_concept(
        name="evaluate",
        parent_space=activities_space,
    )
    select_concept = homer.def_concept(
        name="select",
        parent_space=activities_space,
    )
    publish_concept = homer.def_concept(
        name="publish",
        parent_space=activities_space,
    )
    space_type_concept = homer.def_concept(
        name="space type",
        parent_space=top_level_conceptual_space,
    )
    space_types_space = homer.def_conceptual_space(
        name="space types",
        parent_concept=space_type_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    inner_concept = homer.def_concept(
        name="inner",
        parent_space=space_types_space,
    )
    outer_concept = homer.def_concept(
        name="outer",
        parent_space=space_types_space,
    )
    direction_concept = homer.def_concept(
        name="direction",
        parent_space=top_level_conceptual_space,
    )
    directions_space = homer.def_conceptual_space(
        name="directions",
        parent_concept=direction_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    forward_concept = homer.def_concept(
        name="forward",
        parent_space=directions_space,
    )
    reverse_concept = homer.def_concept(
        name="reverse",
        parent_space=directions_space,
    )
    structure_concept = homer.def_concept(
        name="structure",
        parent_space=top_level_conceptual_space,
    )
    structures_space = homer.def_conceptual_space(
        name="structures",
        parent_concept=structure_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    chunk_concept = homer.def_concept(
        name="chunk",
        parent_space=structures_space,
    )
    view_concept = homer.def_concept(
        name="view",
        parent_space=structures_space,
    )
    view_discourse_concept = homer.def_concept(
        name="view-discourse",
        parent_space=structures_space,
    )
    view_monitoring_concept = homer.def_concept(
        name="view-monitoring",
        parent_space=structures_space,
    )
    view_simplex_concept = homer.def_concept(
        name="view-simplex",
        parent_space=structures_space,
    )
    word_concept = homer.def_concept(
        name="word",
        parent_space=structures_space,
        instance_type=str,
    )
    phrase_concept = homer.def_concept(
        name="phrase",
        parent_space=structures_space,
    )
    label_concept = homer.def_concept(
        name="label",
        parent_space=structures_space,
    )
    relation_concept = homer.def_concept(
        name="relation",
        parent_space=structures_space,
    )
    correspondence_concept = homer.def_concept(
        name="correspondence",
        parent_space=structures_space,
    )
    template_concept = homer.def_concept(
        name="template",
        parent_space=structures_space,
    )
    text_concept = homer.def_concept(
        name="text",
        parent_space=structures_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    discourse_concept = homer.def_concept(
        name="discourse",
        parent_space=structures_space,
        instance_type=Word,
    )
    label_concepts_space = homer.def_conceptual_space(
        name="label concepts",
        parent_concept=label_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    relational_concepts_space = homer.def_conceptual_space(
        name="relational concepts",
        parent_concept=relation_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    correspondential_concepts_space = homer.def_conceptual_space(
        name="correspondential concepts",
        parent_concept=correspondence_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    templates_space = homer.def_conceptual_space(
        name="templates",
        parent_concept=template_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    text_space = homer.def_conceptual_space(
        name="text",
        parent_concept=text_concept,
        locations=[Location([], top_level_conceptual_space)],
    )
    # structure links
    homer.def_concept_link(inner_concept, chunk_concept, activation=1.0)
    homer.def_concept_link(chunk_concept, inner_concept, activation=1.0)
    homer.def_concept_link(chunk_concept, label_concept, activation=1.0)
    homer.def_concept_link(chunk_concept, relation_concept, activation=1.0)
    homer.def_concept_link(chunk_concept, view_concept, activation=1.0)
    homer.def_concept_link(label_concept, inner_concept, activation=1.0)
    homer.def_concept_link(relation_concept, inner_concept, activation=1.0)
    homer.def_concept_link(view_concept, view_discourse_concept, activation=1.0)
    homer.def_concept_link(view_concept, view_monitoring_concept, activation=1.0)
    homer.def_concept_link(view_concept, view_simplex_concept, activation=1.0)
    homer.def_concept_link(view_monitoring_concept, reverse_concept, activation=1.0)
    homer.def_concept_link(view_monitoring_concept, outer_concept, activation=1.0)
    homer.def_concept_link(reverse_concept, chunk_concept, activation=1.0)
    homer.def_concept_link(
        view_discourse_concept, correspondence_concept, activation=1.0
    )
    homer.def_concept_link(view_discourse_concept, word_concept, activation=1.0)
    homer.def_concept_link(view_simplex_concept, correspondence_concept, activation=1.0)
    homer.def_concept_link(view_simplex_concept, word_concept, activation=1.0)
    homer.def_concept_link(word_concept, phrase_concept, activation=1.0)
    homer.def_concept_link(word_concept, view_monitoring_concept, activation=1.0)
    homer.def_concept_link(word_concept, label_concept, activation=1.0)
    homer.def_concept_link(word_concept, relation_concept, activation=1.0)
    homer.def_concept_link(view_monitoring_concept, publish_concept, activation=1.0)

    # activity links
    homer.def_concept_link(suggest_concept, build_concept, activation=1.0)
    homer.def_concept_link(build_concept, evaluate_concept, activation=1.0)
    homer.def_concept_link(evaluate_concept, select_concept, activation=1.0)
    homer.def_concept_link(select_concept, suggest_concept, activation=1.0)

    # activity-structure links
    homer.def_concept_link(suggest_concept, correspondence_concept)
    homer.def_concept_link(suggest_concept, chunk_concept)
    homer.def_concept_link(suggest_concept, label_concept, activation=1.0)
    homer.def_concept_link(suggest_concept, phrase_concept)
    homer.def_concept_link(suggest_concept, relation_concept)
    homer.def_concept_link(suggest_concept, view_discourse_concept)
    homer.def_concept_link(suggest_concept, view_monitoring_concept)
    homer.def_concept_link(suggest_concept, view_simplex_concept)
    homer.def_concept_link(suggest_concept, word_concept)
    homer.def_concept_link(build_concept, correspondence_concept)
    homer.def_concept_link(build_concept, chunk_concept)
    homer.def_concept_link(build_concept, label_concept, activation=1.0)
    homer.def_concept_link(build_concept, phrase_concept)
    homer.def_concept_link(build_concept, relation_concept)
    homer.def_concept_link(build_concept, view_discourse_concept)
    homer.def_concept_link(build_concept, view_monitoring_concept)
    homer.def_concept_link(build_concept, view_simplex_concept)
    homer.def_concept_link(build_concept, word_concept)
    homer.def_concept_link(evaluate_concept, correspondence_concept)
    homer.def_concept_link(evaluate_concept, chunk_concept)
    homer.def_concept_link(evaluate_concept, label_concept)
    homer.def_concept_link(evaluate_concept, phrase_concept)
    homer.def_concept_link(evaluate_concept, relation_concept)
    homer.def_concept_link(evaluate_concept, view_discourse_concept)
    homer.def_concept_link(evaluate_concept, view_monitoring_concept)
    homer.def_concept_link(evaluate_concept, view_simplex_concept)
    homer.def_concept_link(evaluate_concept, word_concept)
    homer.def_concept_link(select_concept, correspondence_concept)
    homer.def_concept_link(select_concept, chunk_concept)
    homer.def_concept_link(select_concept, label_concept)
    homer.def_concept_link(select_concept, phrase_concept)
    homer.def_concept_link(select_concept, relation_concept)
    homer.def_concept_link(select_concept, view_discourse_concept)
    homer.def_concept_link(select_concept, view_monitoring_concept)
    homer.def_concept_link(select_concept, view_simplex_concept)
    homer.def_concept_link(select_concept, word_concept)

    # Grammatical Knowledge

    grammar_vectors = {
        "sentence": [],
        "np": [],
        "vp": [],
        "ap": [],
        "pp": [],
        "noun": [],
        "verb": [],
        "adj": [],
        "jjr": [],
        "adv": [],
        "cop": [],
        "prep": [],
        "det": [],
        "conj": [],
        "null": [],
    }
    for index, concept in enumerate(grammar_vectors):
        grammar_vectors[concept] = [0 for _ in grammar_vectors]
        grammar_vectors[concept][index] = 1

    dependency_vectors = {
        "det_r": [],
        "nsubj": [],
        "cop_r": [],
        "prep_r": [],
        "pobj": [],
        "dep": [],
    }
    for index, concept in enumerate(dependency_vectors):
        dependency_vectors[concept] = [0 for _ in dependency_vectors]
        dependency_vectors[concept][index] = 1

    grammar_concept = homer.def_concept(
        name="grammar",
        parent_space=label_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=0.1,
    )
    grammatical_concepts_space = homer.def_conceptual_space(
        name="grammar",
        parent_concept=grammar_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        is_basic_level=True,
        is_symbolic=True,
    )
    sentence_concept = homer.def_concept(
        name="s",
        locations=[Location([grammar_vectors["sentence"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    np_concept = homer.def_concept(
        name="np",
        locations=[Location([grammar_vectors["np"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    vp_concept = homer.def_concept(
        name="vp",
        locations=[Location([grammar_vectors["vp"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    ap_concept = homer.def_concept(
        name="ap",
        locations=[Location([grammar_vectors["ap"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    pp_concept = homer.def_concept(
        name="pp",
        locations=[Location([grammar_vectors["pp"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    noun_concept = homer.def_concept(
        name="noun",
        locations=[Location([grammar_vectors["noun"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    verb_concept = homer.def_concept(
        name="verb",
        locations=[
            Location([grammar_vectors["verb"]], grammatical_concepts_space),
            Location([], label_concepts_space),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    adj_concept = homer.def_concept(
        name="adj",
        locations=[Location([grammar_vectors["adj"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    jjr_concept = homer.def_concept(
        name="jjr",
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    adv_concept = homer.def_concept(
        name="adv",
        locations=[Location([grammar_vectors["adv"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    cop_concept = homer.def_concept(
        name="cop",
        locations=[Location([grammar_vectors["cop"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    prep_concept = homer.def_concept(
        name="prep",
        locations=[Location([grammar_vectors["prep"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    det_concept = homer.def_concept(
        name="det",
        locations=[Location([grammar_vectors["det"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    conj_concept = homer.def_concept(
        name="conj",
        locations=[Location([grammar_vectors["conj"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        classifier=ProximityClassifier(),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    null_concept = homer.def_concept(
        name="null",
        locations=[Location([grammar_vectors["null"]], grammatical_concepts_space)],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Label,
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    s_np_vp = homer.def_rule(
        name="s --> np, vp",
        location=Location([], grammatical_concepts_space),
        root=sentence_concept,
        left_branch=np_concept,
        right_branch=vp_concept,
        stable_activation=1.0,
    )
    s_noun_vp = homer.def_rule(
        name="s --> noun, vp",
        location=Location([], grammatical_concepts_space),
        root=sentence_concept,
        left_branch=noun_concept,
        right_branch=vp_concept,
        stable_activation=1.0,
    )
    s_s_pp = homer.def_rule(
        name="s --> s, pp",
        location=Location([], grammatical_concepts_space),
        root=sentence_concept,
        left_branch=sentence_concept,
        right_branch=pp_concept,
        stable_activation=1.0,
    )
    # TODO: add S --> S conj S
    np_det_noun = homer.def_rule(
        name="np --> det, noun",
        location=Location([], grammatical_concepts_space),
        root=np_concept,
        left_branch=det_concept,
        right_branch=noun_concept,
        stable_activation=1.0,
    )
    vp_cop_adj = homer.def_rule(
        name="vp --> cop, adj",
        location=Location([], grammatical_concepts_space),
        root=vp_concept,
        left_branch=cop_concept,
        right_branch=adj_concept,
        stable_activation=1.0,
    )
    vp_cop_ap = homer.def_rule(
        name="vp --> cop, ap",
        location=Location([], grammatical_concepts_space),
        root=vp_concept,
        left_branch=cop_concept,
        right_branch=ap_concept,
        stable_activation=1.0,
    )
    vp_verb = homer.def_rule(
        name="vp --> verb",
        location=Location([], grammatical_concepts_space),
        root=vp_concept,
        left_branch=verb_concept,
        right_branch=null_concept,
        stable_activation=1.0,
    )
    ap_adj = homer.def_rule(
        name="ap --> adj",
        location=Location([], grammatical_concepts_space),
        root=ap_concept,
        left_branch=adj_concept,
        right_branch=null_concept,
        stable_activation=1.0,
    )
    pp_prep_np = homer.def_rule(
        name="pp --> prep, np",
        location=Location([], grammatical_concepts_space),
        root=pp_concept,
        left_branch=prep_concept,
        right_branch=np_concept,
        stable_activation=1.0,
    )
    dependency_concept = homer.def_concept(
        name="dependency",
        parent_space=relational_concepts_space,
        instance_type=Word,
        distance_function=centroid_euclidean_distance,
    )
    dependency_concepts_space = homer.def_conceptual_space(
        name="dependency",
        parent_concept=dependency_concept,
        locations=[Location([], relational_concepts_space)],
        no_of_dimensions=1,
        is_basic_level=False,
        is_symbolic=True,
    )
    det_r_concept = homer.def_concept(
        name="det_r",
        locations=[
            TwoPointLocation(
                [grammar_vectors["noun"]],
                [grammar_vectors["det"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["det_r"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Relation,
        classifier=RuleClassifier(
            lambda kwargs: fuzzy.AND(
                kwargs["start"].location.coordinates[0][0]
                == kwargs["end"].location.coordinates[0][0] + 1,
                kwargs["start"].has_label(noun_concept),
                kwargs["end"].has_label(det_concept),
            )
        ),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    nsubj_concept = homer.def_concept(
        name="nsubj",
        locations=[
            TwoPointLocation(
                [grammar_vectors["verb"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["adj"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["jjr"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["nsubj"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Relation,
        classifier=RuleClassifier(
            lambda kwargs: fuzzy.AND(
                kwargs["end"].has_label(noun_concept),
                fuzzy.OR(
                    kwargs["start"].has_label(verb_concept),
                    fuzzy.AND(
                        fuzzy.OR(
                            kwargs["start"].has_label(adj_concept),
                            kwargs["start"].has_label(jjr_concept),
                        ),
                        kwargs["start"].has_relation_with_name("cop_r"),
                    ),
                ),
                kwargs["end"].location.coordinates[0][0]
                < kwargs["start"].location.coordinates[0][0],
            )
        ),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    cop_r_concept = homer.def_concept(
        name="cop_r",
        locations=[
            TwoPointLocation(
                [grammar_vectors["adj"]],
                [grammar_vectors["cop"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["jjr"]],
                [grammar_vectors["cop"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["cop_r"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Relation,
        classifier=RuleClassifier(
            lambda kwargs: fuzzy.AND(
                kwargs["end"].has_label(cop_concept),
                fuzzy.OR(
                    kwargs["start"].has_label(adj_concept),
                    kwargs["start"].has_label(jjr_concept),
                ),
                kwargs["start"].location.coordinates[0][0]
                == kwargs["end"].location.coordinates[0][0] + 1,
            )
        ),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    prep_r_concept = homer.def_concept(
        name="prep_r",
        locations=[
            TwoPointLocation(
                [grammar_vectors["verb"]],
                [grammar_vectors["prep"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["adj"]],
                [grammar_vectors["prep"]],
                grammatical_concepts_space,
            ),
            TwoPointLocation(
                [grammar_vectors["jjr"]],
                [grammar_vectors["prep"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["prep_r"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Relation,
        classifier=RuleClassifier(
            lambda kwargs: fuzzy.AND(
                kwargs["end"].has_label(prep_concept),
                fuzzy.OR(
                    kwargs["start"].has_label(verb_concept),
                    fuzzy.AND(
                        fuzzy.OR(
                            kwargs["start"].has_label(adj_concept),
                            kwargs["start"].has_label(jjr_concept),
                        ),
                        kwargs["start"].has_relation_with_name("cop_r"),
                    ),
                ),
                kwargs["start"].location.coordinates[0][0]
                < kwargs["end"].location.coordinates[0][0],
            )
        ),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    pobj_concept = homer.def_concept(
        name="pobj",
        locations=[
            TwoPointLocation(
                [grammar_vectors["prep"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["pobj"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Relation,
        classifier=RuleClassifier(
            lambda kwargs: fuzzy.AND(
                kwargs["end"].has_label(noun_concept),
                kwargs["start"].has_label(prep_concept),
                kwargs["start"].location.coordinates[0][0]
                < kwargs["end"].location.coordinates[0][0],
            )
        ),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )
    dep_concept = homer.def_concept(
        name="dep",
        locations=[
            TwoPointLocation(
                [grammar_vectors["prep"]],
                [grammar_vectors["noun"]],
                grammatical_concepts_space,
            ),
            Location(
                [dependency_vectors["dep"]],
                dependency_concepts_space,
            ),
        ],
        parent_space=grammatical_concepts_space,
        instance_type=Word,
        structure_type=Relation,
        classifier=RuleClassifier(
            lambda kwargs: fuzzy.AND(
                kwargs["end"].has_label(noun_concept),
                kwargs["start"].has_label(prep_concept),
                kwargs["start"].has_relation_with_name("prep_r"),
                lambda x: kwargs["start"]
                .relation_with_name("prep_r")
                .start.has_relation_with_name("pobj")(),
                kwargs["end"].location.coordinates[0][0]
                > kwargs["start"].location.coordinates[0][0],
            )
        ),
        distance_function=centroid_euclidean_distance,
        distance_to_proximity_weight=grammar_concept.distance_to_proximity_weight,
    )

    homer.def_concept_link(det_concept, det_r_concept, activation=1.0)
    homer.def_concept_link(noun_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(noun_concept, pobj_concept, activation=1.0)
    homer.def_concept_link(noun_concept, dep_concept, activation=1.0)
    homer.def_concept_link(prep_concept, prep_r_concept, activation=1.0)
    homer.def_concept_link(prep_concept, pobj_concept, activation=1.0)
    homer.def_concept_link(prep_concept, dep_concept, activation=1.0)
    homer.def_concept_link(cop_concept, cop_r_concept, activation=1.0)
    homer.def_concept_link(cop_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(cop_concept, prep_r_concept, activation=1.0)
    homer.def_concept_link(verb_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(verb_concept, prep_r_concept, activation=1.0)
    homer.def_concept_link(adj_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(adj_concept, cop_r_concept, activation=1.0)
    homer.def_concept_link(adj_concept, prep_r_concept, activation=1.0)
    homer.def_concept_link(jjr_concept, nsubj_concept, activation=1.0)
    homer.def_concept_link(jjr_concept, cop_r_concept, activation=1.0)
    homer.def_concept_link(jjr_concept, prep_r_concept, activation=1.0)

    the_lexeme = homer.def_lexeme(
        headword="the",
        parent_concept=None,
    )
    the_word = homer.def_word(
        name="the",
        lexeme=the_lexeme,
        word_form=WordForm.HEADWORD,
        locations=[Location([grammar_vectors["det"]], grammatical_concepts_space)],
    )
    is_lexeme = homer.def_lexeme(
        headword="is",
        parent_concept=None,
    )
    is_word = homer.def_word(
        name="is",
        lexeme=is_lexeme,
        word_form=WordForm.HEADWORD,
        locations=[Location([grammar_vectors["cop"]], grammatical_concepts_space)],
    )
    it_lexeme = homer.def_lexeme(
        headword="it",
        parent_concept=None,
    )
    it_word = homer.def_word(
        name="it",
        lexeme=it_lexeme,
        word_form=WordForm.HEADWORD,
        locations=[Location([grammar_vectors["noun"]], grammatical_concepts_space)],
    )
    in_lexeme = homer.def_lexeme(
        headword="in",
        parent_concept=None,
    )
    in_word = homer.def_word(
        name="in",
        lexeme=it_lexeme,
        word_form=WordForm.HEADWORD,
        locations=[Location([grammar_vectors["prep"]], grammatical_concepts_space)],
    )
    than_lexeme = homer.def_lexeme(
        headword="than",
        parent_concept=None,
    )
    than_word = homer.def_word(
        name="than",
        lexeme=than_lexeme,
        word_form=WordForm.HEADWORD,
        locations=[Location([grammar_vectors["prep"]], grammatical_concepts_space)],
    )
    and_lexeme = homer.def_lexeme(
        headword="and",
        parent_concept=None,
    )
    and_word = homer.def_word(
        name="and",
        lexeme=than_lexeme,
        word_form=WordForm.HEADWORD,
        locations=[Location([grammar_vectors["conj"]], grammatical_concepts_space)],
    )
    comma_lexeme = homer.def_lexeme(
        headword=",",
        parent_concept=None,
    )
    comma_word = homer.def_word(
        name=",",
        lexeme=than_lexeme,
        word_form=WordForm.HEADWORD,
        locations=[Location([grammar_vectors["conj"]], grammatical_concepts_space)],
    )

    # Domain Specific Knowledge

    same_different_concept = homer.def_concept(
        name="same-different",
        parent_space=correspondential_concepts_space,
        distance_function=centroid_euclidean_distance,
    )
    same_different_space = homer.def_conceptual_space(
        name="same-different",
        locations=[Location([], correspondential_concepts_space)],
        parent_concept=same_different_concept,
        is_basic_level=True,
    )
    same = homer.def_concept(
        name="same",
        classifier=SamenessClassifier(),
        parent_space=same_different_space,
        distance_function=centroid_euclidean_distance,
    )
    different = homer.def_concept(
        name="different",
        classifier=DifferentnessClassifier(),
        parent_space=same_different_space,
        distance_function=centroid_euclidean_distance,
    )
    temperature_concept = homer.def_concept(
        name="temperature",
        parent_space=label_concepts_space,
        distance_function=centroid_euclidean_distance,
    )
    temperature_space = homer.def_conceptual_space(
        name="temperature",
        parent_concept=temperature_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        is_basic_level=True,
    )
    hot = homer.def_concept(
        name="hot",
        locations=[Location([[22]], temperature_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    hot_lexeme = homer.def_lexeme(
        headword="hot",
        parent_concept=hot,
    )
    hot_word = homer.def_word(
        name="hot",
        lexeme=hot_lexeme,
        locations=[Location([grammar_vectors["adj"]], grammatical_concepts_space)],
    )
    hotter = homer.def_concept(
        name="hotter",
        locations=[TwoPointLocation([[math.nan]], [[math.nan]], temperature_space)],
        classifier=DifferenceClassifier(4),
        structure_type=Relation,
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    homer.def_concept_link(hot, hotter, activation=1.0)
    hotter_lexeme = homer.def_lexeme(
        headword="hotter",
        parent_concept=hotter,
    )
    hotter_word = homer.def_word(
        name="hotter",
        lexeme=hotter_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    warm = homer.def_concept(
        name="warm",
        locations=[Location([[16]], temperature_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    warm_lexeme = homer.def_lexeme(
        headword="warm",
        parent_concept=warm,
    )
    warm_word = homer.def_word(
        name="warm",
        lexeme=warm_lexeme,
        locations=[Location([grammar_vectors["adj"]], grammatical_concepts_space)],
    )
    warmer_word = homer.def_word(
        name="warmer",
        lexeme=warm_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    mild = homer.def_concept(
        name="mild",
        locations=[Location([[10]], temperature_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    mild_lexeme = homer.def_lexeme(
        headword="mild",
        parent_concept=mild,
    )
    mild_word = homer.def_word(
        name="mild",
        lexeme=mild_lexeme,
        locations=[Location([grammar_vectors["adj"]], grammatical_concepts_space)],
    )
    milder_word = homer.def_word(
        name="milder",
        lexeme=mild_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    cold = homer.def_concept(
        name="cold",
        locations=[Location([[4]], temperature_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    cold_lexeme = homer.def_lexeme(
        headword="cold",
        parent_concept=cold,
    )
    cold_word = homer.def_word(
        name="cold",
        lexeme=cold_lexeme,
        locations=[Location([grammar_vectors["adj"]], grammatical_concepts_space)],
    )
    colder = homer.def_concept(
        name="colder",
        locations=[TwoPointLocation([[math.nan]], [[math.nan]], temperature_space)],
        classifier=DifferenceClassifier(-4),
        structure_type=Relation,
        parent_space=temperature_space,
        distance_function=centroid_euclidean_distance,
    )
    homer.def_concept_link(cold, colder, activation=1.0)
    colder_lexeme = homer.def_lexeme(
        headword="colder",
        parent_concept=colder,
    )
    colder_word = homer.def_word(
        name="colder",
        lexeme=colder_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )

    location_concept = homer.def_concept(
        name="location",
        parent_space=label_concepts_space,
        distance_function=centroid_euclidean_distance,
    )
    north_south_space = homer.def_conceptual_space(
        name="north-south",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [[c[0]] for c in location.coordinates]
        },
    )
    west_east_space = homer.def_conceptual_space(
        name="west-east",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [[c[1]] for c in location.coordinates]
        },
    )
    nw_se_space = homer.def_conceptual_space(
        name="nw-se",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                [statistics.fmean(c)] for c in location.coordinates
            ]
        },
    )
    ne_sw_space = homer.def_conceptual_space(
        name="ne-sw",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=1,
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                [statistics.fmean([c[0], 4 - c[1]])] for c in location.coordinates
            ]
        },
    )
    location_space = homer.def_conceptual_space(
        name="location",
        parent_concept=location_concept,
        locations=[Location([], label_concepts_space)],
        no_of_dimensions=2,
        dimensions=[north_south_space, west_east_space],
        sub_spaces=[north_south_space, west_east_space, nw_se_space, ne_sw_space],
        is_basic_level=True,
    )
    north = homer.def_concept(
        name="north",
        locations=[Location([[0, 2]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    north_lexeme = homer.def_lexeme(
        headword="north",
        parent_concept=north,
    )
    north_word = homer.def_word(
        name="north",
        lexeme=north_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    norther_word = homer.def_word(
        name="further north",
        lexeme=north_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    south = homer.def_concept(
        name="south",
        locations=[Location([[5, 2]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    south_lexeme = homer.def_lexeme(
        headword="south",
        parent_concept=south,
    )
    south_word = homer.def_word(
        name="south",
        lexeme=south_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    souther_word = homer.def_word(
        name="further south",
        lexeme=south_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    east = homer.def_concept(
        name="east",
        locations=[Location([[2.5, 4]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    east_lexeme = homer.def_lexeme(
        headword="east",
        parent_concept=east,
    )
    east_word = homer.def_word(
        name="east",
        lexeme=east_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    easter_word = homer.def_word(
        name="further east",
        lexeme=east_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    west = homer.def_concept(
        name="west",
        locations=[Location([[2.5, 0]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    west_lexeme = homer.def_lexeme(
        headword="west",
        parent_concept=west,
    )
    west_word = homer.def_word(
        name="west",
        lexeme=west_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    wester_word = homer.def_word(
        name="further west",
        lexeme=west_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    northwest = homer.def_concept(
        name="northwest",
        locations=[Location([[0, 0]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    northwest_lexeme = homer.def_lexeme(
        headword="northwest",
        parent_concept=northwest,
    )
    northwest_word = homer.def_word(
        name="northwest",
        lexeme=northwest_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    northwester_word = homer.def_word(
        name="further northwest",
        lexeme=northwest_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    northeast = homer.def_concept(
        name="northeast",
        locations=[Location([[0, 4]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    northeast_lexeme = homer.def_lexeme(
        headword="northeast",
        parent_concept=northeast,
    )
    northeast_word = homer.def_word(
        name="northeast",
        lexeme=northeast_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    northeaster_word = homer.def_word(
        name="further northeast",
        lexeme=northeast_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    southwest = homer.def_concept(
        name="southwest",
        locations=[Location([[5, 0]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    southwest_lexeme = homer.def_lexeme(
        headword="southwest",
        parent_concept=southwest,
    )
    southwest_word = homer.def_word(
        name="southwest",
        lexeme=southwest_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    southwester_word = homer.def_word(
        name="further southwest",
        lexeme=southwest_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    southeast = homer.def_concept(
        name="southeast",
        locations=[Location([[5, 4]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    southeast_lexeme = homer.def_lexeme(
        headword="southeast",
        parent_concept=southeast,
    )
    southeast_word = homer.def_word(
        name="southeast",
        lexeme=southeast_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    southeaster_word = homer.def_word(
        name="further southeast",
        lexeme=southeast_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )
    midlands = homer.def_concept(
        name="midlands",
        locations=[Location([[2.5, 2]], location_space)],
        classifier=ProximityClassifier(),
        structure_type=Label,
        parent_space=location_space,
        distance_function=centroid_euclidean_distance,
    )
    midlands_lexeme = homer.def_lexeme(
        headword="midlands",
        parent_concept=midlands,
    )
    midlands_word = homer.def_word(
        name="midlands",
        lexeme=midlands_lexeme,
        locations=[
            Location(
                add_vectors([grammar_vectors["adj"]], [grammar_vectors["noun"]]),
                grammatical_concepts_space,
            )
        ],
    )
    midlandser_word = homer.def_word(
        name="further inland",
        lexeme=midlands_lexeme,
        word_form=WordForm.COMPARATIVE,
        locations=[Location([grammar_vectors["jjr"]], grammatical_concepts_space)],
    )

    template_1 = homer.def_template(
        name="the [location] is [temperature]",
        parent_concept=text_concept,
        contents=[
            the_word,
            homer.def_word(word_form=WordForm.HEADWORD),
            is_word,
            homer.def_word(word_form=WordForm.HEADWORD),
        ],
    )
    template_1_location_space = location_space.instance_in_space(template_1)
    print(template_1_location_space)
    print(template_1_location_space.sub_spaces)
    homer.logger.log(template_1_location_space)
    template_1_temperature_space = temperature_space.instance_in_space(template_1)
    homer.logger.log(template_1_temperature_space)
    template_1_slot = homer.def_chunk(
        locations=[
            Location([], template_1),
            Location([[None, None]], template_1_location_space),
            Location([[None]], template_1_temperature_space),
        ],
        parent_space=template_1,
    )
    template_1_slot_location_label = homer.def_label(
        start=template_1_slot, parent_space=template_1_location_space
    )
    print("location label parent space:", template_1_slot_location_label.parent_space)
    template_1_slot_temperature_label = homer.def_label(
        start=template_1_slot, parent_space=template_1_temperature_space
    )
    print(
        "temperature label parent space:",
        template_1_slot_temperature_label.parent_space,
    )
    homer.def_correspondence(template_1_slot_location_label, template_1[1])
    homer.def_correspondence(template_1_slot_temperature_label, template_1[3])
    template_2 = homer.def_template(
        name="it is [temperature] in the [location]",
        parent_concept=text_concept,
        contents=[
            it_word,
            is_word,
            homer.def_word(word_form=WordForm.HEADWORD),
            in_word,
            the_word,
            homer.def_word(word_form=WordForm.HEADWORD),
        ],
    )
    template_2_location_space = location_space.instance_in_space(template_2)
    print(template_2_location_space)
    homer.logger.log(template_2_location_space)
    template_2_temperature_space = temperature_space.instance_in_space(template_2)
    homer.logger.log(template_2_temperature_space)
    template_2_slot = homer.def_chunk(
        locations=[
            Location([], template_2),
            Location([[None, None]], template_2_location_space),
            Location([[None]], template_2_temperature_space),
        ],
        parent_space=template_2,
    )
    template_2_slot_location_label = homer.def_label(
        start=template_2_slot, parent_space=template_2_location_space
    )
    template_2_slot_temperature_label = homer.def_label(
        start=template_2_slot, parent_space=template_2_temperature_space
    )
    homer.def_correspondence(template_2_slot_temperature_label, template_2[2])
    homer.def_correspondence(template_2_slot_location_label, template_2[5])
    template_4 = homer.def_template(
        name="it is [temperature.comparative] in the [location] than the [location]",
        parent_concept=text_concept,
        contents=[
            it_word,
            is_word,
            homer.def_word(word_form=WordForm.COMPARATIVE),
            in_word,
            the_word,
            homer.def_word(word_form=WordForm.HEADWORD),
            than_word,
            the_word,
            homer.def_word(word_form=WordForm.HEADWORD),
        ],
    )
    template_4_location_space = location_space.instance_in_space(template_4)
    homer.logger.log(template_4_location_space)
    template_4_temperature_space = temperature_space.instance_in_space(template_4)
    homer.logger.log(template_4_temperature_space)
    template_4_slot_1 = homer.def_chunk(
        locations=[
            Location([], template_4),
            Location([[None, None]], template_4_location_space),
            Location([[None]], template_4_temperature_space),
        ],
        parent_space=template_4,
    )
    template_4_slot_2 = homer.def_chunk(
        locations=[
            Location([], template_4),
            Location([[None, None]], template_4_location_space),
            Location([[None]], template_4_temperature_space),
        ],
        parent_space=template_4,
    )
    template_4_slot_1_location_label = homer.def_label(
        start=template_4_slot_1, parent_space=template_4_location_space
    )
    template_4_slot_2_location_label = homer.def_label(
        start=template_4_slot_2, parent_space=template_4_location_space
    )
    template_4_slots_temperature_relation = homer.def_relation(
        start=template_4_slot_1,
        end=template_4_slot_2,
        parent_space=template_4_temperature_space,
    )
    homer.def_correspondence(template_4_slots_temperature_relation, template_4[2])
    homer.def_correspondence(template_4_slot_1_location_label, template_4[5])
    homer.def_correspondence(template_4_slot_2_location_label, template_4[8])
    and_template = homer.def_template(
        name="[phrase] and [phrase]",
        parent_concept=discourse_concept,
        contents=[
            homer.def_phrase(label_concept=sentence_concept),
            and_word,
            homer.def_phrase(label_concept=sentence_concept),
        ],
    )
    list_template = homer.def_template(
        name="[phrase], [phrase]",
        parent_concept=discourse_concept,
        contents=[
            homer.def_phrase(label_concept=sentence_concept),
            comma_word,
            homer.def_phrase(label_concept=sentence_concept),
        ],
    )
    location_space_in_input = location_space.instance_in_space(input_space)
    homer.logger.log(location_space_in_input)
    temperature_space_in_input = temperature_space.instance_in_space(input_space)
    homer.logger.log(temperature_space_in_input)

    input_chunks = StructureCollection()
    for i, row in enumerate(problem):
        for j, cell in enumerate(row):
            locations = [
                Location([[i, j]], input_space),
                Location([[i, j]], location_space_in_input),
                Location([[cell]], temperature_space_in_input),
            ]
            members = StructureCollection()
            quality = 0.0
            chunk = Chunk(
                ID.new(Chunk),
                "",
                locations,
                members,
                input_space,
                quality,
            )
            logger.log(chunk)
            input_chunks.add(chunk)
            homer.bubble_chamber.chunks.add(chunk)
            input_space.add(chunk)
            location_space_in_input.add(chunk)
            temperature_space_in_input.add(chunk)

    return homer


for _ in range(1):
    homer = setup_homer()
    result = homer.run()
    with open("results.csv", "a") as f:
        f.write(str(result["codelets_run"]) + "\n")
