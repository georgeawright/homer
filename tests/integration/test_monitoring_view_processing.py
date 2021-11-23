import math
import pytest
from unittest.mock import Mock

from homer.id import ID
from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.builders.view_builders import MonitoringViewBuilder
from homer.codelets.evaluators import CorrespondenceEvaluator
from homer.codelets.evaluators.view_evaluators import MonitoringViewEvaluator
from homer.codelets.selectors import CorrespondenceSelector
from homer.codelets.selectors.view_selectors import MonitoringViewSelector
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.codelets.suggesters.view_suggesters import MonitoringViewSuggester
from homer.location import Location
from homer.locations import TwoPointLocation
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Label, Relation
from homer.structures.nodes import Chunk
from homer.structures.spaces import ContextualSpace
from homer.structures.views import SimplexView


@pytest.mark.skip
def test_monitoring_view_processing(
    bubble_chamber,
    input_concept,
    text_concept,
    same_concept,
    location_space,
    temperature_space,
    grammar_space,
    comparison_frame,
    north_concept,
    south_concept,
    cold_concept,
    hot_concept,
    hotter_concept,
    it_word,
    is_word,
    in_word,
    the_word,
    than_word,
    north_word,
    south_word,
    hotter_word,
):
    # setup input
    input_space = ContextualSpace(
        "",
        "",
        "input",
        input_concept,
        bubble_chamber.new_structure_collection(),
        conceptual_spaces=bubble_chamber.new_structure_collection(
            temperature_space, location_space
        ),
        links_in=bubble_chamber.new_structure_collection(),
        links_out=bubble_chamber.new_structure_collection(),
        parent_spaces=bubble_chamber.new_structure_collection(),
    )
    bubble_chamber.contextual_spaces.add(input_space)
    raw_chunk_1 = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], input_space),
            Location([[0, 0]], location_space),
            Location([[5]], temperature_space),
        ],
        bubble_chamber.new_structure_collection(),
        input_space,
        0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            input_space, temperature_space, location_space
        ),
        bubble_chamber.new_structure_collection(),
        is_raw=True,
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
            Location([[5]], temperature_space),
        ],
        bubble_chamber.new_structure_collection(),
        input_space,
        0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            input_space, temperature_space, location_space
        ),
        bubble_chamber.new_structure_collection(),
        is_raw=True,
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
            Location([[20]], temperature_space),
        ],
        bubble_chamber.new_structure_collection(),
        input_space,
        0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            input_space, temperature_space, location_space
        ),
        bubble_chamber.new_structure_collection(),
        is_raw=True,
    )
    input_space.add(raw_chunk_3)
    location_space.add(raw_chunk_3)
    temperature_space.add(raw_chunk_3)
    raw_chunk_4 = Chunk(
        ID.new(Chunk),
        "",
        [
            Location([[]], input_space),
            Location([[1, 1]], location_space),
            Location([[20]], temperature_space),
        ],
        bubble_chamber.new_structure_collection(),
        input_space,
        0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            input_space, temperature_space, location_space
        ),
        bubble_chamber.new_structure_collection(),
        is_raw=True,
    )
    input_space.add(raw_chunk_4)
    location_space.add(raw_chunk_4)
    temperature_space.add(raw_chunk_4)

    chunk_1 = Chunk(
        "",
        "",
        [
            Location([[]], input_space),
            Location([[0, 0], [0, 1]], location_space),
            Location([[5]], temperature_space),
        ],
        bubble_chamber.new_structure_collection(raw_chunk_1, raw_chunk_2),
        input_space,
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            input_space, temperature_space, location_space
        ),
        bubble_chamber.new_structure_collection(),
    )
    input_space.add(chunk_1)
    location_space.add(chunk_1)
    temperature_space.add(chunk_1)
    chunk_2 = Chunk(
        "",
        "",
        [
            Location([[]], input_space),
            Location([[1, 0], [1, 1]], location_space),
            Location([[20]], temperature_space),
        ],
        bubble_chamber.new_structure_collection(raw_chunk_3, raw_chunk_4),
        input_space,
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            input_space, temperature_space, location_space
        ),
        bubble_chamber.new_structure_collection(),
    )
    input_space.add(chunk_2)
    location_space.add(chunk_2)
    temperature_space.add(chunk_2)

    location_label_1 = Label(
        "",
        "",
        chunk_1,
        bubble_chamber.new_structure_collection(chunk_1),
        north_concept,
        [Location([[]], input_space), Location([[0, 0], [0, 1]], location_space)],
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(input_space, location_space),
    )
    chunk_1.links_out.add(location_label_1)
    input_space.add(location_label_1)
    location_space.add(location_label_1)
    temperature_label_1 = Label(
        "",
        "",
        chunk_1,
        bubble_chamber.new_structure_collection(chunk_1),
        cold_concept,
        [Location([[]], input_space), Location([[5]], temperature_space)],
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(input_space, temperature_space),
    )
    chunk_1.links_out.add(temperature_label_1)
    input_space.add(temperature_label_1)
    temperature_space.add(temperature_label_1)

    location_label_2 = Label(
        "",
        "",
        chunk_2,
        bubble_chamber.new_structure_collection(chunk_2),
        south_concept,
        [Location([[]], input_space), Location([[1, 0], [1, 1]], location_space)],
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(input_space, location_space),
    )
    chunk_2.links_out.add(location_label_2)
    input_space.add(location_label_2)
    location_space.add(location_label_2)
    temperature_label_2 = Label(
        "",
        "",
        chunk_2,
        bubble_chamber.new_structure_collection(chunk_2),
        hot_concept,
        [Location([[]], input_space), Location([[20]], temperature_space)],
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(input_space, temperature_space),
    )
    chunk_2.links_out.add(temperature_label_2)
    input_space.add(temperature_label_2)
    temperature_space.add(temperature_label_2)

    temperature_relation = Relation(
        "",
        "",
        chunk_2,
        bubble_chamber.new_structure_collection(chunk_1, chunk_2),
        hotter_concept,
        [
            Location([[]], input_space),
            TwoPointLocation([[20]], [[5]], temperature_space),
        ],
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(input_space, temperature_space),
    )
    chunk_2.links_out.add(temperature_relation)
    chunk_1.links_in.add(temperature_relation)
    input_space.add(temperature_relation)
    temperature_space.add(temperature_relation)

    # setup view containing text and interpretation
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

    interpretation_space = ContextualSpace(
        "",
        "",
        "interpretation",
        input_concept,
        bubble_chamber.new_structure_collection(),
        conceptual_spaces=bubble_chamber.new_structure_collection(
            temperature_space, location_space
        ),
        links_in=bubble_chamber.new_structure_collection(),
        links_out=bubble_chamber.new_structure_collection(),
        parent_spaces=bubble_chamber.new_structure_collection(),
    )
    interpretation_chunk_1 = Chunk(
        "",
        "",
        [
            Location([[]], interpretation_space),
            Location([[math.nan, math.nan]], location_space),
            Location([[math.nan]], temperature_space),
        ],
        bubble_chamber.new_structure_collection(),
        input_space,
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            interpretation_space, location_space, temperature_space
        ),
        bubble_chamber.new_structure_collection(),
    )
    interpretation_space.add(interpretation_chunk_1)
    location_space.add(interpretation_chunk_1)
    temperature_space.add(interpretation_chunk_1)
    interpretation_chunk_2 = Chunk(
        "",
        "",
        [
            Location([[]], interpretation_space),
            Location([[math.nan, math.nan]], location_space),
            Location([[math.nan]], temperature_space),
        ],
        bubble_chamber.new_structure_collection(raw_chunk_3, raw_chunk_4),
        interpretation_space,
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            interpretation_space, location_space, temperature_space
        ),
        bubble_chamber.new_structure_collection(),
    )
    interpretation_space.add(interpretation_chunk_2)
    location_space.add(interpretation_chunk_2)
    temperature_space.add(interpretation_chunk_2)
    interpretation_location_label_1 = Label(
        "",
        "",
        interpretation_chunk_1,
        bubble_chamber.new_structure_collection(interpretation_chunk_1),
        north_concept,
        [
            Location([[]], interpretation_space),
            Location([[math.nan, math.nan]], location_space),
        ],
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(interpretation_space, location_space),
    )
    interpretation_chunk_1.links_out.add(interpretation_location_label_1)
    interpretation_space.add(interpretation_location_label_1)
    location_space.add(interpretation_location_label_1)
    interpretation_location_label_2 = Label(
        "",
        "",
        interpretation_chunk_2,
        bubble_chamber.new_structure_collection(interpretation_chunk_2),
        south_concept,
        [
            Location([[]], interpretation_space),
            Location([[math.nan, math.nan]], location_space),
        ],
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(interpretation_space, location_space),
    )
    interpretation_chunk_2.links_out.add(interpretation_location_label_2)
    interpretation_space.add(interpretation_location_label_2)
    location_space.add(interpretation_location_label_2)
    interpretation_temperature_relation = Relation(
        "",
        "",
        interpretation_chunk_2,
        bubble_chamber.new_structure_collection(
            interpretation_chunk_1, interpretation_chunk_2
        ),
        hotter_concept,
        [
            Location([[]], interpretation_space),
            TwoPointLocation([[math.nan]], [[math.nan]], temperature_space),
        ],
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(
            interpretation_space, temperature_space
        ),
    )
    interpretation_chunk_2.links_out.add(interpretation_temperature_relation)
    interpretation_chunk_1.links_in.add(interpretation_temperature_relation)
    interpretation_space.add(interpretation_temperature_relation)
    temperature_space.add(interpretation_temperature_relation)

    reverse_simplex_view = SimplexView(
        "",
        "",
        [],
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(text_space, comparison_frame),
        interpretation_space,
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    bubble_chamber.views.add(reverse_simplex_view)

    location_1_correspondence = Correspondence(
        "",
        "",
        text_8,
        bubble_chamber.new_structure_collection(
            text_8, interpretation_location_label_1
        ),
        [],
        same_concept,
        location_space,
        reverse_simplex_view,
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    reverse_simplex_view.members.add(location_1_correspondence)
    location_2_correspondence = Correspondence(
        "",
        "",
        text_5,
        bubble_chamber.new_structure_collection(
            text_5, interpretation_location_label_2
        ),
        [],
        same_concept,
        location_space,
        reverse_simplex_view,
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    reverse_simplex_view.members.add(location_2_correspondence)
    temperature_relation_correspondence = Correspondence(
        "",
        "",
        text_2,
        bubble_chamber.new_structure_collection(
            text_2, interpretation_temperature_relation
        ),
        [],
        same_concept,
        temperature_space,
        reverse_simplex_view,
        1.0,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    reverse_simplex_view.members.add(temperature_relation_correspondence)

    # suggest, build, evaluate, and select initial monitoring view
    view_suggester = MonitoringViewSuggester.spawn(
        "",
        bubble_chamber,
        {
            "input_spaces": bubble_chamber.new_structure_collection(
                interpretation_space, input_space
            ),
            "output_space": text_space,
        },
        1.0,
    )
    view_suggester.run()
    assert CodeletResult.SUCCESS == view_suggester.result

    view_builder = view_suggester.child_codelets[0]
    assert isinstance(view_builder, MonitoringViewBuilder)
    view_builder.run()
    assert CodeletResult.SUCCESS == view_builder.result
    view = view_builder.child_structures.get()
    original_view_quality = view.quality
    original_view_activation = view.activation

    view_evaluator = view_builder.child_codelets[0]
    assert isinstance(view_evaluator, MonitoringViewEvaluator)
    view_evaluator.run()
    assert CodeletResult.SUCCESS == view_evaluator.result
    assert view.quality == original_view_quality

    view_selector = view_evaluator.child_codelets[0]
    assert isinstance(view_selector, MonitoringViewSelector)
    view_selector.run()
    assert CodeletResult.SUCCESS == view_selector.result
    view.update_activation()
    assert view.activation == original_view_activation

    # add correspondences between interpretation and input
    correspondence_suggester_1 = CorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": interpretation_space,
            "target_structure_one": interpretation_temperature_relation,
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
    correspondence_1_original_quality = correspondence_1.quality
    correspondence_1_original_activation = correspondence_1.activation

    correspondence_evaluator_1 = correspondence_builder_1.child_codelets[0]
    assert isinstance(correspondence_evaluator_1, CorrespondenceEvaluator)
    correspondence_evaluator_1.run()
    assert CodeletResult.SUCCESS == correspondence_evaluator_1.result
    assert correspondence_1.quality > correspondence_1_original_quality

    correspondence_selector_1 = correspondence_evaluator_1.child_codelets[0]
    assert isinstance(correspondence_selector_1, CorrespondenceSelector)
    correspondence_selector_1.run()
    assert CodeletResult.SUCCESS == correspondence_selector_1.result
    correspondence_1.update_activation()
    assert correspondence_1.activation > correspondence_1_original_activation

    # suggest an incompatible correspondence
    correspondence_suggester_2 = CorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": interpretation_space,
            "target_structure_one": interpretation_location_label_1,
            "target_space_two": input_space,
            "target_structure_two": location_label_2,
            "target_conceptual_space": None,
            "parent_concept": None,
        },
        1.0,
    )
    correspondence_suggester_2.run()
    assert CodeletResult.FIZZLE == correspondence_suggester_2.result

    # re-evaluate and re-select monitoring view
    view_evaluator_2 = view_evaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1
    )
    view_evaluator_2.run()
    assert CodeletResult.SUCCESS == view_evaluator_2.result
    assert view.quality > original_view_quality

    view_selector_2 = view_evaluator_2.child_codelets[0]
    assert isinstance(view_selector_2, MonitoringViewSelector)
    view_selector_2.run()
    assert CodeletResult.SUCCESS == view_selector_2.result
    view.update_activation()
    assert view.activation > original_view_activation

    # build another view with different correspondences
    view_2_suggester = MonitoringViewSuggester.spawn(
        "",
        bubble_chamber,
        {
            "input_spaces": bubble_chamber.new_structure_collection(
                interpretation_space, input_space
            ),
            "output_space": text_space,
        },
        1.0,
    )
    view_2_suggester.run()
    assert CodeletResult.SUCCESS == view_2_suggester.result

    view_2_builder = view_2_suggester.child_codelets[0]
    assert isinstance(view_2_builder, MonitoringViewBuilder)
    view_2_builder.run()
    assert CodeletResult.SUCCESS == view_2_builder.result
    view_2 = view_2_builder.child_structures.get()
    original_view_2_quality = view_2.quality
    original_view_2_activation = view_2.activation

    view_2_evaluator = view_2_builder.child_codelets[0]
    assert isinstance(view_2_evaluator, MonitoringViewEvaluator)
    view_2_evaluator.run()
    assert CodeletResult.SUCCESS == view_2_evaluator.result
    assert view_2.quality == original_view_2_quality

    view_2_selector = view_2_evaluator.child_codelets[0]
    assert isinstance(view_2_selector, MonitoringViewSelector)
    view_2_selector.run()
    assert CodeletResult.SUCCESS == view_2_selector.result
    view_2.update_activation()
    assert view_2.activation == original_view_2_activation

    view_2_correspondence_suggester_1 = CorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view_2,
            "target_space_one": interpretation_space,
            "target_structure_one": interpretation_temperature_relation,
            "target_space_two": None,
            "target_structure_two": None,
            "target_conceptual_space": None,
            "parent_concept": None,
        },
        1.0,
    )
    view_2_correspondence_suggester_1.run()
    assert CodeletResult.SUCCESS == view_2_correspondence_suggester_1.result

    view_2_correspondence_builder_1 = view_2_correspondence_suggester_1.child_codelets[
        0
    ]
    assert isinstance(view_2_correspondence_builder_1, CorrespondenceBuilder)
    view_2_correspondence_builder_1.run()
    assert CodeletResult.SUCCESS == view_2_correspondence_builder_1.result
    view_2_correspondence_1 = view_2_correspondence_builder_1.child_structures.get()
    view_2_correspondence_1_original_quality = view_2_correspondence_1.quality
    view_2_correspondence_1_original_activation = view_2_correspondence_1.activation

    view_2_correspondence_evaluator_1 = view_2_correspondence_builder_1.child_codelets[
        0
    ]
    assert isinstance(view_2_correspondence_evaluator_1, CorrespondenceEvaluator)
    view_2_correspondence_evaluator_1.run()
    assert CodeletResult.SUCCESS == view_2_correspondence_evaluator_1.result
    assert view_2_correspondence_1.quality > view_2_correspondence_1_original_quality

    view_2_correspondence_selector_1 = view_2_correspondence_evaluator_1.child_codelets[
        0
    ]
    assert isinstance(view_2_correspondence_selector_1, CorrespondenceSelector)
    view_2_correspondence_selector_1.run()
    assert CodeletResult.SUCCESS == view_2_correspondence_selector_1.result
    view_2_correspondence_1.update_activation()
    assert (
        view_2_correspondence_1.activation > view_2_correspondence_1_original_activation
    )

    view_2_correspondence_suggester_2 = CorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view_2,
            "target_space_one": interpretation_space,
            "target_structure_one": interpretation_location_label_1,
            "target_space_two": input_space,
            "target_structure_two": location_label_1,
            "target_conceptual_space": None,
            "parent_concept": None,
        },
        1.0,
    )
    view_2_correspondence_suggester_2.run()
    assert CodeletResult.SUCCESS == view_2_correspondence_suggester_2.result

    view_2_correspondence_builder_2 = view_2_correspondence_suggester_2.child_codelets[
        0
    ]
    assert isinstance(view_2_correspondence_builder_2, CorrespondenceBuilder)
    view_2_correspondence_builder_2.run()
    assert CodeletResult.SUCCESS == view_2_correspondence_builder_2.result
    view_2_correspondence_2 = view_2_correspondence_builder_2.child_structures.get()
    view_2_correspondence_2_original_quality = view_2_correspondence_2.quality
    view_2_correspondence_2_original_activation = view_2_correspondence_2.activation

    view_2_correspondence_evaluator_2 = view_2_correspondence_builder_2.child_codelets[
        0
    ]
    assert isinstance(view_2_correspondence_evaluator_2, CorrespondenceEvaluator)
    view_2_correspondence_evaluator_2.run()
    assert CodeletResult.SUCCESS == view_2_correspondence_evaluator_2.result
    assert view_2_correspondence_2.quality > view_2_correspondence_2_original_quality

    view_2_correspondence_selector_2 = view_2_correspondence_evaluator_2.child_codelets[
        0
    ]
    assert isinstance(view_2_correspondence_selector_2, CorrespondenceSelector)
    view_2_correspondence_selector_2.run()
    assert CodeletResult.SUCCESS == view_2_correspondence_selector_2.result
    view_2_correspondence_2.update_activation()
    assert (
        view_2_correspondence_2.activation > view_2_correspondence_2_original_activation
    )

    # re-evaluate views
    view_1_re_evaluator = MonitoringViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view), 1
    )
    view_1_re_evaluator.run()

    view_2_re_evaluator = MonitoringViewEvaluator.spawn(
        "", bubble_chamber, bubble_chamber.new_structure_collection(view_2), 1
    )
    view_2_re_evaluator.run()

    assert view_2.quality > view.quality
