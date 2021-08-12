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


def test_chunking_of_weather_data(
    bubble_chamber, location_space, temperature_space, sameness_rule
):
    input_space = ContextualSpace(
        "",
        "",
        "input",
        Mock(),
        StructureCollection(),
        conceptual_spaces=StructureCollection({temperature_space, location_space}),
    )
    bubble_chamber.contextual_spaces.add(input_space)

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
