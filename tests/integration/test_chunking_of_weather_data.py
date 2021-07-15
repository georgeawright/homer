import statistics
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.classifiers import SamenessClassifier
from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder
from homer.codelets.evaluators import ChunkEvaluator
from homer.codelets.selectors import ChunkSelector
from homer.codelets.suggesters import ChunkSuggester
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.structures.nodes import Chunk, Concept, Rule
from homer.structures.spaces import ConceptualSpace, ContextualSpace
from homer.tools import centroid_euclidean_distance


def test_chunking_of_weather_data():
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
    location_concept = Concept(
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
    north_south_space = ConceptualSpace(
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
    west_east_space = ConceptualSpace(
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
    nw_se_space = ConceptualSpace(
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
    ne_sw_space = ConceptualSpace(
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
    location_space = ConceptualSpace(
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
    bubble_chamber.contextual_spaces.add(location_space)
    temperature_concept = Concept(
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
    temperature_space = ConceptualSpace(
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
    bubble_chamber.conceptual_spaces.add(temperature_space)
    input_space = ContextualSpace(
        "",
        "",
        "input",
        Mock(),
        StructureCollection(),
        conceptual_spaces=StructureCollection({temperature_space, location_space}),
    )
    bubble_chamber.contextual_spaces.add(input_space)
    sameness_classifier = SamenessClassifier()
    sameness_concept = Concept(
        "",
        "",
        "sameness",
        [],
        sameness_classifier,
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    sameness_rule = Rule(
        "", "", "sameness", Mock(), sameness_concept, sameness_concept, None
    )
    bubble_chamber.rules.add(sameness_rule)

    # create input chunks
    raw_chunk_1 = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], input_space),
            Location([[0, 0]], location_space),
            Location([[10]], temperature_space),
        ],
        StructureCollection(),
        input_space,
        0,
    )
    input_space.add(raw_chunk_1)
    location_space.add(raw_chunk_1)
    temperature_space.add(raw_chunk_1)
    raw_chunk_2 = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], input_space),
            Location([[0, 1]], location_space),
            Location([[10]], temperature_space),
        ],
        StructureCollection(),
        input_space,
        0,
    )
    input_space.add(raw_chunk_2)
    location_space.add(raw_chunk_2)
    temperature_space.add(raw_chunk_2)
    raw_chunk_3 = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], input_space),
            Location([[1, 0]], location_space),
            Location([[10]], temperature_space),
        ],
        StructureCollection(),
        input_space,
        0,
    )
    input_space.add(raw_chunk_3)
    location_space.add(raw_chunk_3)
    temperature_space.add(raw_chunk_3)

    # create chunk suggester
    suggester = ChunkSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_space": input_space,
            "target_node": raw_chunk_1,
            "target_rule": sameness_rule,
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
            Location([[]], input_space),
            Location([[0, 1], [1, 1]], location_space),
            Location([[10], [5]], temperature_space),
        ],
        StructureCollection(),
        input_space,
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
    assert CodeletResult.SUCCESS == suggester_2.result

    # assert expansion of chunk is suggested
    builder_2 = suggester_2.child_codelets[0]
    assert isinstance(builder_2, ChunkBuilder)
    assert builder_2._target_structures["target_root"] == chunk
