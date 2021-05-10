import random

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero


class Publisher(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber

    def run(self) -> CodeletResult:
        target_view = self.bubble_chamber.monitoring_views.get_active()
        if (
            target_view.quality > random.random()
            and target_view.activation > random.random()
        ):
            words = list(target_view.output_space.contents.where(is_word=True))
            words.sort(key=lambda word: word.location.coordinates[0][0])
            text = " ".join([word.value for word in words])
            self.bubble_chamber.result = text
            self.result = CodeletResult.SUCCESS
        else:
            self.result = CodeletResult.FAIL
