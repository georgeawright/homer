import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets import Publisher
from homer.structure_collection import StructureCollection


@pytest.mark.skip
@pytest.mark.parametrize(
    "view_quality, view_activation, random_number, success_or_fail",
    [
        (1, 1, 0, CodeletResult.SUCCESS),
        (0.5, 0.5, 0, CodeletResult.SUCCESS),
    ],
)
def test_publishes_text_from_high_quality_active_monitoring_view(
    view_quality, view_activation, random_number, success_or_fail
):
    hello = Mock()
    hello.is_word = True
    hello.value = "hello"
    hello.location.coordinates = [[0]]
    world = Mock()
    world.is_word = True
    world.value = "world"
    world.location.coordinates = [[1]]

    output_space = Mock()
    output_space.contents = StructureCollection({hello, world})
    view = Mock()
    view.output_space = output_space
    view.quality = view_quality
    view.activation = view_activation

    bubble_chamber = Mock()
    bubble_chamber.result = None
    bubble_chamber.concepts = {"publish": Mock()}
    bubble_chamber.monitoring_views = StructureCollection({view})

    with patch.object(random, "random", return_value=random_number):
        publisher = Publisher("", "", bubble_chamber, 1)
        publisher.run()
        assert success_or_fail == publisher.result
        if success_or_fail == CodeletResult.SUCCESS:
            assert "hello world" == bubble_chamber.result
        else:
            assert "" == bubble_chamber.result
