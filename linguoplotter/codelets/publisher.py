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
        coderack: "Coderack",
        targets: StructureDict,
        last_satisfaction: FloatBetweenOneAndZero,
        last_time: int,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)
        self.coderack = coderack
        self.last_satisfaction = last_satisfaction
        self.last_time = last_time

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        last_satisfaction: FloatBetweenOneAndZero,
        last_time: int,
        urgency: FloatBetweenOneAndZero,
    ):
        targets = bubble_chamber.new_dict(name="targets")
        urgency = max(urgency, cls.MINIMUM_CODELET_URGENCY)
        return cls(
            ID.new(cls),
            parent_id,
            bubble_chamber,
            coderack,
            targets,
            last_satisfaction,
            last_time,
            urgency,
        )

    def run(self) -> CodeletResult:
        if self.bubble_chamber.worldview.view is None:
            self.bubble_chamber.loggers["activity"].log("Worldview is empty.")
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return
        self.bubble_chamber.loggers["activity"].log("Worldview is not empty.")
        if self.bubble_chamber.focus.view is not None:
            self.bubble_chamber.loggers["activity"].log("Focus is not empty.")
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return
        self.bubble_chamber.loggers["activity"].log("Focus is empty.")
        satisfaction_difference = (
            self.bubble_chamber.general_satisfaction - self.last_satisfaction
        )
        time_difference = self.coderack.codelets_run - self.last_time
        satisfaction_gradient = satisfaction_difference / time_difference
        random_number = self.bubble_chamber.random_machine.generate_number() - 0.5
        self.bubble_chamber.loggers["activity"].log(
            f"Satisfaction gradient: {satisfaction_gradient}"
        )
        self.bubble_chamber.loggers["activity"].log(f"Random number: {random_number}")
        if satisfaction_gradient > random_number:
            self.bubble_chamber.loggers["activity"].log(
                "Satisfaction is increasing too much."
            )
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return
        publish_concept = self.bubble_chamber.concepts["publish"]
        self.bubble_chamber.loggers["activity"].log(
            f"Publish concept activation: {publish_concept.activation}"
        )
        if not publish_concept.is_fully_active():
            self.bubble_chamber.loggers["activity"].log("Boosting publish concept")
            publish_concept.boost_activation(self.bubble_chamber.worldview.satisfaction)
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return
        self.bubble_chamber.loggers["activity"].log("Publishing")
        self.bubble_chamber.result = self.bubble_chamber.worldview.output
        self.result = CodeletResult.FINISH

    def _fizzle(self) -> CodeletResult:
        self._update_bottom_up_factories_urgencies()
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                last_satisfaction=self.bubble_chamber.general_satisfaction,
                last_time=self.coderack.codelets_run,
                urgency=self.bubble_chamber.worldview.satisfaction,
            )
        )

    def _update_bottom_up_factories_urgencies(self):
        for codelet in self.coderack._codelets:
            if (
                "BottomUpSuggesterFactory" in codelet.codelet_id
                or "BottomUpEvaluatorFactory" in codelet.codelet_id
            ):
                codelet.urgency = 1.0
