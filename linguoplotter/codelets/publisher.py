from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict


class Publisher(Codelet):

    PUBLICATION_PROBABILITY_EXPONENT = HyperParameters.PUBLICATION_PROBABILITY_EXPONENT
    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        targets = bubble_chamber.new_dict(name="targets")
        urgency = max(urgency, cls.MINIMUM_CODELET_URGENCY)
        return cls(ID.new(cls), parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        urgency = bubble_chamber.concepts["publish"]
        return cls.spawn(parent_id, bubble_chamber, urgency)

    def run(self) -> CodeletResult:
        if self.bubble_chamber.worldview.views.is_empty:
            self.bubble_chamber.loggers["activity"].log("There is no worldview.")
            self._fizzle()
            self.result = CodeletResult.FIZZLE
        else:
            self.bubble_chamber.loggers["activity"].log("Worldview is not empty")
            publish_concept = self.bubble_chamber.concepts["publish"]
            self.bubble_chamber.loggers["activity"].log(
                f"Publish concept activation: {publish_concept.activation}"
            )
            if publish_concept.is_fully_active():
                self.bubble_chamber.result = self.bubble_chamber.worldview.output
                self.result = CodeletResult.FINISH
            else:
                self.bubble_chamber.loggers["activity"].log("Boosting publish concept")
                publish_concept.boost_activation(
                    self.bubble_chamber.worldview.satisfaction
                )
                self._fizzle()
                self.result = CodeletResult.FIZZLE

    def _fizzle(self) -> CodeletResult:
        urgency = self.bubble_chamber.worldview.satisfaction
        self.child_codelets.append(
            self.spawn(self.codelet_id, self.bubble_chamber, urgency)
        )
