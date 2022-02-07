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
    np_frame = bubble_chamber.frames.filter(
        lambda x: x.input_space == correspondence.end.parent_space
    ).get()
    codelet.target_space_two = view.parent_frame.output_space
    codelet.target_structure_two = codelet.target_space_two.contents.filter(
        lambda x: x.is_label
        and x.parent_concept == bubble_chamber.concepts["np"]
        and x in np_frame.output_space.contents
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
        == "it will be colder in the northwest than in the northeast"
    )

    # END: build comparative phrase

    # START: chunk and describe more data
    # target_node = input_space.contents.filter(
    #    lambda x: x.has_location_in_space(location_space)
    #    and x.location_in_space(location_space).coordinates == [[0, 4]]
    # ).get()
    # codelet = ChunkSuggester.spawn(
    #    "",
    #    bubble_chamber,
    #    {"target_space": input_space, "target_node": target_node, "target_rule": None},
    #    1.0,
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, ChunkBuilder)
    # assert target_node.super_chunks.is_empty()
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # assert not target_node.super_chunks.is_empty()

    # chunk = codelet.child_structures.where(is_slot=False).get()
    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, ChunkEvaluator)
    # assert 0 == chunk.quality
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # assert 0 < chunk.quality

    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, ChunkSelector)
    # original_chunk_activation = chunk.activation
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # chunk.update_activation()
    # assert original_chunk_activation < chunk.activation

    # codelet = [c for c in codelet.child_codelets if isinstance(c, ChunkSuggester)][0]
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, ChunkBuilder)
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # chunk = codelet.child_structures.where(is_slot=False).get()
    # assert 3 == chunk.size

    # chunk_quality = chunk.quality
    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, ChunkEvaluator)
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # assert chunk_quality <= chunk.quality

    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, ChunkSelector)
    # original_chunk_activation = chunk.activation
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # chunk.update_activation()
    # assert original_chunk_activation <= chunk.activation
    # parent_concept = bubble_chamber.concepts["cool"]
    # codelet = LabelSuggester.spawn(
    #    "",
    #    bubble_chamber,
    #    {"target_node": chunk, "parent_concept": parent_concept},
    #    1.0,
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, LabelBuilder)
    # assert not chunk.has_label_with_name("cool")
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # assert chunk.has_label_with_name("cool")

    # label = codelet.child_structures.get()
    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, LabelEvaluator)
    # assert 0 == label.quality
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # assert 0 < label.quality

    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, LabelSelector)
    # original_label_activation = label.activation
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # label.update_activation()
    # assert original_label_activation < label.activation

    # parent_concept = bubble_chamber.concepts["northeast"]

    # codelet = LabelSuggester.spawn(
    #    "",
    #    bubble_chamber,
    #    {"target_node": chunk, "parent_concept": parent_concept},
    #    1.0,
    # )
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result

    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, LabelBuilder)
    # assert not chunk.has_label_with_name("northeast")
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # assert chunk.has_label_with_name("northeast")

    # label = codelet.child_structures.get()
    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, LabelEvaluator)
    # assert 0 == label.quality
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # assert 0 < label.quality

    # codelet = codelet.child_codelets[0]
    # assert isinstance(codelet, LabelSelector)
    # original_label_activation = label.activation
    # codelet.run()
    # assert CodeletResult.FINISH == codelet.result
    # label.update_activation()
    # assert original_label_activation < label.activation
    # chunk_two = chunk

    # END: chunk and describe more data

    # START: compile longer piece of text
    # END: compile longer piece of text
