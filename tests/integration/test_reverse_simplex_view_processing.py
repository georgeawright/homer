from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.builders.projection_builders import (
    ChunkProjectionBuilder,
    LabelProjectionBuilder,
    RelationProjectionBuilder,
)
from homer.codelets.builders.view_builders import SimplexViewBuilder
from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.codelets.evaluators.projection_evaluators import (
    ChunkProjectionEvaluator,
    LabelProjectionEvaluator,
    RelationProjectionEvaluator,
)
from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from homer.codelets.selectors import CorrespondenceSelector
from homer.codelets.selectors.projection_selectors import (
    ChunkProjectionSelector,
    LabelProjectionSelector,
    RelationProjectionSelector,
)
from homer.codelets.selectors.view_selectors import SimplexViewSelector
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.codelets.suggesters.projection_suggesters import (
    ChunkProjectionSuggester,
    LabelProjectionSuggester,
    RelationProjectionSuggester,
)
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


def test_reverse_simplex_view_processing(
    bubble_chamber,
    input_concept,
    text_concept,
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
    south_word,
    north_word,
):
    text_space = ContextualSpace(
        "",
        "",
        "text",
        text_concept,
        StructureCollection(),
        conceptual_spaces=StructureCollection({grammar_space}),
    )
    bubble_chamber.contextual_spaces.add(text_space)

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

    # setup text space with words
    text_0 = it_word.copy_to_location(Location([[0]], text_space), quality=1.0)
    text_1 = is_word.copy_to_location(Location([[1]], text_space), quality=1.0)
    text_2 = hotter_word.copy_to_location(Location([[2]], text_space), quality=1.0)
    text_3 = in_word.copy_to_location(Location([[3]], text_space), quality=1.0)
    text_4 = the_word.copy_to_location(Location([[4]], text_space), quality=1.0)
    text_5 = south_word.copy_to_location(Location([[5]], text_space), quality=1.0)
    text_6 = than_word.copy_to_location(Location([[6]], text_space), quality=1.0)
    text_7 = the_word.copy_to_location(Location([[7]], frame_output_space), quality=1.0)
    text_8 = north_word.copy_to_location(Location([[8]], text_space), quality=1.0)

    # suggest and build view for input space and frame
    view_suggester = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"contextual_space": text_space, "frame": frame}, 1
    )
    view_suggester.run()
    assert CodeletResult.SUCCESS == view_suggester.result

    view_builder = view_suggester.child_codelets[0]
    assert isinstance(view_builder, SimplexViewBuilder)
    view_builder.run()
    assert CodeletResult.SUCCESS == view_builder.result
    view = view_builder.child_structures.where(is_simplex_view=True).get()
    assert text_concept == view.input_frames.get().input_space.parent_concept
    assert input_concept == view.input_frames.get().output_space.parent_concept
    original_view_quality = view.quality
    original_view_activation = view.activation

    view_evaluator = view_builder.child_codelets[0]
    assert isinstance(view_evaluator, SimplexViewEvaluator)
    view_evaluator.run()
    assert CodeletResult.SUCCESS == view_evaluator.result
    assert view.quality == original_view_quality

    # build correspondences
    view_frame = view.input_frames.get()
    view_frame_input = view_frame.input_space
    correspondence_suggester_1 = CorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": text_space,
            "target_structure_one": text_2,
            "target_space_two": view_frame_input,
            "target_structure_two": StructureCollection(
                {
                    word
                    for word in view_frame_input.contents
                    if word.location_in_space(view_frame_input).coordinates == [[2]]
                }
            ).get(),
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
    assert correspondence_1.start.parent_space == text_space
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

    correspondence_suggester_2 = (
        correspondence_selector_1.child_codelets[0]
        if isinstance(
            correspondence_selector_1.child_codelets[0], CorrespondenceSuggester
        )
        else correspondence_selector_1.child_codelets[1]
    )
    correspondence_suggester_2._target_structures["target_structure_one"] = text_5
    correspondence_suggester_2._target_structures["target_space_two"] = view_frame_input
    correspondence_suggester_2._target_structures[
        "target_structure_two"
    ] = StructureCollection(
        {
            word
            for word in view_frame_input.contents
            if word.location_in_space(view_frame_input).coordinates == [[5]]
        }
    ).get()
    correspondence_suggester_2.run()
    assert CodeletResult.SUCCESS == correspondence_suggester_2.result

    correspondence_builder_2 = correspondence_suggester_2.child_codelets[0]
    assert isinstance(correspondence_builder_2, CorrespondenceBuilder)
    correspondence_builder_2.run()
    assert CodeletResult.SUCCESS == correspondence_builder_2.result
    correspondence_2 = correspondence_builder_2.child_structures.get()
    assert correspondence_2.start.parent_space == text_space
    assert correspondence_2.end.parent_space == view.input_frames.get().input_space
    original_correspondence_2_quality = correspondence_2.quality
    original_correspondence_2_activation = correspondence_2.activation

    correspondence_evaluator_2 = correspondence_builder_2.child_codelets[0]
    assert isinstance(correspondence_evaluator_2, CorrespondenceEvaluator)
    correspondence_evaluator_2.run()
    assert CodeletResult.SUCCESS == correspondence_evaluator_2.result
    assert correspondence_2.quality > original_correspondence_2_quality

    correspondence_selector_2 = correspondence_evaluator_2.child_codelets[0]
    assert isinstance(correspondence_selector_2, CorrespondenceSelector)
    correspondence_selector_2.run()
    assert CodeletResult.SUCCESS == correspondence_selector_2.result
    correspondence_2.update_activation()
    assert correspondence_2.activation > original_correspondence_2_activation

    correspondence_suggester_3 = (
        correspondence_selector_2.child_codelets[0]
        if isinstance(
            correspondence_selector_2.child_codelets[0], CorrespondenceSuggester
        )
        else correspondence_selector_2.child_codelets[1]
    )
    correspondence_suggester_3._target_structures["target_structure_one"] = text_8
    correspondence_suggester_3._target_structures["target_space_two"] = view_frame_input
    correspondence_suggester_3._target_structures[
        "target_structure_two"
    ] = StructureCollection(
        {
            word
            for word in view_frame_input.contents
            if word.location_in_space(view_frame_input).coordinates == [[8]]
        }
    ).get()
    correspondence_suggester_3.run()
    assert CodeletResult.SUCCESS == correspondence_suggester_3.result

    correspondence_builder_3 = correspondence_suggester_3.child_codelets[0]
    assert isinstance(correspondence_builder_3, CorrespondenceBuilder)
    correspondence_builder_3.run()
    assert CodeletResult.SUCCESS == correspondence_builder_3.result
    correspondence_3 = correspondence_builder_3.child_structures.get()
    assert correspondence_3.start.parent_space == text_space
    assert correspondence_3.end.parent_space == view.input_frames.get().input_space
    original_correspondence_3_quality = correspondence_3.quality
    original_correspondence_3_activation = correspondence_3.activation

    correspondence_evaluator_3 = correspondence_builder_3.child_codelets[0]
    assert isinstance(correspondence_evaluator_3, CorrespondenceEvaluator)
    correspondence_evaluator_3.run()
    assert CodeletResult.SUCCESS == correspondence_evaluator_3.result
    assert correspondence_3.quality > original_correspondence_3_quality

    correspondence_selector_3 = correspondence_evaluator_3.child_codelets[0]
    assert isinstance(correspondence_selector_3, CorrespondenceSelector)
    correspondence_selector_3.run()
    assert CodeletResult.SUCCESS == correspondence_selector_3.result
    correspondence_3.update_activation()
    assert correspondence_3.activation > original_correspondence_3_activation

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

    # project chunks, labels, relations into output
    view_frame_output = view_frame.output_space
    target_chunk = view_frame_output.contents.where(is_chunk=True).get()
    chunk_projection_suggester_1 = ChunkProjectionSuggester.spawn(
        "", bubble_chamber, {"target_view": view, "target_projectee": target_chunk}, 1.0
    )
    chunk_projection_suggester_1.run()
    assert CodeletResult.SUCCESS == chunk_projection_suggester_1.result

    chunk_projection_builder_1 = chunk_projection_suggester_1.child_codelets[0]
    assert isinstance(chunk_projection_builder_1, ChunkProjectionBuilder)
    chunk_projection_builder_1.run()
    assert CodeletResult.SUCCESS == chunk_projection_builder_1.result
    chunk_projection_1 = chunk_projection_builder_1.child_structures.where(
        is_chunk=True
    ).get()
    original_chunk_projection_1_quality = chunk_projection_1.quality
    original_chunk_projection_1_activation = chunk_projection_1.activation

    chunk_projection_evaluator_1 = chunk_projection_builder_1.child_codelets[0]
    assert isinstance(chunk_projection_evaluator_1, ChunkProjectionEvaluator)
    chunk_projection_evaluator_1.run()
    assert CodeletResult.SUCCESS == chunk_projection_evaluator_1.result
    assert chunk_projection_1.quality > original_chunk_projection_1_quality

    chunk_projection_selector_1 = chunk_projection_evaluator_1.child_codelets[0]
    assert isinstance(chunk_projection_selector_1, ChunkProjectionSelector)
    chunk_projection_selector_1.run()
    assert CodeletResult.SUCCESS == chunk_projection_selector_1.result
    chunk_projection_1.update_activation()
    assert chunk_projection_1.activation > original_chunk_projection_1_activation


#    chunk_projection_suggester_2 = ChunkProjectionSuggester()
#    label_projection_suggester_1 = LabelProjectionSuggester()
#    label_projection_suggester_2 = LabelProjectionSuggester()
#    relation_projection_suggester = RelationProjectionSuggester()

# re-evaluate view


#    view_evaluator_3 = SimplexViewEvaluator.spawn(
#        "", bubble_chamber, StructureCollection({view}), 1.0
#    )
#    view_evaluator_3.run()
#    assert CodeletResult.SUCCESS == view_evaluator_3.result
#    assert view.quality > view_quality_after_evaluator_2
#
#    view_selector_3 = view_evaluator_3.child_codelets[0]
#    assert isinstance(view_selector_3, SimplexViewSelector)
#    view_selector_3.run()
#    assert CodeletResult.SUCCESS == view_selector_3.result
#    view.update_activation()
#    assert view.activation >= view_activation_after_selector_2
