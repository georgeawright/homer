from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collection import StructureCollection


class Recycler(Codelet):

    MINIMUM_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.coderack = coderack

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            coderack,
            urgency,
        )

    def run(self) -> CodeletResult:
        try:
            target = self.bubble_chamber.structures.filter(
                lambda x: x.is_recyclable and x not in self.bubble_chamber.recycle_bin
            ).get()
            self.bubble_chamber.loggers["activity"].log(self, f"Found target: {target}")
            self.bubble_chamber.recycle_bin.add(target)
            self.result = CodeletResult.FINISH
        except MissingStructureError:
            self.bubble_chamber.loggers["activity"].log(self, "Couldn't find target")
            self.result = CodeletResult.FIZZLE
        self._engender_follow_up()
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _update_garbage_collector_urgency(self):
        for codelet in self.coderack._codelets:
            if "GarbageCollector" in codelet.codelet_id:
                codelet.urgency = (
                    len(self.bubble_chamber.recycle_bin)
                    * self.coderack.MINIMUM_CODELET_URGENCY
                )
                return
        raise Exception

    def _engender_follow_up(self):
        try:
            structures_sample = StructureCollection.union(
                self.bubble_chamber.spaces.where(is_main_input=True)
                .get()
                .contents.where(is_raw=False),
                self.bubble_chamber.views,
            ).sample(10)
            recyclable_structures = structures_sample.filter(
                lambda x: x.is_recyclable and not x in self.bubble_chamber.recycle_bin
            )
            proportion_recyclable = len(recyclable_structures) / len(structures_sample)
        except MissingStructureError:
            proportion_recyclable = 0
        urgency = max(
            proportion_recyclable,
            self.MINIMUM_URGENCY,
        )
        self.child_codelets.append(
            self.spawn(self.codelet_id, self.bubble_chamber, self.coderack, urgency)
        )
