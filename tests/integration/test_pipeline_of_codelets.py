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
    assert len(view.input_spaces) == 1

    codelet = codelet.child_codelets[0]
    assert isinstance(codelet, SimplexViewEvaluator)
    assert 0 == view.quality
    codelet.run()
    assert CodeletResult.FINISH == codelet.result
    assert 0 == view.quality  # empty view has quality of 0
    assert len(view.input_spaces) == 1

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

    target_label = chunk_two.labels_in_space(
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
    assert letter_chunk.name == "cool"

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
    assert letter_chunk.name == "er"

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
    assert letter_chunk.name == "cooler"

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

    codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
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

    codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
    codelet.parent_concept = bubble_chamber.concepts["same"]
    codelet.target_structure_one = relation_correspondence.start.end.labels.filter(
        lambda x: bubble_chamber.conceptual_spaces["temperature"] in x.parent_spaces
    ).get()
    codelet.target_space_one = rp_view.parent_frame.input_space
    codelet.target_structure_two = relation_correspondence.end.end.labels.filter(
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

    codelet = SubFrameToFrameCorrespondenceSuggester.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    codelet = codelet.child_codelets[0]
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

    codelet = PotentialSubFrameToFrameCorrespondenceSuggester.spawn(
        "", bubble_chamber, {"target_view": view}, 1.0
    )
    codelet.run()
    assert CodeletResult.FINISH == codelet.result

    # END: build comparative phrase

    # START: chunk and describe more data
    # END: chunk and describe more data

    # START: compile longer piece of text
    # END: compile longer piece of text
