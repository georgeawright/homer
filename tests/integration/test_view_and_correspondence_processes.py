import math
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.builders.view_builders import SimplexViewBuilder
from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from homer.codelets.selectors import CorrespondenceSelector
from homer.codelets.selectors.view_selectors import SimplexViewSelector
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.codelets.suggesters.view_suggesters import SimplexViewSuggester
from homer.id import ID
from homer.location import Location
from homer.locations import TwoPointLocation
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk, Concept, Word
from homer.structures.spaces import ConceptualSpace, ContextualSpace, Frame
from homer.structures.views import SimplexView
from homer.tools import centroid_euclidean_distance
from homer.word_form import WordForm


def test_view_and_correspondence_processes(
    bubble_chamber,
    location_space,
    temperature_space,
    grammar_space,
    sameness_concept,
    hot_concept,
    cold_concept,
    hotter_concept,
    it_word,
    is_word,
    in_word,
    the_word,
    than_word,
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

    # setup frame
    frame_input_space = ContextualSpace(
        "", "", "", None, StructureCollection(), [location_space, temperature_space]
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
    label_one = Label(ID.new(Label), "", chunk_one, None, frame_input_space, 1.0)
    chunk_one.links_out.add(label_one)
    label_two = Label(ID.new(Label), "", chunk_two, None, frame_input_space, 1.0)
    chunk_two.links_out.add(label_two)
    one_to_two_relation = Relation(
        ID.new(Relation), "", chunk_one, chunk_two, None, frame_input_space, 1.0
    )
    chunk_one.links_out.add(one_to_two_relation)
    chunk_two.links_in.add(one_to_two_relation)
    frame_output_space = ContextualSpace(
        "", "", "", None, StructureCollection(), [grammar_space]
    )
    word_0 = it_word.copy_to_location(Location([[0]], frame_output_space), quality=1.0)
    word_1 = is_word.copy_to_location(Location([[1]], frame_output_space), quality=1.0)
    word_2 = Word(
        ID.new(Word),
        "",
        None,
        None,
        WordForm.HEADWORD,
        [Location([[2]], frame_output_space), Location([[None]], grammar_space)],
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
        [Location([[5]], frame_output_space), Location([[None]], grammar_space)],
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
        [Location([[8]], frame_output_space), Location([[None]], grammar_space)],
        frame_output_space,
        1.0,
    )
    frame_output_space.add(word_8)
    word_2_correspondence = Correspondence(
        "",
        "",
        one_to_two_relation,
        word_2,
        temperature_space,
        temperature_space,
        [
            one_to_two_relation.location_in_space(one_to_two_relation.parent_space),
            word_2.location_in_space(word_2.parent_space),
        ],
        sameness_concept,
        temperature_space,
        None,
        1.0,
    )
    word_5_correspondence = Correspondence(
        "",
        "",
        label_one,
        word_5,
        location_space,
        location_space,
        [
            label_one.location_in_space(label_one.parent_space),
            word_5.location_in_space(word_5.parent_space),
        ],
        sameness_concept,
        location_space,
        None,
        1.0,
    )
    word_8_correspondence = Correspondence(
        "",
        "",
        label_two,
        word_8,
        location_space,
        location_space,
        [
            label_two.location_in_space(label_two.parent_space),
            word_8.location_in_space(word_8.parent_space),
        ],
        sameness_concept,
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

    # setup input space with chunks, labels, relations
    hot_chunk = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], input_space),
            Location([[0, 0]], location_space),
            Location([[22]], temperature_space),
        ],
        StructureCollection(),
        input_space,
        1.0,
    )
    input_space.add(hot_chunk)
    location_space.add(hot_chunk)
    temperature_space.add(hot_chunk)
    hot_label = Label(ID.new(Label), "", hot_chunk, hot_concept, input_space, 1.0)
    hot_chunk.links_out.add(hot_label)
    cold_chunk = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], input_space),
            Location([[0, 1]], location_space),
            Location([[4]], temperature_space),
        ],
        StructureCollection(),
        input_space,
        1.0,
    )
    input_space.add(cold_chunk)
    location_space.add(cold_chunk)
    temperature_space.add(cold_chunk)
    cold_label = Label(ID.new(Label), "", cold_chunk, cold_concept, input_space, 1.0)
    cold_chunk.links_out.add(cold_label)
    hot_to_cold_relation = Relation(
        ID.new(Relation), "", hot_chunk, cold_chunk, hotter_concept, input_space, 1.0
    )
    hot_chunk.links_out.add(hot_to_cold_relation)
    cold_chunk.links_in.add(hot_to_cold_relation)

    # suggest and build view for input space and frame
    suggester = SimplexViewSuggester.spawn(
        "", bubble_chamber, StructureCollection({input_space, frame}), 1
    )
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result

    builder = suggester.child_codelets[0]
    assert isinstance(builder, SimplexViewBuilder)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    view = builder.child_structures.where(is_simplex_view=True).get()
    original_view_quality = view.quality
    original_view_activation = view.activation

    evaluator = builder.child_codelets[0]
    assert isinstance(evaluator, SimplexViewEvaluator)
    evaluator.run()
    assert CodeletResult.SUCCESS == evaluator.result
    assert view.quality == original_view_quality

    # build correspondences

    # re-evaluate and select view as correspondences are added
