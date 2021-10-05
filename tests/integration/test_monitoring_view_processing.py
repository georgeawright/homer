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
        StructureCollection(),
        conceptual_spaces=StructureCollection({temperature_space, location_space}),
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
        StructureCollection(),
        input_space,
        0,
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
        StructureCollection(),
        input_space,
        0,
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
        StructureCollection(),
        input_space,
        0,
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
        StructureCollection(),
        input_space,
        0,
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
        StructureCollection({raw_chunk_1, raw_chunk_2}),
        input_space,
        1.0,
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
        StructureCollection({raw_chunk_3, raw_chunk_4}),
        input_space,
        1.0,
    )
    input_space.add(chunk_2)
    location_space.add(chunk_2)
    temperature_space.add(chunk_2)

    location_label_1 = Label(
        "",
        "",
        chunk_1,
        north_concept,
        [Location([[]], input_space), Location([[0, 0], [0, 1]], location_space)],
        1.0,
    )
    chunk_1.links_out.add(location_label_1)
    input_space.add(location_label_1)
    location_space.add(location_label_1)
    temperature_label_1 = Label(
        "",
        "",
        chunk_1,
        cold_concept,
        [Location([[]], input_space), Location([[5]], temperature_space)],
        1.0,
    )
    chunk_1.links_out.add(temperature_label_1)
    input_space.add(temperature_label_1)
    temperature_space.add(temperature_label_1)

    location_label_2 = Label(
        "",
        "",
        chunk_2,
        south_concept,
        [Location([[]], input_space), Location([[1, 0], [1, 1]], location_space)],
        1.0,
    )
    chunk_2.links_out.add(location_label_2)
    input_space.add(location_label_2)
    location_space.add(location_label_2)
    temperature_label_2 = Label(
        "",
        "",
        chunk_2,
        hot_concept,
        [Location([[]], input_space), Location([[20]], temperature_space)],
        1.0,
    )
    chunk_2.links_out.add(temperature_label_2)
    input_space.add(temperature_label_2)
    temperature_space.add(temperature_label_2)

    temperature_relation = Relation(
        "",
        "",
        chunk_2,
        chunk_1,
        hotter_concept,
        [
            Location([[]], input_space),
            TwoPointLocation([[20]], [[5]], temperature_space),
        ],
        1.0,
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
        StructureCollection(),
        conceptual_spaces=StructureCollection({grammar_space}),
    )
    text_0 = it_word.copy_to_location(Location([[0]], text_space), quality=1.0)
    text_1 = is_word.copy_to_location(Location([[1]], text_space), quality=1.0)
    text_2 = hotter_word.copy_to_location(Location([[2]], text_space), quality=1.0)
    text_3 = in_word.copy_to_location(Location([[3]], text_space), quality=1.0)
    text_4 = the_word.copy_to_location(Location([[4]], text_space), quality=1.0)
    text_5 = south_word.copy_to_location(Location([[5]], text_space), quality=1.0)
    text_6 = than_word.copy_to_location(Location([[6]], text_space), quality=1.0)
    text_7 = the_word.copy_to_location(Location([[7]], text_space), quality=1.0)
    text_8 = north_word.copy_to_location(Location([[8]], text_space), quality=1.0)

    interpretation_space = ContextualSpace(
        "",
        "",
        "interpretation",
        input_concept,
        StructureCollection(),
        conceptual_spaces=StructureCollection({temperature_space, location_space}),
    )
    interpretation_chunk_1 = Chunk(
        "",
        "",
        [
            Location([[]], interpretation_space),
            Location([[None, None]], location_space),
            Location([[None]], temperature_space),
        ],
        StructureCollection(),
        input_space,
        1.0,
    )
    interpretation_space.add(interpretation_chunk_1)
    location_space.add(interpretation_chunk_1)
    temperature_space.add(interpretation_chunk_1)
    interpretation_chunk_2 = Chunk(
        "",
        "",
        [
            Location([[]], interpretation_space),
            Location([[None, None]], location_space),
            Location([[None]], temperature_space),
        ],
        StructureCollection({raw_chunk_3, raw_chunk_4}),
        interpretation_space,
        1.0,
    )
    interpretation_space.add(interpretation_chunk_2)
    location_space.add(interpretation_chunk_2)
    temperature_space.add(interpretation_chunk_2)
    interpretation_location_label_1 = Label(
        "",
        "",
        interpretation_chunk_1,
        north_concept,
        [
            Location([[]], interpretation_space),
            Location([[None, None]], location_space),
        ],
        1.0,
    )
    interpretation_chunk_1.links_out.add(interpretation_location_label_1)
    interpretation_space.add(interpretation_location_label_1)
    location_space.add(interpretation_location_label_1)
    interpretation_location_label_2 = Label(
        "",
        "",
        interpretation_chunk_2,
        south_concept,
        [
            Location([[]], interpretation_space),
            Location([[None, None]], location_space),
        ],
        1.0,
    )
    interpretation_chunk_2.links_out.add(interpretation_location_label_2)
    interpretation_space.add(interpretation_location_label_2)
    location_space.add(interpretation_location_label_2)
    interpretation_temperature_relation = Relation(
        "",
        "",
        interpretation_chunk_2,
        interpretation_chunk_1,
        hotter_concept,
        [
            Location([[]], interpretation_space),
            TwoPointLocation([[None]], [[None]], temperature_space),
        ],
        1.0,
    )
    interpretation_chunk_2.links_out.add(interpretation_temperature_relation)
    interpretation_chunk_1.links_in.add(interpretation_temperature_relation)
    interpretation_space.add(interpretation_temperature_relation)
    temperature_space.add(interpretation_temperature_relation)

    reverse_simplex_view = SimplexView(
        "",
        "",
        [],
        StructureCollection(),
        StructureCollection({text_space, comparison_frame}),
        interpretation_space,
        1.0,
    )
    bubble_chamber.views.add(reverse_simplex_view)

    location_1_correspondence = Correspondence(
        "",
        "",
        text_8,
        interpretation_location_label_1,
        [],
        same_concept,
        location_space,
        reverse_simplex_view,
        1.0,
    )
    reverse_simplex_view.members.add(location_1_correspondence)
    location_2_correspondence = Correspondence(
        "",
        "",
        text_5,
        interpretation_location_label_2,
        [],
        same_concept,
        location_space,
        reverse_simplex_view,
        1.0,
    )
    reverse_simplex_view.members.add(location_2_correspondence)
    temperature_relation_correspondence = Correspondence(
        "",
        "",
        text_2,
        interpretation_temperature_relation,
        [],
        same_concept,
        temperature_space,
        reverse_simplex_view,
        1.0,
    )
    reverse_simplex_view.members.add(temperature_relation_correspondence)

    # suggest, build, evaluate, and select initial monitoring view
    view_suggester = MonitoringViewSuggester.spawn(
        "",
        bubble_chamber,
        {
            "input_spaces": StructureCollection({interpretation_space, input_space}),
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
    assert CodeletResult.SUCCESS == correspondence_suggester_2.result

    correspondence_builder_2 = correspondence_suggester_2.child_codelets[0]
    assert isinstance(correspondence_builder_2, CorrespondenceBuilder)
    correspondence_builder_2.run()
    assert CodeletResult.SUCCESS == correspondence_builder_2.result
    correspondence_2 = correspondence_builder_2.child_structures.get()
    correspondence_2_original_quality = correspondence_2.quality
    correspondence_2_original_activation = correspondence_2.activation

    correspondence_evaluator_2 = correspondence_builder_2.child_codelets[0]
    assert isinstance(correspondence_evaluator_2, CorrespondenceEvaluator)
    correspondence_evaluator_2.run()
    assert CodeletResult.SUCCESS == correspondence_evaluator_2.result
    assert correspondence_2.quality > correspondence_2_original_quality

    correspondence_selector_2 = correspondence_evaluator_2.child_codelets[0]
    assert isinstance(correspondence_selector_2, CorrespondenceSelector)
    correspondence_selector_2.run()
    assert CodeletResult.SUCCESS == correspondence_selector_2.result
    correspondence_2.update_activation()
    assert correspondence_2.activation > correspondence_2_original_activation

    # suggest an incompatible correspondence
    correspondence_suggester_3 = CorrespondenceSuggester.spawn(
        "",
        bubble_chamber,
        {
            "target_view": view,
            "target_space_one": interpretation_space,
            "target_structure_one": interpretation_location_label_1,
            "target_space_two": input_space,
            "target_structure_two": location_label_1,
            "target_conceptual_space": None,
            "parent_concept": None,
        },
        1.0,
    )
    correspondence_suggester_3.run()
    assert CodeletResult.FIZZLE == correspondence_suggester_3.result

    # re-evaluate and re-select monitoring view
    view_evaluator_2 = view_evaluator.spawn(
        "", bubble_chamber, StructureCollection({view}), 1
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
            "input_spaces": StructureCollection({interpretation_space, input_space}),
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

    # re-evaluate views and select new view
