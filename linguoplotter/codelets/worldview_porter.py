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


class WorldviewPorter(Codelet):

    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

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
                and x not in self.bubble_chamber.worldview.views
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
        competing_view_collection = self._get_competing_view_collection()
        self.bubble_chamber.loggers["activity"].log_collection(
            self, competing_view_collection, "Assembled competing views"
        )
        current_worldview_satisfaction = self._calculate_satisfaction(
            self.bubble_chamber.worldview.views
        )
        potential_worldview_satisfaction = self._calculate_satisfaction(
            competing_view_collection
        )
        if (
            potential_worldview_satisfaction
            > self.bubble_chamber.worldview.satisfaction
        ):
            self.bubble_chamber.worldview.views = competing_view_collection
            self.bubble_chamber.worldview.satisfaction = (
                potential_worldview_satisfaction
            )
            self.bubble_chamber.concepts["publish"].decay_activation(
                self.bubble_chamber.general_satisfaction
            )
            self.result = CodeletResult.FINISH
        else:
            self.bubble_chamber.worldview.satisfaction = current_worldview_satisfaction
            self.bubble_chamber.concepts["publish"].boost_activation(
                self.bubble_chamber.general_satisfaction
            )
            self._update_publisher_urgency()
            self.result = CodeletResult.FIZZLE

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

    def _update_publisher_urgency(self):
        for codelet in self.coderack._codelets:
            if "Publisher" in codelet.codelet_id:
                codelet.urgency = self.bubble_chamber.worldview.satisfaction
                return
        raise Exception

    def _get_competing_view_collection(self) -> StructureCollection:
        compatible_views = self.bubble_chamber.new_structure_collection(
            self.target_view
        )
        current_worldview_views = self.bubble_chamber.worldview.views.copy()
        while not current_worldview_views.is_empty():
            view = current_worldview_views.pop()
            if self._is_compatible(view, compatible_views):
                compatible_views.add(view)
        return compatible_views

    def _is_compatible(self, view: View, views: StructureCollection) -> bool:
        collected_raw_input = StructureCollection.union(
            *[view.raw_input_nodes() for collected_view in views]
        )
        for collected_view in views:
            if collected_view.output == view.output:
                return False
            overlapping_raw_input = StructureCollection.intersection(
                view.raw_input_nodes(), collected_raw_input
            )
            if len(overlapping_raw_input) / len(view.raw_input_nodes()) > 0.5:
                return False
        return True

    def _calculate_satisfaction(
        self, views: StructureCollection
    ) -> FloatBetweenOneAndZero:
        return fuzzy.AND(
            self._proportion_of_input_in_views(views),
            fuzzy.OR(
                self._view_quality_score(views),
                self._frame_depth_score(views),
                self._frame_types_score(views),
            ),
        )

    def _view_quality_score(self, views: StructureCollection) -> FloatBetweenOneAndZero:
        if views.is_empty():
            return 0
        return statistics.fmean([view.quality for view in views])

    def _proportion_of_input_in_views(
        self, views: StructureCollection
    ) -> FloatBetweenOneAndZero:
        if views.is_empty():
            return 0
        size_of_raw_input_in_views = len(
            self.bubble_chamber.new_structure_collection(
                *[
                    (raw_input_member, correspondence.conceptual_space)
                    for view in views
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
        proportion = size_of_raw_input_in_views / self.bubble_chamber.size_of_raw_input
        self.bubble_chamber.loggers["activity"].log(
            self, f"Proportion of input in view: {proportion}"
        )
        return proportion

    def _frame_types_score(self, views: StructureCollection) -> FloatBetweenOneAndZero:
        if views.is_empty():
            return 0
        frame_types = self.bubble_chamber.new_structure_collection()
        for view in views:
            for frame in view.frames:
                frame_type = frame
                while frame_type.parent_frame is not None:
                    frame_type = frame_type.parent_frame
                frame_types.add(frame_type)
        number_of_frame_types_in_views = len(frame_types)
        score = 1 / number_of_frame_types_in_views
        self.bubble_chamber.loggers["activity"].log(self, f"Frame types score: {score}")
        return score

    def _frame_depth_score(self, views: StructureCollection) -> FloatBetweenOneAndZero:
        if views.is_empty():
            return 0
        score = statistics.fmean([view.parent_frame.depth / 10 for view in views])
        self.bubble_chamber.loggers["activity"].log(self, f"Frame depth score: {score}")
        return score
