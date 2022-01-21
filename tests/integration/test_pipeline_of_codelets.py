from homer.codelet_result import CodeletResult
from homer.codelets.builders import (
    ChunkBuilder,
    LabelBuilder,
    RelationBuilder,
)
from homer.codelets.evaluators import (
    CorrespondenceEvaluator,
    ChunkEvaluator,
    LabelEvaluator,
    RelationEvaluator,
)
from homer.codelets.selectors import (
    CorrespondenceSelector,
    ChunkSelector,
    LabelSelector,
    RelationSelector,
)
from homer.codelets.suggesters import (
    ChunkSuggester,
    LabelSuggester,
    RelationSuggester,
)


def test_pipeline_of_codelets(homer):
    bubble_chamber = homer.bubble_chamber
    input_space = bubble_chamber.contextual_spaces["input"]
    location_space = bubble_chamber.conceptual_spaces["location"]

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
    label.update_activation()
    assert CodeletResult.FINISH == codelet.result
    assert original_label_activation < label.activation
