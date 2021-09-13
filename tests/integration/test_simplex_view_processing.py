# TODO: rename to test_simplex_view_processing
# add word projection into an output space at end of text
import math
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.builders.projection_builders import WordProjectionBuilder
from homer.codelets.builders.view_builders import SimplexViewBuilder
from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.codelets.evaluators.projection_evaluators import WordProjectionEvaluator
from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from homer.codelets.selectors import CorrespondenceSelector
from homer.codelets.selectors.projection_selectors import WordProjectionSelector
from homer.codelets.selectors.view_selectors import SimplexViewSelector
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.codelets.suggesters.projection_suggesters import WordProjectionSuggester
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
    input_concept,
    location_space,
    temperature_space,
    grammar_space,
    same_concept,
    hot_concept,
    cold_concept,
    hotter_concept,
    it_word,
    is_word,
    in_word,
    the_word,
    than_word,
    hotter_lexeme,
    hotter_word,
):
    input_space = ContextualSpace(
        "",
        "",
        "input",
        input_concept,
        StructureCollection(),
        conceptual_spaces=StructureCollection({temperature_space, location_space}),
    )
    bubble_chamber.contextual_spaces.add(input_space)

    # setup frame
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
    hot_label = Label(
        ID.new(Label),
        "",
        hot_chunk,
        hot_concept,
        [Location([[]], input_space), Location([[22]], temperature_space)],
        1.0,
    )
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
    cold_label = Label(
        ID.new(Label),
        "",
        cold_chunk,
        cold_concept,
        [Location([[]], input_space), Location([[4]], temperature_space)],
        1.0,
    )
    cold_chunk.links_out.add(cold_label)
    hot_to_cold_relation = Relation(
        ID.new(Relation),
        "",
        hot_chunk,
        cold_chunk,
        hotter_concept,
        [
            TwoPointLocation([[]], [[]], input_space),
            TwoPointLocation([[22]], [[4]], temperature_space),
        ],
        1.0,
    )
    hot_chunk.links_out.add(hot_to_cold_relation)
    cold_chunk.links_in.add(hot_to_cold_relation)

    # suggest and build view for input space and frame
    view_suggester = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"contextual_space": input_space, "frame": frame}, 1
    )
    view_suggester.run()
    assert CodeletResult.SUCCESS == view_suggester.result

    view_builder = view_suggester.child_codelets[0]
    assert isinstance(view_builder, SimplexViewBuilder)
    view_builder.run()
    assert CodeletResult.SUCCESS == view_builder.result
    view = view_builder.child_structures.where(is_simplex_view=True).get()
    original_view_quality = view.quality
    original_view_activation = view.activation

    view_evaluator = view_builder.child_codelets[0]
    assert isinstance(view_evaluator, SimplexViewEvaluator)
    view_evaluator.run()
    assert CodeletResult.SUCCESS == view_evaluator.result
    assert view.quality == original_view_quality

    # build correspondences
    correspondence_suggester_1 = CorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": hot_to_cold_relation,
            "target_space_two": None,
            "target_structure_two": None,
            "target_conceptual_space": None,
            "parent_concept": None,
        },
        1.0,
    )
    correspondence_suggester_1.run()
    assert CodeletResult.SUCCESS == correspondence_suggester_1.result

    correspondence_builder_1 = correspondence_suggester_1.child_codelets[0]
    assert isinstance(correspondence_builder_1, CorrespondenceBuilder)
    correspondence_builder_1.run()
    assert CodeletResult.SUCCESS == correspondence_builder_1.result
    correspondence_1 = correspondence_builder_1.child_structures.get()
    assert correspondence_1.start.parent_space == input_space
    assert correspondence_1.end.parent_space == view.input_frames.get().input_space
    original_correspondence_1_quality = correspondence_1.quality
    original_correspondence_1_activation = correspondence_1.activation

    correspondence_evaluator_1 = correspondence_builder_1.child_codelets[0]
    assert isinstance(correspondence_evaluator_1, CorrespondenceEvaluator)
    correspondence_evaluator_1.run()
    assert CodeletResult.SUCCESS == correspondence_evaluator_1.result
    assert correspondence_1.quality > original_correspondence_1_quality

    correspondence_selector_1 = correspondence_evaluator_1.child_codelets[0]
    assert isinstance(correspondence_selector_1, CorrespondenceSelector)
    correspondence_selector_1.run()
    assert CodeletResult.SUCCESS == correspondence_selector_1.result
    correspondence_1.update_activation()
    assert correspondence_1.activation > original_correspondence_1_activation

    # re-evaluate and select view as correspondences are added
    view_evaluator_2 = SimplexViewEvaluator.spawn(
        "", bubble_chamber, StructureCollection({view}), 1.0
    )
    view_evaluator_2.run()
    assert CodeletResult.SUCCESS == view_evaluator_2.result
    assert view.quality > original_view_quality
    view_quality_after_evaluator_2 = view.quality

    view_selector_2 = view_evaluator_2.child_codelets[0]
    assert isinstance(view_selector_2, SimplexViewSelector)
    view_selector_2.run()
    assert CodeletResult.SUCCESS == view_selector_2.result
    view.update_activation()
    assert view.activation > original_view_activation
    view_activation_after_selector_2 = view.activation

    # project words into output
    frame = view.input_spaces.where(is_frame=True).get()
    target_word_1 = frame.output_space.contents.where(is_word=True, is_slot=False).get()
    word_projection_suggester_1 = WordProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": target_word_1},
        1.0,
    )
    word_projection_suggester_1.run()
    assert CodeletResult.SUCCESS == word_projection_suggester_1.result

    word_projection_builder_1 = word_projection_suggester_1.child_codelets[0]
    assert isinstance(word_projection_builder_1, WordProjectionBuilder)
    word_projection_builder_1.run()
    assert CodeletResult.SUCCESS == word_projection_builder_1.result
    assert 1 == len(view.output_space.contents.where(is_word=True))
    word_1 = word_projection_builder_1.child_structures.where(is_word=True).get()
    original_word_1_quality = word_1.quality
    original_word_1_activation = word_1.activation

    word_projection_evaluator_1 = word_projection_builder_1.child_codelets[0]
    assert isinstance(word_projection_evaluator_1, WordProjectionEvaluator)
    word_projection_evaluator_1.run()
    assert CodeletResult.SUCCESS == word_projection_evaluator_1.result
    assert word_1.quality > original_word_1_quality

    word_projection_selector_1 = word_projection_evaluator_1.child_codelets[0]
    assert isinstance(word_projection_selector_1, WordProjectionSelector)
    word_projection_selector_1.run()
    assert CodeletResult.SUCCESS == word_projection_selector_1.result
    word_1.update_activation()
    assert word_1.activation > original_word_1_activation

    word_correspondee = correspondence_1.slot_argument
    frame_correspondence = word_correspondee.correspondences_to_space(
        frame.output_space
    ).get()
    target_word_2 = frame_correspondence.end
    word_projection_suggester_2 = WordProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": target_word_2},
        1.0,
    )
    word_projection_suggester_2.run()
    assert CodeletResult.SUCCESS == word_projection_suggester_2.result

    word_projection_builder_2 = word_projection_suggester_2.child_codelets[0]
    assert isinstance(word_projection_builder_2, WordProjectionBuilder)
    word_projection_builder_2.run()
    assert CodeletResult.SUCCESS == word_projection_builder_2.result
    assert 2 == len(view.output_space.contents.where(is_word=True))
    word_2 = word_projection_builder_2.child_structures.where(is_word=True).get()
    original_word_2_quality = word_2.quality
    original_word_2_activation = word_2.activation

    word_projection_evaluator_2 = word_projection_builder_2.child_codelets[0]
    assert isinstance(word_projection_evaluator_2, WordProjectionEvaluator)
    word_projection_evaluator_2.run()
    assert CodeletResult.SUCCESS == word_projection_evaluator_2.result
    assert word_2.quality > original_word_2_quality

    word_projection_selector_2 = word_projection_evaluator_2.child_codelets[0]
    assert isinstance(word_projection_selector_2, WordProjectionSelector)
    word_projection_selector_2.run()
    assert CodeletResult.SUCCESS == word_projection_selector_2.result
    word_2.update_activation()
    assert word_2.activation > original_word_2_activation

    # re-evaluate view
    view_evaluator_3 = SimplexViewEvaluator.spawn(
        "", bubble_chamber, StructureCollection({view}), 1.0
    )
    view_evaluator_3.run()
    assert CodeletResult.SUCCESS == view_evaluator_3.result
    assert view.quality > view_quality_after_evaluator_2

    view_selector_3 = view_evaluator_3.child_codelets[0]
    assert isinstance(view_selector_3, SimplexViewSelector)
    view_selector_3.run()
    assert CodeletResult.SUCCESS == view_selector_3.result
    view.update_activation()
    assert view.activation >= view_activation_after_selector_2
