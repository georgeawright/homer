import pytest
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
    comparison_frame,
):
    text_space = ContextualSpace(
        "",
        "",
        "text",
        text_concept,
        bubble_chamber.new_structure_collection(),
        conceptual_spaces=bubble_chamber.new_structure_collection(grammar_space),
        links_in=bubble_chamber.new_structure_collection(),
        links_out=bubble_chamber.new_structure_collection(),
        parent_spaces=bubble_chamber.new_structure_collection(),
    )
    bubble_chamber.contextual_spaces.add(text_space)

    # setup text space with words
    text_0 = it_word.copy_to_location(
        Location([[0]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )
    text_1 = is_word.copy_to_location(
        Location([[1]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )
    text_2 = hotter_word.copy_to_location(
        Location([[2]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )
    text_3 = in_word.copy_to_location(
        Location([[3]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )
    text_4 = the_word.copy_to_location(
        Location([[4]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )
    text_5 = south_word.copy_to_location(
        Location([[5]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )
    text_6 = than_word.copy_to_location(
        Location([[6]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )
    text_7 = the_word.copy_to_location(
        Location([[7]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )
    text_8 = north_word.copy_to_location(
        Location([[8]], text_space), quality=1.0, bubble_chamber=bubble_chamber
    )

    # suggest and build view for input space and frame
    view_suggester = SimplexViewSuggester.spawn(
        "",
        bubble_chamber,
        {"contextual_space": text_space, "frame": comparison_frame},
        1,
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
            "target_structure_two": bubble_chamber.new_structure_collection(
                *[
                    word
                    for word in view_frame_input.contents
                    if word.location_in_space(view_frame_input).coordinates == [[2]]
                ]
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
    ] = bubble_chamber.new_structure_collection(
        *[
            word
            for word in view_frame_input.contents
            if word.location_in_space(view_frame_input).coordinates == [[5]]
        ]
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
    ] = bubble_chamber.new_structure_collection(
        *[
            word
            for word in view_frame_input.contents
            if word.location_in_space(view_frame_input).coordinates == [[8]]
        ]
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
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1.0
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
    assert chunk_projection_1 in view.output_space.contents
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

    chunk_projection_suggester_2 = None
    for child_codelet in chunk_projection_selector_1.child_codelets:
        if isinstance(child_codelet, ChunkProjectionSuggester):
            chunk_projection_suggester_2 = child_codelet
    chunk_projection_suggester_2.run()
    assert CodeletResult.SUCCESS == chunk_projection_suggester_2.result

    chunk_projection_builder_2 = chunk_projection_suggester_2.child_codelets[0]
    assert isinstance(chunk_projection_builder_2, ChunkProjectionBuilder)
    chunk_projection_builder_2.run()
    assert CodeletResult.SUCCESS == chunk_projection_builder_2.result
    chunk_projection_2 = chunk_projection_builder_2.child_structures.where(
        is_chunk=True
    ).get()
    assert chunk_projection_2 in view.output_space.contents
    original_chunk_projection_2_quality = chunk_projection_2.quality
    original_chunk_projection_2_activation = chunk_projection_2.activation

    chunk_projection_evaluator_2 = chunk_projection_builder_2.child_codelets[0]
    assert isinstance(chunk_projection_evaluator_2, ChunkProjectionEvaluator)
    chunk_projection_evaluator_2.run()
    assert CodeletResult.SUCCESS == chunk_projection_evaluator_2.result
    assert chunk_projection_2.quality > original_chunk_projection_2_quality

    chunk_projection_selector_2 = chunk_projection_evaluator_2.child_codelets[0]
    assert isinstance(chunk_projection_selector_2, ChunkProjectionSelector)
    chunk_projection_selector_2.run()
    assert CodeletResult.SUCCESS == chunk_projection_selector_2.result
    chunk_projection_2.update_activation()
    assert chunk_projection_2.activation > original_chunk_projection_2_activation

    target_label = view_frame_output.contents.where(is_label=True).get()
    label_projection_suggester_1 = LabelProjectionSuggester.spawn(
        "", bubble_chamber, {"target_view": view, "target_projectee": target_label}, 1.0
    )
    label_projection_suggester_1.run()
    assert CodeletResult.SUCCESS == label_projection_suggester_1.result

    label_projection_builder_1 = label_projection_suggester_1.child_codelets[0]
    assert isinstance(label_projection_builder_1, LabelProjectionBuilder)
    label_projection_builder_1.run()
    assert CodeletResult.SUCCESS == label_projection_builder_1.result
    label_projection_1 = label_projection_builder_1.child_structures.where(
        is_label=True
    ).get()
    assert label_projection_1 in view.output_space.contents
    original_label_projection_1_quality = label_projection_1.quality
    original_label_projection_1_activation = label_projection_1.activation

    label_projection_evaluator_1 = label_projection_builder_1.child_codelets[0]
    assert isinstance(label_projection_evaluator_1, LabelProjectionEvaluator)
    label_projection_evaluator_1.run()
    assert CodeletResult.SUCCESS == label_projection_evaluator_1.result
    assert label_projection_1.quality > original_label_projection_1_quality

    label_projection_selector_1 = label_projection_evaluator_1.child_codelets[0]
    assert isinstance(label_projection_selector_1, LabelProjectionSelector)
    label_projection_selector_1.run()
    assert CodeletResult.SUCCESS == label_projection_selector_1.result
    label_projection_1.update_activation()
    assert label_projection_1.activation > original_label_projection_1_activation

    label_projection_suggester_2 = None
    for child_codelet in label_projection_selector_1.child_codelets:
        if isinstance(child_codelet, LabelProjectionSuggester):
            label_projection_suggester_2 = child_codelet
    label_projection_suggester_2.run()
    assert CodeletResult.SUCCESS == label_projection_suggester_2.result

    label_projection_builder_2 = label_projection_suggester_2.child_codelets[0]
    assert isinstance(label_projection_builder_2, LabelProjectionBuilder)
    label_projection_builder_2.run()
    assert CodeletResult.SUCCESS == label_projection_builder_2.result
    label_projection_2 = label_projection_builder_2.child_structures.where(
        is_label=True
    ).get()
    assert label_projection_2 in view.output_space.contents
    original_label_projection_2_quality = label_projection_2.quality
    original_label_projection_2_activation = label_projection_2.activation

    label_projection_evaluator_2 = label_projection_builder_2.child_codelets[0]
    assert isinstance(label_projection_evaluator_2, LabelProjectionEvaluator)
    label_projection_evaluator_2.run()
    assert CodeletResult.SUCCESS == label_projection_evaluator_2.result
    assert label_projection_2.quality > original_label_projection_2_quality

    label_projection_selector_2 = label_projection_evaluator_2.child_codelets[0]
    assert isinstance(label_projection_selector_2, LabelProjectionSelector)
    label_projection_selector_2.run()
    assert CodeletResult.SUCCESS == label_projection_selector_2.result
    label_projection_2.update_activation()
    assert label_projection_2.activation > original_label_projection_2_activation

    target_relation = view_frame_output.contents.where(is_relation=True).get()
    relation_projection_suggester_1 = RelationProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": target_relation},
        1.0,
    )
    relation_projection_suggester_1.run()
    assert CodeletResult.SUCCESS == relation_projection_suggester_1.result

    relation_projection_builder_1 = relation_projection_suggester_1.child_codelets[0]
    assert isinstance(relation_projection_builder_1, RelationProjectionBuilder)
    relation_projection_builder_1.run()
    assert CodeletResult.SUCCESS == relation_projection_builder_1.result
    relation_projection_1 = relation_projection_builder_1.child_structures.where(
        is_relation=True
    ).get()
    assert relation_projection_1 in view.output_space.contents
    original_relation_projection_1_quality = relation_projection_1.quality
    original_relation_projection_1_activation = relation_projection_1.activation

    relation_projection_evaluator_1 = relation_projection_builder_1.child_codelets[0]
    assert isinstance(relation_projection_evaluator_1, RelationProjectionEvaluator)
    relation_projection_evaluator_1.run()
    assert CodeletResult.SUCCESS == relation_projection_evaluator_1.result
    assert relation_projection_1.quality > original_relation_projection_1_quality

    relation_projection_selector_1 = relation_projection_evaluator_1.child_codelets[0]
    assert isinstance(relation_projection_selector_1, RelationProjectionSelector)
    relation_projection_selector_1.run()
    assert CodeletResult.SUCCESS == relation_projection_selector_1.result
    relation_projection_1.update_activation()
    assert relation_projection_1.activation > original_relation_projection_1_activation

    # re-evaluate view

    view_evaluator_3 = SimplexViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1.0
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
