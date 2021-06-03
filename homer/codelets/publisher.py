import random

from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


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
        try:
            target_view = StructureCollection(
                {
                    view
                    for view in self.bubble_chamber.monitoring_views
                    if any(
                        [
                            structure.has_label_with_name("s")
                            for structure in view.output_space.contents
                        ]
                    )
                }
            ).get(key=activation)
        except MissingStructureError:
            return self._fail()
        if (
            target_view.quality > random.random()
            and target_view.activation > random.random()
        ):
            words = list(target_view.output_space.contents.where(is_word=True))
            words.sort(key=lambda word: word.location.coordinates[0][0])
            text = " ".join([word.value for word in words])
            self.bubble_chamber.result = text
            self.result = CodeletResult.SUCCESS
            return self.result
        return self._fail()

    def _fail(self) -> CodeletResult:
        self.bubble_chamber.concepts["publish"].decay_activation()
        self.result = CodeletResult.FAIL
        return self.result
