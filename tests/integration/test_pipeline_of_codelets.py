import time
from homer.codelet_result import CodeletResult
from homer.codelets.builders import (
    ChunkBuilder,
    LabelBuilder,
    RelationBuilder,
)
from homer.codelets.builders.correspondence_builders import (
    PotentialSubFrameToFrameCorrespondenceBuilder,
    SpaceToFrameCorrespondenceBuilder,
    SubFrameToFrameCorrespondenceBuilder,
)
from homer.codelets.builders.projection_builders import (
    ChunkProjectionBuilder,
    LabelProjectionBuilder,
    LetterChunkProjectionBuilder,
    RelationProjectionBuilder,
)
from homer.codelets.builders.view_builders import SimplexViewBuilder
from homer.codelets.evaluators import (
    CorrespondenceEvaluator,
    ChunkEvaluator,
    LabelEvaluator,
    RelationEvaluator,
)
from homer.codelets.evaluators.projection_evaluators import (
    ChunkProjectionEvaluator,
    LabelProjectionEvaluator,
    LetterChunkProjectionEvaluator,
    RelationProjectionEvaluator,
)
from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator
from homer.codelets.selectors import (
    CorrespondenceSelector,
    ChunkSelector,
    LabelSelector,
    RelationSelector,
)
from homer.codelets.selectors.projection_selectors import (
    ChunkProjectionSelector,
    LabelProjectionSelector,
    LetterChunkProjectionSelector,
    RelationProjectionSelector,
)
from homer.codelets.selectors.view_selectors import SimplexViewSelector
from homer.codelets.suggesters import (
    ChunkSuggester,
    LabelSuggester,
    RelationSuggester,
)
from homer.codelets.suggesters.correspondence_suggesters import (
    PotentialSubFrameToFrameCorrespondenceSuggester,
    SpaceToFrameCorrespondenceSuggester,
    SubFrameToFrameCorrespondenceSuggester,
)
from homer.codelets.suggesters.projection_suggesters import (
    ChunkProjectionSuggester,
    LabelProjectionSuggester,
    LetterChunkProjectionSuggester,
    RelationProjectionSuggester,
)
from homer.codelets.suggesters.view_suggesters import SimplexViewSuggester


def test_pipeline_of_codelets(homer):
    start_time = time.time()
    bubble_chamber = homer.bubble_chamber
    input_space = bubble_chamber.contextual_spaces["input"]
    location_space = bubble_chamber.conceptual_spaces["location"]

    # START: label a raw chunk
    target_node = input_space.contents.filter(
        lambda x: x.location_in_space(location_space).coordinates == [[0, 0]]
    ).get()
    parent_concept = bubble_chamber.concepts["cold"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": target_node, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not target_node.has_label_with_name("cold")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert target_node.has_label_with_name("cold")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation
    # END: label a raw chunk

    # START: build and enlarge a sameness chunk
    codelet = ChunkSuggester.spawn(
        "",
        bubble_chamber,
        {"target_space": input_space, "target_node": target_node, "target_rule": None},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkBuilder)
    assert target_node.super_chunks.is_empty()
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert not target_node.super_chunks.is_empty()

    chunk = codelet.child_structures.where(is_slot=False).get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkEvaluator)
    assert 0 == chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkSelector)
    original_chunk_activation = chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk.update_activation()
    assert original_chunk_activation < chunk.activation

    # suggest an enlargement to the chunk
    codelet = [c for c in codelet.child_codelets if isinstance(c, ChunkSuggester)][0]
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk = codelet.child_structures.where(is_slot=False).get()
    assert 3 == chunk.size

    chunk_quality = chunk.quality
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkEvaluator)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk_quality <= chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkSelector)
    original_chunk_activation = chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk.update_activation()
    assert original_chunk_activation <= chunk.activation
    # END: build and enlarge a sameness chunk

    # START: label the sameness chunk
    parent_concept = bubble_chamber.concepts["cold"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": chunk, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not chunk.has_label_with_name("cold")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk.has_label_with_name("cold")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation

    parent_concept = bubble_chamber.concepts["northwest"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": chunk, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not chunk.has_label_with_name("northwest")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk.has_label_with_name("northwest")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation
    chunk_one = chunk
    # END: label the sameness chunk

    # START: make and label another sameness chunk
    target_node = input_space.contents.filter(
        lambda x: x.has_location_in_space(location_space)
        and x.location_in_space(location_space).coordinates == [[0, 4]]
    ).get()
    codelet = ChunkSuggester.spawn(
        "",
        bubble_chamber,
        {"target_space": input_space, "target_node": target_node, "target_rule": None},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkBuilder)
    assert target_node.super_chunks.is_empty()
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert not target_node.super_chunks.is_empty()

    chunk = codelet.child_structures.where(is_slot=False).get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkEvaluator)
    assert 0 == chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkSelector)
    original_chunk_activation = chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk.update_activation()
    assert original_chunk_activation < chunk.activation

    # suggest an enlargement to the second chunk
    codelet = [c for c in codelet.child_codelets if isinstance(c, ChunkSuggester)][0]
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk = codelet.child_structures.where(is_slot=False).get()
    assert 3 == chunk.size

    chunk_quality = chunk.quality
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkEvaluator)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk_quality <= chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkSelector)
    original_chunk_activation = chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk.update_activation()
    assert original_chunk_activation <= chunk.activation

    # label the second chunk with a temperature label
    parent_concept = bubble_chamber.concepts["cool"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": chunk, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not chunk.has_label_with_name("cool")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk.has_label_with_name("cool")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation

    # label the second chunk with a location label
    parent_concept = bubble_chamber.concepts["northeast"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": chunk, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not chunk.has_label_with_name("northeast")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk.has_label_with_name("northeast")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation
    chunk_two = chunk
    # END: make and label another sameness chunk

    # START: relate the two chunks in temperature as well as location space
    target_space = bubble_chamber.conceptual_spaces["temperature"]
    parent_concept = bubble_chamber.concepts["less"]
    codelet = RelationSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_space": target_space,
            "target_structure_one": chunk_one,
            "target_structure_two": chunk_two,
            "parent_concept": parent_concept,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationBuilder)
    assert not chunk_one.has_relation_with_name("less")
    assert not chunk_two.has_relation_with_name("less")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk_one.has_relation_with_name("less")
    assert chunk_two.has_relation_with_name("less")

    relation = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationEvaluator)
    assert 0 == relation.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < relation.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationSelector)
    original_relation_activation = relation.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    relation.update_activation()
    assert original_relation_activation < relation.activation

    codelet = [c for c in codelet.child_codelets if isinstance(c, RelationSuggester)][0]
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    codelet.target_space = bubble_chamber.conceptual_spaces["northwest-southeast"]
    assert isinstance(codelet, RelationBuilder)
    assert 1 == len(chunk_one.relations)
    assert 1 == len(chunk_two.relations)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 2 == len(chunk_one.relations)
    assert 2 == len(chunk_two.relations)

    relation = codelet.child_structures.get()
    assert (
        relation.conceptual_space
        == bubble_chamber.conceptual_spaces["northwest-southeast"]
    )
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationEvaluator)
    assert 0 == relation.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < relation.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationSelector)
    original_relation_activation = relation.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    relation.update_activation()
    assert original_relation_activation < relation.activation
    # END: relate the two chunks in temperature as well as location space

    # START: build comparative phrase
    frame = bubble_chamber.frames["np[nn]"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "location"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    np_view = view
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewEvaluator)
    assert 0 == view.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 == view.quality  # empty view has quality of 0
    assert len(view.input_spaces) == 1

    # build sameness correspondence between location labels
    target_label = chunk_one.labels_in_space(
        bubble_chamber.conceptual_spaces["location"]
    ).get()
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": target_label,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation
    assert len(view.input_spaces) == 1

    # build correspondence between chunks
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": chunk_one,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.get()
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert len(view.input_spaces) == 1
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # evaluate the simplex view now that correspondences have been added
    codelet = SimplexViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < view.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewSelector)
    original_view_activation = view.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view.update_activation()
    assert original_view_activation < view.activation

    # project a location noun from the frame to the output space
    letter_chunk_slot = view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # make a simplex view with a comparative phrase frame
    frame = bubble_chamber.frames["rp[jjr]"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "temperature"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    rp_view = view

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewEvaluator)
    assert 0 == view.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 == view.quality  # empty view has quality of 0

    # build a correspondence between the relations' temperature labels
    target_label = chunk_one.labels_in_space(
        bubble_chamber.conceptual_spaces["temperature"]
    ).get()
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": target_label,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # build a correspondence between the relations
    target_relation = chunk_one.relations_in_space(
        bubble_chamber.conceptual_spaces["temperature"]
    ).get()
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": target_relation,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # evaluate the view now that correspondences have been added to it
    codelet = SimplexViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < view.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewSelector)
    original_view_activation = view.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view.update_activation()
    assert original_view_activation < view.activation

    # try and fail to project jjr-ending slot into output
    # the root hasn't been filled in so ending cannot be decided
    letter_chunk_slot = view.parent_frame.output_space.contents.filter(
        lambda x: x.is_letter_chunk == True
        and x.is_slot == True
        and not x.super_chunks.is_empty()
        and x.labels.is_empty()
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FIZZLE == codelet.result

    # project jjr-root slot into output ("cold")
    letter_chunk_slot = view.parent_frame.output_space.contents.filter(
        lambda x: x.is_letter_chunk == True
        and x.is_slot == True
        and not x.super_chunks.is_empty()
        and not x.labels.is_empty()
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()
    assert letter_chunk.name == "cold"

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # project jjr-ending into output ("-er")
    letter_chunk_slot = view.parent_frame.output_space.contents.filter(
        lambda x: x.is_letter_chunk == True
        and x.is_slot == True
        and not x.super_chunks.is_empty()
        and x.labels.is_empty()
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()
    assert letter_chunk.name == "\ber"

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # project the jjr container chunk into output ("colder")
    letter_chunk_slot = view.parent_frame.output_space.contents.filter(
        lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()
    assert letter_chunk.name == "colder"

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # build a view with comparative sentence parent frame
    frame = bubble_chamber.frames["s-comparative"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "temperature"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    sentence_view = view

    # construct correspondence from rp-frame to sentence frame (relation)
    # codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    sub_view = rp_view
    codelet.target_structure_one = rp_view.parent_frame.input_space.contents.where(
        is_relation=True
    ).get()
    codelet.target_space_one = rp_view.parent_frame.input_space
    codelet.target_structure_two = view.parent_frame.input_space.contents.where(
        is_relation=True
    ).get()
    codelet.target_space_two = view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["more-less"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in rp_view.parent_frame.input_space.contents
        and x.end in view.parent_frame.input_space.contents
    ).get()
    relation_correspondence = correspondence

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from rp-frame to sentence frame (relation start label)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_structure_one = relation_correspondence.start.start.labels.filter(
        lambda x: bubble_chamber.conceptual_spaces["temperature"] in x.parent_spaces
    ).get()
    codelet.target_space_one = rp_view.parent_frame.input_space
    codelet.target_structure_two = relation_correspondence.end.start.labels.filter(
        lambda x: bubble_chamber.conceptual_spaces["temperature"] in x.parent_spaces
    ).get()
    codelet.target_space_two = view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["temperature"]
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from rp-frame to sentence frame (jjr label)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = rp_view.parent_frame.output_space
    codelet.target_structure_one = (
        codelet.target_space_one.contents.where(
            is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
        )
        .get()
        .labels.get()
    )
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = codelet.target_space_two.contents.where(
        is_label=True, parent_concept=bubble_chamber.concepts["jjr"]
    ).get()
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["grammar"]
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from rp-frame to sentence frame (letter chunk)
    # TODO: allow for a suggester's targets to be pre-specified
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = rp_view.parent_frame.output_space
    codelet.target_structure_one = codelet.target_space_one.contents.where(
        is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
    ).get()
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = (
        codelet.target_space_two.contents.where(
            is_label=True, parent_concept=bubble_chamber.concepts["jjr"]
        )
        .get()
        .start
    )
    codelet.target_conceptual_space = None
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from np-frame to sentence frame (label)
    # codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    sub_view = np_view
    codelet.target_structure_one = np_view.parent_frame.input_space.contents.where(
        is_label=True
    ).get()
    codelet.target_space_one = np_view.parent_frame.input_space
    codelet.target_structure_two = view.parent_frame.input_space.contents.filter(
        lambda x: x.is_label
        and not x.start.relations.filter(lambda y: y.start == x.start).is_empty()
        and x in bubble_chamber.conceptual_spaces["location"].contents
    ).get()
    codelet.sub_frame = view.parent_frame.sub_frames.filter(
        lambda x: codelet.target_structure_two in x.input_space.contents
    ).get()
    codelet.target_space_two = view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["location"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in np_view.parent_frame.input_space.contents
        and x.end in view.parent_frame.input_space.contents
    ).get()
    relation_correspondence = correspondence

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from np-frame to sentence frame (np label)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = np_view.parent_frame.output_space
    codelet.target_structure_one = (
        codelet.target_space_one.contents.where(
            is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
        )
        .get()
        .labels.filter(
            lambda x: x in bubble_chamber.conceptual_spaces["grammar"].contents
        )
        .get()
    )
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = codelet.target_space_two.contents.where(
        structure_id="Label63"
    ).get()
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["grammar"]
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from np-frame to sentence frame (letter_chunk)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = np_view.parent_frame.output_space
    codelet.target_structure_one = codelet.target_space_one.contents.where(
        is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
    ).get()
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = correspondence.end.start
    codelet.target_conceptual_space = None
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # no more views to fill sub view slots
    codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.run()
    assert CodeletResult.FIZZLE == codelet.result

    # construct another np view for the relation end
    frame = bubble_chamber.frames["np[nn]"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "location"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    np_view_2 = view
    assert len(view.input_spaces) == 1

    # build correspondence between location labels
    target_label = chunk_two.labels_in_space(
        bubble_chamber.conceptual_spaces["location"]
    ).get()
    assert target_label.parent_concept.name == "northeast"
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": np_view_2,
            "target_space_one": input_space,
            "target_structure_one": target_label,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation
    assert len(view.input_spaces) == 1

    # build correspondence between chunks
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": np_view_2,
            "target_space_one": input_space,
            "target_structure_one": chunk_two,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.get()
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert len(view.input_spaces) == 1
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # evaluate view now that correspondences have been added
    codelet = SimplexViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < view.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewSelector)
    original_view_activation = view.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view.update_activation()
    assert original_view_activation < view.activation

    # project a location noun from the frame to the output space
    letter_chunk_slot = view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # build correspondence from second np view and comparative sentence view (label)
    # codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": sentence_view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": sentence_view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    sub_view = np_view_2
    codelet.target_structure_one = np_view_2.parent_frame.input_space.contents.where(
        is_label=True
    ).get()
    codelet.target_space_one = np_view_2.parent_frame.input_space
    codelet.target_structure_two = (
        sentence_view.parent_frame.input_space.contents.filter(
            lambda x: x.is_label
            and not x.start.relations.filter(lambda y: y.end == x.start).is_empty()
            and x in bubble_chamber.conceptual_spaces["location"].contents
        ).get()
    )
    codelet.target_space_two = sentence_view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["location"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in np_view_2.parent_frame.input_space.contents
        and x.end in sentence_view.parent_frame.input_space.contents
    ).get()
    relation_correspondence = correspondence

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # build correspondence from second np view and comparative sentence view (np label)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": sentence_view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": sentence_view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = np_view_2.parent_frame.output_space
    codelet.target_structure_one = (
        codelet.target_space_one.contents.where(
            is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
        )
        .get()
        .labels.filter(
            lambda x: x in bubble_chamber.conceptual_spaces["grammar"].contents
        )
        .get()
    )
    codelet.target_space_two = sentence_view.parent_frame.output_space
    codelet.target_structure_two = codelet.target_space_two.contents.where(
        is_label=True,
        parent_concept=bubble_chamber.concepts["np"],
        correspondences=bubble_chamber.new_structure_collection(),
    ).get()
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["grammar"]
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from second np-frame to sentence frame (letter_chunk)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = np_view_2.parent_frame.output_space
    codelet.target_structure_one = codelet.target_space_one.contents.where(
        is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
    ).get()
    codelet.target_space_two = sentence_view.parent_frame.output_space
    codelet.target_structure_two = correspondence.end.start
    codelet.target_conceptual_space = None
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # project all of the letter chunks
    for letter_chunk in sentence_view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ):
        codelet = LetterChunkProjectionSuggester.spawn(
            "",
            bubble_chamber,
            {"target_view": sentence_view, "target_projectee": letter_chunk},
            1.0,
        )
        codelet.run()
        assert CodeletResult.FINISH == codelet.result

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionEvaluator)
        assert 0 == letter_chunk.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < letter_chunk.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionSelector)
        original_letter_chunk_activation = letter_chunk.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        letter_chunk.update_activation()
        assert original_letter_chunk_activation < letter_chunk.activation

    assert (
        sentence_view.output_space.contents.filter(
            lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
        )
        .get()
        .name
        == "temperatures will be colder in the northwest than in the northeast"
    )

    for label in sentence_view.parent_frame.output_space.contents.filter(
        lambda x: x.is_label
        and x.parent_concept
        in {
            bubble_chamber.concepts["sentence"],
            bubble_chamber.concepts["nsubj"],
            bubble_chamber.concepts["vb"],
            bubble_chamber.concepts["predicate"],
        }
    ):
        codelet = LabelProjectionSuggester.spawn(
            "",
            bubble_chamber,
            {"target_view": sentence_view, "target_projectee": label},
            1.0,
        )
        codelet.run()
        assert CodeletResult.FINISH == codelet.result

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LabelProjectionBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        label = codelet.child_structures.where(is_label=True).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LabelProjectionEvaluator)
        assert 0 == label.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < label.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LabelProjectionSelector)
        original_label_activation = label.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        label.update_activation()
        assert original_label_activation < label.activation

    sentence_1_view = sentence_view

    assert (
        "temperatures"
        == sentence_1_view.output_space.contents.where(
            is_label=True, parent_concept=bubble_chamber.concepts["nsubj"]
        )
        .get()
        .start.name
    )
    assert (
        "will be"
        == sentence_1_view.output_space.contents.where(
            is_label=True, parent_concept=bubble_chamber.concepts["vb"]
        )
        .get()
        .start.name
    )
    assert (
        "colder in the northwest than in the northeast"
        == sentence_1_view.output_space.contents.where(
            is_label=True, parent_concept=bubble_chamber.concepts["predicate"]
        )
        .get()
        .start.name
    )
    # END: build comparative phrase

    # START: chunk and describe more data
    # build a third sameness chunk
    target_node = input_space.contents.filter(
        lambda x: x.has_location_in_space(location_space)
        and x.location_in_space(location_space).coordinates == [[5, 0]]
    ).get()
    codelet = ChunkSuggester.spawn(
        "",
        bubble_chamber,
        {"target_space": input_space, "target_node": target_node, "target_rule": None},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkBuilder)
    assert target_node.super_chunks.is_empty()
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert not target_node.super_chunks.is_empty()

    chunk = codelet.child_structures.where(is_slot=False).get()
    chunk_three = chunk
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkEvaluator)
    assert 0 == chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkSelector)
    original_chunk_activation = chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk.update_activation()
    assert original_chunk_activation < chunk.activation

    codelet = [c for c in codelet.child_codelets if isinstance(c, ChunkSuggester)][0]
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk = codelet.child_structures.where(is_slot=False).get()
    assert 3 == chunk.size

    chunk_quality = chunk.quality
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkEvaluator)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk_quality <= chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkSelector)
    original_chunk_activation = chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk.update_activation()
    assert original_chunk_activation <= chunk.activation

    # label the third chunk "southwest"
    parent_concept = bubble_chamber.concepts["southwest"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": chunk, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not chunk.has_label_with_name("southwest")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk.has_label_with_name("southwest")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation

    # label the third chunk "high"
    parent_concept = bubble_chamber.concepts["high"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": chunk, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not chunk.has_label_with_name("high")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk.has_label_with_name("high")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation

    # build a fourth sameness chunk
    target_node = input_space.contents.filter(
        lambda x: x.has_location_in_space(location_space)
        and x.location_in_space(location_space).coordinates == [[5, 4]]
    ).get()
    codelet = ChunkSuggester.spawn(
        "",
        bubble_chamber,
        {"target_space": input_space, "target_node": target_node, "target_rule": None},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkBuilder)
    assert target_node.super_chunks.is_empty()
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert not target_node.super_chunks.is_empty()

    chunk = codelet.child_structures.where(is_slot=False).get()
    chunk_four = chunk
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkEvaluator)
    assert 0 == chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkSelector)
    original_chunk_activation = chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk.update_activation()
    assert original_chunk_activation < chunk.activation

    codelet = [c for c in codelet.child_codelets if isinstance(c, ChunkSuggester)][0]
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk = codelet.child_structures.where(is_slot=False).get()
    assert 3 == chunk.size

    chunk_quality = chunk.quality
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkEvaluator)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk_quality <= chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, ChunkSelector)
    original_chunk_activation = chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    chunk.update_activation()
    assert original_chunk_activation <= chunk.activation

    # label the fourth chunk "southeast"
    parent_concept = bubble_chamber.concepts["southeast"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": chunk, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not chunk.has_label_with_name("southeast")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk.has_label_with_name("southeast")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation

    # label the fourth chunk "high"
    parent_concept = bubble_chamber.concepts["high"]
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": chunk, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert not chunk.has_label_with_name("high")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk.has_label_with_name("high")

    label = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    original_label_activation = label.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    label.update_activation()
    assert original_label_activation < label.activation

    # relate the third and fourth chunks in height space
    target_space = bubble_chamber.conceptual_spaces["height"]
    parent_concept = bubble_chamber.concepts["more"]
    codelet = RelationSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_space": target_space,
            "target_structure_one": chunk_four,
            "target_structure_two": chunk_three,
            "parent_concept": parent_concept,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationBuilder)
    assert not chunk_three.has_relation_with_name("more")
    assert not chunk_four.has_relation_with_name("more")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk_three.has_relation_with_name("more")
    assert chunk_four.has_relation_with_name("more")

    relation = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationEvaluator)
    assert 0 == relation.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < relation.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationSelector)
    original_relation_activation = relation.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    relation.update_activation()
    assert original_relation_activation < relation.activation

    # build a noun phrase for location
    frame = bubble_chamber.frames["np[nn]"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "location"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    np_view = view
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewEvaluator)
    assert 0 == view.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 == view.quality  # empty view has quality of 0
    assert len(view.input_spaces) == 1

    # build sameness correspondence between location labels
    target_label = chunk_three.labels_in_space(
        bubble_chamber.conceptual_spaces["location"]
    ).get()
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": target_label,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation
    assert len(view.input_spaces) == 1

    # build correspondence between chunks
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": chunk_three,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.get()
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert len(view.input_spaces) == 1
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # evaluate the simplex view now that correspondences have been added
    codelet = SimplexViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < view.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewSelector)
    original_view_activation = view.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view.update_activation()
    assert original_view_activation < view.activation

    # project a location noun from the frame to the output space
    letter_chunk_slot = view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # make a simplex view with a comparative phrase frame
    frame = bubble_chamber.frames["rp[jjr]"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "height"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    rp_view = view

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewEvaluator)
    assert 0 == view.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 == view.quality  # empty view has quality of 0

    # build a correspondence between the relations' height labels
    target_label = chunk_four.labels_in_space(
        bubble_chamber.conceptual_spaces["height"]
    ).get()
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": target_label,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # build a correspondence between the relations
    target_relation = chunk_three.relations_in_space(
        bubble_chamber.conceptual_spaces["height"]
    ).get()
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": input_space,
            "target_structure_one": target_relation,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # evaluate the view now that correspondences have been added to it
    codelet = SimplexViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < view.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewSelector)
    original_view_activation = view.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view.update_activation()
    assert original_view_activation < view.activation

    # try and fail to project jjr-ending slot into output
    # the root hasn't been filled in so ending cannot be decided
    letter_chunk_slot = view.parent_frame.output_space.contents.filter(
        lambda x: x.is_letter_chunk == True
        and x.is_slot == True
        and not x.super_chunks.is_empty()
        and x.labels.is_empty()
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FIZZLE == codelet.result

    # project jjr-root slot into output ("high")
    letter_chunk_slot = view.parent_frame.output_space.contents.filter(
        lambda x: x.is_letter_chunk == True
        and x.is_slot == True
        and not x.super_chunks.is_empty()
        and not x.labels.is_empty()
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()
    assert letter_chunk.name == "high"

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # project jjr-ending into output ("-er")
    letter_chunk_slot = view.parent_frame.output_space.contents.filter(
        lambda x: x.is_letter_chunk == True
        and x.is_slot == True
        and not x.super_chunks.is_empty()
        and x.labels.is_empty()
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()
    assert letter_chunk.name == "\ber"

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # project the jjr container chunk into output ("higher")
    letter_chunk_slot = view.parent_frame.output_space.contents.filter(
        lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()
    assert letter_chunk.name == "higher"

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # build a view with comparative sentence parent frame
    frame = bubble_chamber.frames["s-comparative"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "height"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    sentence_view = view

    # construct correspondence from rp-frame to sentence frame (relation)
    # codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    sub_view = rp_view
    codelet.target_structure_one = rp_view.parent_frame.input_space.contents.where(
        is_relation=True
    ).get()
    codelet.target_space_one = rp_view.parent_frame.input_space
    codelet.target_structure_two = view.parent_frame.input_space.contents.where(
        is_relation=True
    ).get()
    codelet.target_space_two = view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["more-less"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in rp_view.parent_frame.input_space.contents
        and x.end in view.parent_frame.input_space.contents
    ).get()
    relation_correspondence = correspondence

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from rp-frame to sentence frame (relation start label)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_structure_one = relation_correspondence.start.start.labels.filter(
        lambda x: bubble_chamber.conceptual_spaces["height"] in x.parent_spaces
    ).get()
    codelet.target_space_one = rp_view.parent_frame.input_space
    codelet.target_structure_two = relation_correspondence.end.start.labels.filter(
        lambda x: bubble_chamber.conceptual_spaces["height"] in x.parent_spaces
    ).get()
    codelet.target_space_two = view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["height"]
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from rp-frame to sentence frame (jjr label)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = rp_view.parent_frame.output_space
    codelet.target_structure_one = (
        codelet.target_space_one.contents.where(
            is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
        )
        .get()
        .labels.get()
    )
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = codelet.target_space_two.contents.where(
        is_label=True, parent_concept=bubble_chamber.concepts["jjr"]
    ).get()
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["grammar"]
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from rp-frame to sentence frame (letter chunk)
    # TODO: allow for a suggester's targets to be pre-specified
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = rp_view.parent_frame.output_space
    codelet.target_structure_one = codelet.target_space_one.contents.where(
        is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
    ).get()
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = (
        codelet.target_space_two.contents.where(
            is_label=True, parent_concept=bubble_chamber.concepts["jjr"]
        )
        .get()
        .start
    )
    codelet.target_conceptual_space = None
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from np-frame to sentence frame (label)
    # codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    sub_view = np_view
    codelet.target_structure_one = np_view.parent_frame.input_space.contents.where(
        is_label=True
    ).get()
    codelet.target_space_one = np_view.parent_frame.input_space
    codelet.target_structure_two = view.parent_frame.input_space.contents.filter(
        lambda x: x.is_label
        and not x.start.relations.filter(lambda y: y.start == x.start).is_empty()
        and x in bubble_chamber.conceptual_spaces["location"].contents
    ).get()
    codelet.sub_frame = view.parent_frame.sub_frames.filter(
        lambda x: codelet.target_structure_two in x.input_space.contents
    ).get()
    codelet.target_space_two = view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["location"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in np_view.parent_frame.input_space.contents
        and x.end in view.parent_frame.input_space.contents
    ).get()
    relation_correspondence = correspondence

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from np-frame to sentence frame (np label)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = np_view.parent_frame.output_space
    codelet.target_structure_one = (
        codelet.target_space_one.contents.where(
            is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
        )
        .get()
        .labels.filter(
            lambda x: x in bubble_chamber.conceptual_spaces["grammar"].contents
        )
        .get()
    )
    codelet.target_space_two = view.parent_frame.output_space

    codelet.target_structure_two = codelet.target_space_two.contents.where(
        structure_id="Label92"
    ).get()
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["grammar"]
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from np-frame to sentence frame (letter_chunk)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = np_view.parent_frame.output_space
    codelet.target_structure_one = codelet.target_space_one.contents.where(
        is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
    ).get()
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = correspondence.end.start
    codelet.target_conceptual_space = None
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # no more views to fill sub view slots
    codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.run()
    assert CodeletResult.FIZZLE == codelet.result

    # construct another np view for the relation end
    frame = bubble_chamber.frames["np[nn]"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "location"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    np_view_2 = view
    assert len(view.input_spaces) == 1

    # build correspondence between location labels
    target_label = chunk_four.labels_in_space(
        bubble_chamber.conceptual_spaces["location"]
    ).get()
    assert target_label.parent_concept.name == "southeast"
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": np_view_2,
            "target_space_one": input_space,
            "target_structure_one": target_label,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation
    assert len(view.input_spaces) == 1

    # build correspondence between chunks
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": np_view_2,
            "target_space_one": input_space,
            "target_structure_one": chunk_four,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.get()
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert len(view.input_spaces) == 1
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # evaluate view now that correspondences have been added
    codelet = SimplexViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < view.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewSelector)
    original_view_activation = view.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view.update_activation()
    assert original_view_activation < view.activation

    # project a location noun from the frame to the output space
    letter_chunk_slot = view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # build correspondence from second np view and comparative sentence view (label)
    # codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": sentence_view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": sentence_view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    sub_view = np_view_2
    codelet.target_structure_one = np_view_2.parent_frame.input_space.contents.where(
        is_label=True
    ).get()
    codelet.target_space_one = np_view_2.parent_frame.input_space
    codelet.target_structure_two = (
        sentence_view.parent_frame.input_space.contents.filter(
            lambda x: x.is_label
            and not x.start.relations.filter(lambda y: y.end == x.start).is_empty()
            and x in bubble_chamber.conceptual_spaces["location"].contents
        ).get()
    )
    codelet.target_space_two = sentence_view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["location"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in np_view_2.parent_frame.input_space.contents
        and x.end in sentence_view.parent_frame.input_space.contents
    ).get()
    relation_correspondence = correspondence

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # build correspondence from second np view and comparative sentence view (np label)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": sentence_view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": sentence_view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = np_view_2.parent_frame.output_space
    codelet.target_structure_one = (
        codelet.target_space_one.contents.where(
            is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
        )
        .get()
        .labels.filter(
            lambda x: x in bubble_chamber.conceptual_spaces["grammar"].contents
        )
        .get()
    )
    codelet.target_space_two = sentence_view.parent_frame.output_space
    codelet.target_structure_two = codelet.target_space_two.contents.where(
        is_label=True,
        parent_concept=bubble_chamber.concepts["np"],
        correspondences=bubble_chamber.new_structure_collection(),
    ).get()
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["grammar"]
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # construct correspondence from second np-frame to sentence frame (letter_chunk)
    # codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = np_view_2.parent_frame.output_space
    codelet.target_structure_one = codelet.target_space_one.contents.where(
        is_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
    ).get()
    codelet.target_space_two = sentence_view.parent_frame.output_space
    codelet.target_structure_two = correspondence.end.start
    codelet.target_conceptual_space = None
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # project all of the letter chunks
    for letter_chunk in sentence_view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ):
        codelet = LetterChunkProjectionSuggester.spawn(
            "",
            bubble_chamber,
            {"target_view": sentence_view, "target_projectee": letter_chunk},
            1.0,
        )
        codelet.run()
        assert CodeletResult.FINISH == codelet.result

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionEvaluator)
        assert 0 == letter_chunk.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < letter_chunk.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionSelector)
        original_letter_chunk_activation = letter_chunk.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        letter_chunk.update_activation()
        assert original_letter_chunk_activation < letter_chunk.activation

    assert (
        sentence_view.output_space.contents.filter(
            lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
        )
        .get()
        .name
        == "temperatures will be higher in the southeast than in the southwest"
    )
    sentence_2_view = sentence_view
    for label in sentence_view.parent_frame.output_space.contents.filter(
        lambda x: x.is_label
        and x.parent_concept
        in {
            bubble_chamber.concepts["sentence"],
            bubble_chamber.concepts["nsubj"],
            bubble_chamber.concepts["vb"],
            bubble_chamber.concepts["predicate"],
        }
    ):
        codelet = LabelProjectionSuggester.spawn(
            "",
            bubble_chamber,
            {"target_view": sentence_view, "target_projectee": label},
            1.0,
        )
        codelet.run()
        assert CodeletResult.FINISH == codelet.result

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LabelProjectionBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        label = codelet.child_structures.where(is_label=True).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LabelProjectionEvaluator)
        assert 0 == label.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < label.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LabelProjectionSelector)
        original_label_activation = label.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        label.update_activation()
        assert original_label_activation < label.activation

    sentence_2_view = sentence_view

    assert (
        "temperatures"
        == sentence_2_view.output_space.contents.where(
            is_label=True, parent_concept=bubble_chamber.concepts["nsubj"]
        )
        .get()
        .start.name
    )
    assert (
        "will be"
        == sentence_2_view.output_space.contents.where(
            is_label=True, parent_concept=bubble_chamber.concepts["vb"]
        )
        .get()
        .start.name
    )
    assert (
        "higher in the southeast than in the southwest"
        == sentence_2_view.output_space.contents.where(
            is_label=True, parent_concept=bubble_chamber.concepts["predicate"]
        )
        .get()
        .start.name
    )
    # END: chunk and describe more data

    # START: compile longer piece of text
    frame = bubble_chamber.frames["s-and"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    and_sentence_view = view

    sentence_1_space = sentence_1_view.output_space
    sentence_1_sentence_chunk = sentence_1_space.contents.filter(
        lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
    ).get()
    sentence_1_sentence_label = sentence_1_sentence_chunk.labels.get()
    sentence_1_nsubj_chunk = sentence_1_sentence_chunk.left_branch.get()
    sentence_1_nsubj_label = sentence_1_nsubj_chunk.labels.get()
    sentence_1_vp_chunk = sentence_1_sentence_chunk.right_branch.get()
    sentence_1_vb_chunk = sentence_1_vp_chunk.left_branch.get()
    sentence_1_vb_label = sentence_1_vb_chunk.labels.get()
    sentence_1_pred_chunk = sentence_1_vp_chunk.right_branch.get()
    sentence_1_pred_label = sentence_1_pred_chunk.labels.get()

    sentence_2_space = sentence_2_view.output_space
    sentence_2_sentence_chunk = sentence_2_space.contents.filter(
        lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
    ).get()
    sentence_2_sentence_label = sentence_2_sentence_chunk.labels.get()
    sentence_2_nsubj_chunk = sentence_2_sentence_chunk.left_branch.get()
    sentence_2_nsubj_label = sentence_2_nsubj_chunk.labels.get()
    sentence_2_vp_chunk = sentence_2_sentence_chunk.right_branch.get()
    sentence_2_vb_chunk = sentence_2_vp_chunk.left_branch.get()
    sentence_2_vb_label = sentence_2_vb_chunk.labels.get()
    sentence_2_pred_chunk = sentence_2_vp_chunk.right_branch.get()
    sentence_2_pred_label = sentence_2_pred_chunk.labels.get()

    and_frame_output_space = and_sentence_view.parent_frame.output_space
    and_sentence_sentence_chunk = and_frame_output_space.contents.filter(
        lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
    ).get()
    and_sentence_clause_1_chunk = and_sentence_sentence_chunk.left_branch.get()
    and_sentence_clause_1_label = and_sentence_clause_1_chunk.labels.get()
    and_sentence_clause_1_nsubj_chunk = and_sentence_clause_1_chunk.left_branch.get()
    and_sentence_clause_1_nsubj_label = and_sentence_clause_1_nsubj_chunk.labels.get()
    and_sentence_clause_1_vp_chunk = and_sentence_clause_1_chunk.right_branch.get()
    and_sentence_clause_1_vb_chunk = and_sentence_clause_1_vp_chunk.left_branch.get()
    and_sentence_clause_1_vb_label = and_sentence_clause_1_vb_chunk.labels.get()
    and_sentence_clause_1_pred_chunk = and_sentence_clause_1_vp_chunk.right_branch.get()
    and_sentence_clause_1_pred_label = and_sentence_clause_1_pred_chunk.labels.get()
    and_sentence_conj_chunk = and_sentence_sentence_chunk.right_branch.get()
    and_sentence_and_chunk = and_sentence_conj_chunk.left_branch.get()
    and_sentence_clause_2_chunk = and_sentence_conj_chunk.right_branch.get()
    and_sentence_clause_2_label = and_sentence_clause_2_chunk.labels.get()
    and_sentence_clause_2_nsubj_chunk = and_sentence_clause_2_chunk.left_branch.get()
    and_sentence_clause_2_nsubj_label = and_sentence_clause_2_nsubj_chunk.labels.get()
    and_sentence_clause_2_vp_chunk = and_sentence_clause_2_chunk.right_branch.get()
    and_sentence_clause_2_vb_chunk = and_sentence_clause_2_vp_chunk.left_branch.get()
    and_sentence_clause_2_vb_label = and_sentence_clause_2_vb_chunk.labels.get()
    and_sentence_clause_2_pred_chunk = and_sentence_clause_2_vp_chunk.right_branch.get()
    and_sentence_clause_2_pred_label = and_sentence_clause_2_pred_chunk.labels.get()

    # construct correspondence from sentence_1_frame to and-sentence frame (sentence label)
    # codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "",
        bubble_chamber,
        {"target_view": view},
        1.0,
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = sentence_1_space
    codelet.target_structure_one = sentence_1_sentence_label
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = and_sentence_clause_1_label
    codelet.target_conceptual_space = bubble_chamber.spaces["grammar"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in sentence_1_space.contents
        and x.end in view.parent_frame.output_space.contents
    ).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "",
        bubble_chamber,
        {"target_view": view},
        1.0,
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = sentence_2_space
    codelet.target_structure_one = sentence_2_sentence_label
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = and_sentence_clause_2_label
    codelet.target_conceptual_space = bubble_chamber.spaces["grammar"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in sentence_2_space.contents
        and x.end in view.parent_frame.output_space.contents
    ).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    for structure_1, structure_2 in zip(
        [
            sentence_1_nsubj_label,
            sentence_1_vb_label,
            sentence_1_pred_label,
            sentence_1_sentence_chunk,
            sentence_1_nsubj_chunk,
            sentence_1_vb_chunk,
            sentence_1_pred_chunk,
            sentence_1_vp_chunk,
        ],
        [
            and_sentence_clause_1_nsubj_label,
            and_sentence_clause_1_vb_label,
            and_sentence_clause_1_pred_label,
            and_sentence_clause_1_chunk,
            and_sentence_clause_1_nsubj_chunk,
            and_sentence_clause_1_vb_chunk,
            and_sentence_clause_1_pred_chunk,
            and_sentence_clause_1_vp_chunk,
        ],
    ):
        codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
            "",
            bubble_chamber,
            {"target_view": view},
            1.0,
        )
        codelet.parent_concept = bubble_chamber.concepts["same"]
        codelet.target_space_one = sentence_1_space
        codelet.target_structure_one = structure_1
        codelet.target_space_two = view.parent_frame.output_space
        codelet.target_structure_two = structure_2
        codelet.target_conceptual_space = (
            bubble_chamber.spaces["grammar"] if structure_1.is_label else None
        )
        assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        correspondence = codelet.child_structures.filter(
            lambda x: x.is_correspondence
            and x.start in sentence_1_space.contents
            and x.end in view.parent_frame.output_space.contents
        ).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, CorrespondenceEvaluator)
        assert 0 == correspondence.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < correspondence.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, CorrespondenceSelector)
        original_correspondence_activation = correspondence.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        correspondence.update_activation()
        assert original_correspondence_activation < correspondence.activation

    for structure_1, structure_2 in zip(
        [
            sentence_2_nsubj_label,
            sentence_2_vb_label,
            sentence_2_pred_label,
            sentence_2_sentence_chunk,
            sentence_2_nsubj_chunk,
            sentence_2_vb_chunk,
            sentence_2_pred_chunk,
            sentence_2_vp_chunk,
        ],
        [
            and_sentence_clause_2_nsubj_label,
            and_sentence_clause_2_vb_label,
            and_sentence_clause_2_pred_label,
            and_sentence_clause_2_chunk,
            and_sentence_clause_2_nsubj_chunk,
            and_sentence_clause_2_vb_chunk,
            and_sentence_clause_2_pred_chunk,
            and_sentence_clause_2_vp_chunk,
        ],
    ):
        codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
            "",
            bubble_chamber,
            {"target_view": view},
            1.0,
        )
        codelet.parent_concept = bubble_chamber.concepts["same"]
        codelet.target_space_one = sentence_2_space
        codelet.target_structure_one = structure_1
        codelet.target_space_two = view.parent_frame.output_space
        codelet.target_structure_two = structure_2
        codelet.target_conceptual_space = (
            bubble_chamber.spaces["grammar"] if structure_1.is_label else None
        )
        assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        correspondence = codelet.child_structures.filter(
            lambda x: x.is_correspondence
            and x.start in sentence_2_space.contents
            and x.end in view.parent_frame.output_space.contents
        ).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, CorrespondenceEvaluator)
        assert 0 == correspondence.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < correspondence.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, CorrespondenceSelector)
        original_correspondence_activation = correspondence.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        correspondence.update_activation()
        assert original_correspondence_activation < correspondence.activation

    # project all of the letter chunks
    for letter_chunk in and_sentence_view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ):
        codelet = LetterChunkProjectionSuggester.spawn(
            "",
            bubble_chamber,
            {"target_view": and_sentence_view, "target_projectee": letter_chunk},
            1.0,
        )
        codelet.run()
        assert CodeletResult.FINISH == codelet.result

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionEvaluator)
        assert 0 == letter_chunk.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < letter_chunk.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionSelector)
        original_letter_chunk_activation = letter_chunk.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        letter_chunk.update_activation()
        assert original_letter_chunk_activation < letter_chunk.activation

    result = (
        and_sentence_view.output_space.contents.filter(
            lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
        )
        .get()
        .name
    )
    assert (
        result
        == "temperatures will be colder in the northwest than in the northeast and higher in the southeast than in the southwest"
    )
    # END: compile longer piece of text

    # START: compile alternative longer piece of text using "but"
    frame = bubble_chamber.frames["s-but"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    but_sentence_view = view

    sentence_1_space = sentence_1_view.output_space
    sentence_1_sentence_chunk = sentence_1_space.contents.filter(
        lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
    ).get()
    sentence_1_sentence_label = sentence_1_sentence_chunk.labels.get()
    sentence_1_nsubj_chunk = sentence_1_sentence_chunk.left_branch.get()
    sentence_1_nsubj_label = sentence_1_nsubj_chunk.labels.get()
    sentence_1_vp_chunk = sentence_1_sentence_chunk.right_branch.get()
    sentence_1_vb_chunk = sentence_1_vp_chunk.left_branch.get()
    sentence_1_vb_label = sentence_1_vb_chunk.labels.get()
    sentence_1_pred_chunk = sentence_1_vp_chunk.right_branch.get()
    sentence_1_pred_label = sentence_1_pred_chunk.labels.get()

    sentence_2_space = sentence_2_view.output_space
    sentence_2_sentence_chunk = sentence_2_space.contents.filter(
        lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
    ).get()
    sentence_2_sentence_label = sentence_2_sentence_chunk.labels.get()
    sentence_2_nsubj_chunk = sentence_2_sentence_chunk.left_branch.get()
    sentence_2_nsubj_label = sentence_2_nsubj_chunk.labels.get()
    sentence_2_vp_chunk = sentence_2_sentence_chunk.right_branch.get()
    sentence_2_vb_chunk = sentence_2_vp_chunk.left_branch.get()
    sentence_2_vb_label = sentence_2_vb_chunk.labels.get()
    sentence_2_pred_chunk = sentence_2_vp_chunk.right_branch.get()
    sentence_2_pred_label = sentence_2_pred_chunk.labels.get()

    but_frame_output_space = but_sentence_view.parent_frame.output_space
    but_sentence_sentence_chunk = but_frame_output_space.contents.filter(
        lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
    ).get()
    but_sentence_clause_1_chunk = but_sentence_sentence_chunk.left_branch.get()
    but_sentence_clause_1_label = but_sentence_clause_1_chunk.labels.get()
    but_sentence_clause_1_nsubj_chunk = but_sentence_clause_1_chunk.left_branch.get()
    but_sentence_clause_1_nsubj_label = but_sentence_clause_1_nsubj_chunk.labels.get()
    but_sentence_clause_1_vp_chunk = but_sentence_clause_1_chunk.right_branch.get()
    but_sentence_clause_1_vb_chunk = but_sentence_clause_1_vp_chunk.left_branch.get()
    but_sentence_clause_1_vb_label = but_sentence_clause_1_vb_chunk.labels.get()
    but_sentence_clause_1_pred_chunk = but_sentence_clause_1_vp_chunk.right_branch.get()
    but_sentence_clause_1_pred_label = but_sentence_clause_1_pred_chunk.labels.get()
    but_sentence_conj_chunk = but_sentence_sentence_chunk.right_branch.get()
    but_sentence_but_chunk = but_sentence_conj_chunk.left_branch.get()
    but_sentence_clause_2_chunk = but_sentence_conj_chunk.right_branch.get()
    but_sentence_clause_2_label = but_sentence_clause_2_chunk.labels.get()
    but_sentence_clause_2_nsubj_chunk = but_sentence_clause_2_chunk.left_branch.get()
    but_sentence_clause_2_nsubj_label = but_sentence_clause_2_nsubj_chunk.labels.get()
    but_sentence_clause_2_vp_chunk = but_sentence_clause_2_chunk.right_branch.get()
    but_sentence_clause_2_vb_chunk = but_sentence_clause_2_vp_chunk.left_branch.get()
    but_sentence_clause_2_vb_label = but_sentence_clause_2_vb_chunk.labels.get()
    but_sentence_clause_2_pred_chunk = but_sentence_clause_2_vp_chunk.right_branch.get()
    but_sentence_clause_2_pred_label = but_sentence_clause_2_pred_chunk.labels.get()

    # construct correspondence from sentence_1_frame to but-sentence frame (sentence label)
    # codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
    #    "", bubble_chamber, {"target_view": view}, 1.0
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "",
        bubble_chamber,
        {"target_view": view},
        1.0,
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = sentence_1_space
    codelet.target_structure_one = sentence_1_sentence_label
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = but_sentence_clause_1_label
    codelet.target_conceptual_space = bubble_chamber.spaces["grammar"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in sentence_1_space.contents
        and x.end in view.parent_frame.output_space.contents
    ).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "",
        bubble_chamber,
        {"target_view": view},
        1.0,
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = sentence_2_space
    codelet.target_structure_one = sentence_2_sentence_label
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = but_sentence_clause_2_label
    codelet.target_conceptual_space = bubble_chamber.spaces["grammar"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in sentence_2_space.contents
        and x.end in view.parent_frame.output_space.contents
    ).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    for structure_1, structure_2 in zip(
        [
            sentence_1_nsubj_label,
            sentence_1_vb_label,
            sentence_1_pred_label,
            sentence_1_sentence_chunk,
            sentence_1_nsubj_chunk,
            sentence_1_vb_chunk,
            sentence_1_pred_chunk,
            sentence_1_vp_chunk,
        ],
        [
            but_sentence_clause_1_nsubj_label,
            but_sentence_clause_1_vb_label,
            but_sentence_clause_1_pred_label,
            but_sentence_clause_1_chunk,
            but_sentence_clause_1_nsubj_chunk,
            but_sentence_clause_1_vb_chunk,
            but_sentence_clause_1_pred_chunk,
            but_sentence_clause_1_vp_chunk,
        ],
    ):
        codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
            "",
            bubble_chamber,
            {"target_view": view},
            1.0,
        )
        codelet.parent_concept = bubble_chamber.concepts["same"]
        codelet.target_space_one = sentence_1_space
        codelet.target_structure_one = structure_1
        codelet.target_space_two = view.parent_frame.output_space
        codelet.target_structure_two = structure_2
        codelet.target_conceptual_space = (
            bubble_chamber.spaces["grammar"] if structure_1.is_label else None
        )
        assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        correspondence = codelet.child_structures.filter(
            lambda x: x.is_correspondence
            and x.start in sentence_1_space.contents
            and x.end in view.parent_frame.output_space.contents
        ).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, CorrespondenceEvaluator)
        assert 0 == correspondence.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < correspondence.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, CorrespondenceSelector)
        original_correspondence_activation = correspondence.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        correspondence.update_activation()
        assert original_correspondence_activation < correspondence.activation

    for structure_1, structure_2 in zip(
        [
            sentence_2_nsubj_label,
            sentence_2_vb_label,
            sentence_2_pred_label,
            sentence_2_sentence_chunk,
            sentence_2_nsubj_chunk,
            sentence_2_vb_chunk,
            sentence_2_pred_chunk,
            sentence_2_vp_chunk,
        ],
        [
            but_sentence_clause_2_nsubj_label,
            but_sentence_clause_2_vb_label,
            but_sentence_clause_2_pred_label,
            but_sentence_clause_2_chunk,
            but_sentence_clause_2_nsubj_chunk,
            but_sentence_clause_2_vb_chunk,
            but_sentence_clause_2_pred_chunk,
            but_sentence_clause_2_vp_chunk,
        ],
    ):
        codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
            "",
            bubble_chamber,
            {"target_view": view},
            1.0,
        )
        codelet.parent_concept = bubble_chamber.concepts["same"]
        codelet.target_space_one = sentence_2_space
        codelet.target_structure_one = structure_1
        codelet.target_space_two = view.parent_frame.output_space
        codelet.target_structure_two = structure_2
        codelet.target_conceptual_space = (
            bubble_chamber.spaces["grammar"] if structure_1.is_label else None
        )
        assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        correspondence = codelet.child_structures.filter(
            lambda x: x.is_correspondence
            and x.start in sentence_2_space.contents
            and x.end in view.parent_frame.output_space.contents
        ).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, CorrespondenceEvaluator)
        assert 0 == correspondence.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < correspondence.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, CorrespondenceSelector)
        original_correspondence_activation = correspondence.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        correspondence.update_activation()
        assert original_correspondence_activation < correspondence.activation

    # project all of the letter chunks
    for letter_chunk in but_sentence_view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ):
        codelet = LetterChunkProjectionSuggester.spawn(
            "",
            bubble_chamber,
            {"target_view": but_sentence_view, "target_projectee": letter_chunk},
            1.0,
        )
        codelet.run()
        assert CodeletResult.FINISH == codelet.result

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionBuilder)
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionEvaluator)
        assert 0 == letter_chunk.quality
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        assert 0 < letter_chunk.quality

        codelet = codelet.child_codelets[0]
        assert isinstance(codelet, LetterChunkProjectionSelector)
        original_letter_chunk_activation = letter_chunk.activation
        codelet.run()
        assert CodeletResult.FINISH == codelet.result
        letter_chunk.update_activation()
        assert original_letter_chunk_activation < letter_chunk.activation

    result = (
        but_sentence_view.output_space.contents.filter(
            lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
        )
        .get()
        .name
    )
    assert (
        result
        == "temperatures will be colder in the northwest than in the northeast but higher in the southeast than in the southwest"
    )
    # END: compile longer piece of text

    # START: compare quality of "and" and "but" views
    codelet = SimplexViewEvaluator.spawn(
        "",
        bubble_chamber,
        bubble_chamber.new_structure_collection(and_sentence_view),
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < and_sentence_view.quality

    codelet = SimplexViewEvaluator.spawn(
        "",
        bubble_chamber,
        bubble_chamber.new_structure_collection(but_sentence_view),
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < but_sentence_view.quality

    # "but" view lacks correspondences to difference relations
    assert but_sentence_view.quality < and_sentence_view.quality

    # build differentness relation between chunks from each clause
    target_space = bubble_chamber.conceptual_spaces["temperature"]
    parent_concept = bubble_chamber.concepts["different"]
    codelet = RelationSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_space": target_space,
            "target_structure_one": chunk_one,
            "target_structure_two": chunk_three,
            "parent_concept": parent_concept,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationBuilder)
    assert not chunk_one.has_relation_with_name("different")
    assert not chunk_three.has_relation_with_name("different")
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert chunk_one.has_relation_with_name("different")
    assert chunk_three.has_relation_with_name("different")

    relation = codelet.child_structures.get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationEvaluator)
    assert 0 == relation.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < relation.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, RelationSelector)
    original_relation_activation = relation.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    relation.update_activation()
    assert original_relation_activation < relation.activation

    # build correspondence from differentness relation
    # to differentness relation in "but" frame
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": but_sentence_view,
            "target_space_one": input_space,
            "target_structure_one": relation,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    but_sentence_view_previous_quality = but_sentence_view.quality
    # re-evaluate "but" sentence view
    codelet = SimplexViewEvaluator.spawn(
        "",
        bubble_chamber,
        bubble_chamber.new_structure_collection(but_sentence_view),
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < but_sentence_view.quality

    assert but_sentence_view.quality > but_sentence_view_previous_quality
    # END: compare quality of "and" and "but" views

    # START: make a sentence with "very"
    parent_concept = bubble_chamber.concepts["very"]
    target = chunk_one.labels_in_space(
        bubble_chamber.conceptual_spaces["temperature"]
    ).get()
    codelet = LabelSuggester.spawn(
        "",
        bubble_chamber,
        {"target_node": target, "parent_concept": parent_concept},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelBuilder)
    assert 1 == len(
        chunk_one.labels_in_space(bubble_chamber.conceptual_spaces["temperature"])
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 2 == len(
        chunk_one.labels_in_space(bubble_chamber.conceptual_spaces["temperature"])
    )

    label = codelet.child_structures.filter(
        lambda x: x not in bubble_chamber.conceptual_spaces["temperature"].contents
    ).get()
    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelEvaluator)
    assert 0 == label.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < label.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LabelSelector)
    label_original_activation = label.activation
    target_original_activation = target.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    # build simple adectival phrase view
    frame = bubble_chamber.frames["ap[jj]"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "temperature"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    jj_view = view
    assert len(view.input_spaces) == 1

    # build sameness correspondence between temperature labels
    target_label = chunk_one.labels.filter(
        lambda x: x in bubble_chamber.conceptual_spaces["temperature"].contents
        and not x.labels.is_empty()
    ).get()
    codelet = SpaceToFrameCorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": jj_view,
            "target_space_one": input_space,
            "target_structure_one": target_label,
        },
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert len(jj_view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()
    assert len(jj_view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation
    assert len(view.input_spaces) == 1

    # project adjective into outupt space
    letter_chunk_slot = view.parent_frame.output_space.contents.where(
        is_letter_chunk=True
    ).get()
    codelet = LetterChunkProjectionSuggester.spawn(
        "",
        bubble_chamber,
        {"target_view": view, "target_projectee": letter_chunk_slot},
        1.0,
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk = codelet.child_structures.where(is_letter_chunk=True).get()
    assert "cold" == view.output_space.contents.where(is_letter_chunk=True).get().name

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionEvaluator)
    assert 0 == letter_chunk.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < letter_chunk.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, LetterChunkProjectionSelector)
    original_letter_chunk_activation = letter_chunk.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    letter_chunk.update_activation()
    assert original_letter_chunk_activation < letter_chunk.activation

    # build compound adectival phrase view
    frame = bubble_chamber.frames["ap-frame"]
    codelet = SimplexViewSuggester.spawn(
        "", bubble_chamber, {"frame": frame, "contextual_space": input_space}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    slot_space = codelet.frame.input_space.conceptual_spaces.where(is_slot=True).get()
    codelet.conceptual_spaces_map[slot_space] = bubble_chamber.conceptual_spaces[
        "temperature"
    ]
    assert isinstance(codelet, SimplexViewBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    view = codelet.child_structures.get()
    ap_view = view
    assert len(view.input_spaces) == 1

    # build correspondence from ap sub-frame label to ap frame label
    from homer.tools import print_out

    codelet = PotentialSubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    sub_view = jj_view
    codelet.target_structure_one = jj_view.parent_frame.input_space.contents.where(
        is_label=True
    ).get()
    print_out(codelet.target_structure_one)
    codelet.target_space_one = jj_view.parent_frame.input_space
    print_out(ap_view.parent_frame.input_space)
    print_out(ap_view.parent_frame.input_space.contents)
    codelet.target_structure_two = ap_view.parent_frame.input_space.contents.filter(
        lambda x: x.is_label
        and x.has_location_in_space(bubble_chamber.conceptual_spaces["temperature"])
    ).get()
    print_out(codelet.target_structure_two)
    codelet.target_space_two = view.parent_frame.input_space
    codelet.target_conceptual_space = bubble_chamber.conceptual_spaces["temperature"]
    assert isinstance(codelet, PotentialSubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.filter(
        lambda x: x.is_correspondence
        and x.start in jj_view.parent_frame.input_space.contents
        and x.end in ap_view.parent_frame.input_space.contents
    ).get()
    adj_label_correspondence = correspondence

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # build correspondence from ap sub-frame word to ap frame word
    codelet = SubFrameToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = jj_view.parent_frame.output_space
    codelet.target_structure_one = codelet.target_space_one.contents.where(
        is_letter_chunk=True
    ).get()
    codelet.target_space_two = ap_view.parent_frame.output_space
    codelet.target_structure_two = (
        codelet.target_space_two.contents.where(
            is_letter_chunk=True, super_chunks=bubble_chamber.new_structure_collection()
        )
        .get()
        .right_branch.get()
    )
    codelet.target_conceptual_space = None
    assert isinstance(codelet, SubFrameToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # build correspondence from very label to magnitude slot label
    codelet = SpaceToFrameCorrespondenceBuilder.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_space_one = input_space
    codelet.target_structure_one = input_space.contents.where(
        is_label=True, parent_concept=bubble_chamber.concepts["very"]
    ).get()
    codelet.target_space_two = ap_view.parent_frame.input_space
    codelet.target_structure_two = codelet.target_space_two.contents.filter(
        lambda x: x in bubble_chamber.conceptual_spaces["magnitude"].contents
        and x not in bubble_chamber.conceptual_spaces["temperature"].contents
    ).get()
    codelet.conceptual_space = bubble_chamber.conceptual_spaces["magnitude"]
    assert isinstance(codelet, SpaceToFrameCorrespondenceBuilder)
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence = codelet.child_structures.where(is_correspondence=True).get()

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceEvaluator)
    assert 0 == correspondence.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 < correspondence.quality

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, CorrespondenceSelector)
    original_correspondence_activation = correspondence.activation
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    correspondence.update_activation()
    assert original_correspondence_activation < correspondence.activation

    # END: make a sentence with "very"

    end_time = time.time()
    total_codelets_run = bubble_chamber.loggers["activity"].codelets_run
    # Expect at least 60 codelets to run per second.
    # Remove/alter the below assertion if running with less resources.
    assert (end_time - start_time) < (total_codelets_run // 60)
