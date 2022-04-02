from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters
from homer.id import ID


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
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber

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
        target_view = self.bubble_chamber.worldview.view
        if target_view is None:
            self.bubble_chamber.loggers["activity"].log(self, "There is no worldview.")
            self._fizzle()
            self.result = CodeletResult.FIZZLE
        elif (
            target_view.parent_frame.parent_concept
            != self.bubble_chamber.concepts["sentence"]
        ):
            self.bubble_chamber.loggers["activity"].log(
                self, "Worldview has no sentence."
            )
            self._fizzle()
            self.result = CodeletResult.FIZZLE
        else:
            random_number = self.bubble_chamber.random_machine.generate_number()
            self.bubble_chamber.loggers["activity"].log(
                self, f"Random number: {random_number}"
            )
            self.bubble_chamber.loggers["activity"].log(
                self,
                f"Worldview satisfaction: {self.bubble_chamber.worldview.satisfaction}",
            )
            if (
                self.bubble_chamber.worldview.satisfaction
                ** self.PUBLICATION_PROBABILITY_EXPONENT
                > random_number
            ):
                self._fizzle()
                self.result = CodeletResult.FIZZLE
            else:
                main_chunk = target_view.output_space.contents.filter(
                    lambda x: x.is_chunk and x.super_chunks.is_empty()
                ).get()
                self.bubble_chamber.result = main_chunk.name
                self.result = CodeletResult.FINISH
        self.bubble_chamber.loggers["activity"].log_result(self)

    def _fizzle(self) -> CodeletResult:
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.bubble_chamber.worldview.satisfaction,
            )
        )
