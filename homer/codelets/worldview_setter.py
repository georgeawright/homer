from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.hyper_parameters import HyperParameters
from homer.id import ID
from homer.structure_collection import StructureCollection


class WorldviewSetter(Codelet):

    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.coderack = coderack
        self.target_view = None
        self.result = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, coderack, urgency)

    def run(self) -> CodeletResult:
        try:
            self.target_view = self.bubble_chamber.production_views.filter(
                lambda x: x.unhappiness < HyperParameters.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept.name == "sentence"
                and x != self.bubble_chamber.worldview.view
            ).get(key=lambda x: x.activation * (1 - (1 / len(x.members))))
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found target view: {self.target_view}"
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Target view activation: {self.target_view.activation}"
            )
            self.run_competition()
        except MissingStructureError:
            self.result = CodeletResult.FIZZLE
        self._engender_follow_up()
        self.bubble_chamber.loggers["activity"].log_follow_ups(self)
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def run_competition(self):
        size_of_raw_input_in_view = len(
            self.bubble_chamber.new_structure_collection(
                *[
                    (raw_input_member, correspondence.conceptual_space)
                    for correspondence in self.target_view.members
                    if correspondence.start.is_link
                    and correspondence.start.start.is_chunk
                    and correspondence.start.parent_space.is_main_input
                    for raw_input_member in StructureCollection.union(
                        *[
                            argument.raw_members
                            for argument in correspondence.start.arguments
                        ]
                    )
                    if correspondence.conceptual_space is not None
                ]
            )
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Size of raw input in view: {size_of_raw_input_in_view}"
        )
        proportion_of_input_in_view = (
            size_of_raw_input_in_view / self.bubble_chamber.size_of_raw_input
        )
        self.bubble_chamber.loggers["activity"].log(
            self, f"Proportion of raw input in view: {proportion_of_input_in_view}"
        )
        frame_types = self.bubble_chamber.new_structure_collection()
        for frame in self.target_view.frames:
            frame_type = frame
            while frame_type.parent_frame is not None:
                frame_type = frame_type.parent_frame
            frame_types.add(frame_type)
        number_of_frame_types_in_view = len(frame_types)
        self.bubble_chamber.loggers["activity"].log(
            self, f"Number of frame types in view: {number_of_frame_types_in_view}"
        )
        potential_worldview_satisfaction = (
            self.target_view.quality * proportion_of_input_in_view
        )
        # potential_worldview_satisfaction = self.target_view.quality * (
        #    proportion_of_input_in_view / number_of_frame_types_in_view
        # )
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Potential worldview satisfaction: {potential_worldview_satisfaction}",
        )
        self.bubble_chamber.loggers["activity"].log(
            self,
            f"Current worldview satisfaction: {self.bubble_chamber.worldview.satisfaction}",
        )
        if (
            potential_worldview_satisfaction
            > self.bubble_chamber.worldview.satisfaction
        ):
            self.bubble_chamber.worldview.view = self.target_view
            self.bubble_chamber.worldview.satisfaction = (
                potential_worldview_satisfaction
            )
            self.result = CodeletResult.FINISH
        else:
            self.result = CodeletResult.FIZZLE

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                max(
                    self.bubble_chamber.general_satisfaction,
                    self.MINIMUM_CODELET_URGENCY,
                ),
            )
        )
