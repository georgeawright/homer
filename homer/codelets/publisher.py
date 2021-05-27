from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID


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

    @classmethod
    def make(cls, codelet_id: str, bubble_chamber: BubbleChamber):
        return cls(
            ID.new(cls),
            codelet_id,
            bubble_chamber,
            bubble_chamber.concepts["publish"].activation,
        )

    def run(self) -> CodeletResult:
        full_views = []
        for view in self.bubble_chamber.production_views:
            if view.activation == 0:
                continue
            proportion_of_slots_filled = len(view.slot_values) / len(view.slots)
            if proportion_of_slots_filled == 1:
                full_views.append(view)
        if len(full_views) == 0:
            return self._fail()
        view_texts = []
        for view in full_views:
            words = list(view.output_space.contents.where(is_word=True))
            words.sort(key=lambda word: word.location.coordinates[0][0])
            text = " ".join([word.value for word in words])
            view_texts.append(text)
        result_text = ". ".join(view_texts)
        self.bubble_chamber.result = result_text
        self.result = CodeletResult.SUCCESS
        return self.result

    def _fail(self) -> CodeletResult:
        self.bubble_chamber.concepts["publish"].decay_activation()
        self.result = CodeletResult.FAIL
        return self.result
