from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collections import StructureDict, StructureSet
from linguoplotter.structures import View


class GarbageCollector(Codelet):
    MINIMUM_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)
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
        targets = bubble_chamber.new_dict(name="targets")
        return cls(codelet_id, parent_id, bubble_chamber, coderack, targets, urgency)

    def run(self) -> CodeletResult:
        if self.bubble_chamber.recycle_bin.is_empty:
            self.result = CodeletResult.FIZZLE
        else:
            self._remove_items()
            self.result = CodeletResult.FINISH
        self._engender_follow_up()
        return self.result

    def _remove_items(self):
        worldview = self.bubble_chamber.worldview.view
        focus = self.bubble_chamber.focus.view
        for structure in self.bubble_chamber.recycle_bin:
            self.bubble_chamber.loggers["activity"].log(f"{structure}").log(
                f"Quality: {structure.quality}"
            ).log(f"Activation: {structure.activation}")
            if not structure.is_recyclable:
                self.bubble_chamber.loggers["activity"].log("NOT RECYCLABLE")
                self.bubble_chamber.recycle_bin.remove(structure)
                continue
            if worldview is not None and any(
                [
                    structure == worldview,
                    structure.is_view and structure in worldview.all_sub_views,
                    structure.is_correspondence and structure in worldview.members,
                    structure.is_link and structure in worldview.grouped_links,
                    structure.is_node and structure in worldview.grouped_nodes,
                ]
            ):
                self.bubble_chamber.loggers["activity"].log("IN WORLDVIEW")
                self.bubble_chamber.recycle_bin.remove(structure)
                continue
            if focus is not None and any(
                [
                    structure == focus,
                    structure.is_view and structure in focus.all_sub_views,
                    structure.is_correspondence and structure in focus.members,
                    structure.is_link and structure in focus.grouped_links,
                    structure.is_node and structure in focus.grouped_nodes,
                ]
            ):
                self.bubble_chamber.loggers["activity"].log("STRUCTURE IN FOCUS")
                continue
            relevant_codelets = [
                codelet
                for codelet in self.coderack._codelets
                if (
                    structure in codelet.targets.values()
                    or any(
                        [link in codelet.targets.values() for link in structure.links]
                    )
                    or any(
                        [
                            structure in view.grouped_nodes
                            for view in [
                                t
                                for t in codelet.targets.values()
                                if isinstance(t, View)
                            ]
                        ]
                    )
                    or (
                        isinstance(codelet.targets, StructureDict)
                        and codelet.targets["view"] is not None
                        and (
                            structure in codelet.targets["view"].structures
                            or structure in codelet.targets["view"].sub_views
                        )
                    )
                    or structure.is_view
                    and any(
                        [
                            item in codelet.targets.values()
                            for item in StructureSet.union(
                                *[
                                    sub_frame.input_space.contents
                                    for sub_frame in structure.parent_frame.sub_frames
                                ],
                                *[
                                    sub_frame.output_space.contents
                                    for sub_frame in structure.parent_frame.sub_frames
                                ],
                                structure.parent_frame.input_space.contents,
                                structure.parent_frame.output_space.contents,
                                structure.output_space.contents,
                            )
                        ]
                    )
                )
            ]
            if len(relevant_codelets) > 0:
                self.bubble_chamber.loggers["activity"].log("IN CODELET TARGETS")
                continue
            probability_of_removal = 1 - (
                structure.quality * self.bubble_chamber.random_machine.generate_number()
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Probability of removal: {probability_of_removal}"
            )
            # higher quality structures are more likely to be deleted as randomness increases
            if probability_of_removal > self.bubble_chamber.random_machine.randomness:
                self.bubble_chamber.loggers["activity"].log("REMOVING")
                self.bubble_chamber.recycle_bin.remove(structure)
                self.bubble_chamber.remove(structure)
                # for codelet in relevant_codelets:
                #    self.bubble_chamber.loggers["activity"].log(f"Removing {codelet}")
                #    self.coderack.remove_codelet(codelet)

    def _engender_follow_up(self):
        urgency = max(
            min(1, self.MINIMUM_URGENCY * len(self.bubble_chamber.recycle_bin)),
            self.MINIMUM_URGENCY,
        )
        self.child_codelets.append(
            self.spawn(self.codelet_id, self.bubble_chamber, self.coderack, urgency)
        )
