import statistics

from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import View


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
        text = (
            self.target_view.output_space.contents.filter(
                lambda x: x.is_chunk and x.super_chunks.is_empty()
            )
            .get()
            .name
        )
        self.bubble_chamber.loggers["activity"].log(self, "Potential text")
        self.bubble_chamber.loggers["activity"].log(
            self, "Recalculating worldview satisfaction"
        )
        self.bubble_chamber.worldview.satisfaction = (
            self.calculate_satisfaction(self.bubble_chamber.worldview.view)
            if self.bubble_chamber.worldview.view is not None
            else 0
        )
        self.bubble_chamber.loggers["activity"].log(
            self, "Calculating potential worldview satisfaction"
        )
        potential_worldview_satisfaction = self.calculate_satisfaction(self.target_view)
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
            self.bubble_chamber.concepts["publish"].decay_activation(
                self.bubble_chamber.general_satisfaction
            )
            self.result = CodeletResult.FINISH
        else:
            self.bubble_chamber.concepts["publish"].boost_activation(
                self.bubble_chamber.general_satisfaction
            )
            self._update_publisher_urgency()
            self.result = CodeletResult.FIZZLE

    def _update_publisher_urgency(self):
        for codelet in self.coderack._codelets:
            if "Publisher" in codelet.codelet_id:
                codelet.urgency = self.bubble_chamber.worldview.satisfaction
                return
        raise Exception

    def calculate_satisfaction(self, view: View) -> FloatBetweenOneAndZero:
        self.bubble_chamber.loggers["activity"].log(
            self, f"View quality: {view.quality}"
        )
        return fuzzy.AND(
            fuzzy.OR(view.quality, self.frame_depth_score(view)),
            fuzzy.OR(
                self.proportion_of_input_in_view(view), self.frame_types_score(view)
            ),
        )

    def proportion_of_input_in_view(self, view: View) -> FloatBetweenOneAndZero:
        size_of_raw_input_in_view = len(
            self.bubble_chamber.new_structure_collection(
                *[
                    (raw_input_member, correspondence.conceptual_space)
                    for correspondence in view.members
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
        proportion = size_of_raw_input_in_view / self.bubble_chamber.size_of_raw_input
        self.bubble_chamber.loggers["activity"].log(
            self, f"Proportion of input in view: {proportion}"
        )
        return proportion

    def frame_types_score(self, view: View) -> FloatBetweenOneAndZero:
        frame_types = self.bubble_chamber.new_structure_collection()
        for frame in view.frames:
            frame_type = frame
            while frame_type.parent_frame is not None:
                frame_type = frame_type.parent_frame
            frame_types.add(frame_type)
        number_of_frame_types_in_view = len(frame_types)
        score = 1 / number_of_frame_types_in_view
        self.bubble_chamber.loggers["activity"].log(self, f"Frame types score: {score}")
        return score

    def frame_depth_score(self, view) -> FloatBetweenOneAndZero:
        score = view.parent_frame.depth / 10
        self.bubble_chamber.loggers["activity"].log(self, f"Frame depth score: {score}")
        return score

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                max(
                    self.bubble_chamber.worldview.satisfaction,
                    self.MINIMUM_CODELET_URGENCY,
                ),
            )
        )
