from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID


class Publisher(Codelet):

    PUBLICATION_PROBABILITY_EXPONENT = HyperParameters.PUBLICATION_PROBABILITY_EXPONENT
    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        return cls(
            ID.new(cls),
            parent_id,
            bubble_chamber,
            max(urgency, cls.MINIMUM_CODELET_URGENCY),
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        return cls(
            ID.new(cls),
            parent_id,
            bubble_chamber,
            bubble_chamber.concepts["publish"].activation,
        )

    def run(self) -> CodeletResult:
        if self.bubble_chamber.worldview.views.is_empty():
            self.bubble_chamber.loggers["activity"].log(self, "There is no worldview.")
            self._fizzle()
            self.result = CodeletResult.FIZZLE
        else:
            self.bubble_chamber.loggers["activity"].log(self, "Worldview is not empty")
            publish_concept = self.bubble_chamber.concepts["publish"]
            self.bubble_chamber.loggers["activity"].log(
                self, f"Publish concept activation: {publish_concept.activation}"
            )
            if publish_concept.is_fully_active():
                self.bubble_chamber.result = self.bubble_chamber.worldview.output
                self.result = CodeletResult.FINISH
            else:
                self.bubble_chamber.loggers["activity"].log(
                    self, "Boosting publish concept"
                )
                publish_concept.boost_activation(
                    self.bubble_chamber.worldview.satisfaction
                )
                self._fizzle()
                self.result = CodeletResult.FIZZLE
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)

    def _fizzle(self) -> CodeletResult:
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.bubble_chamber.worldview.satisfaction,
            )
        )
