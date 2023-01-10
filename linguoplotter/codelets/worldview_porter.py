import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict, StructureSet


class WorldviewPorter(Codelet):

    MINIMUM_CODELET_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY
    INPUT_WEIGHT = HyperParameters.WORLDVIEW_QUALITY_PROPORTION_OF_INPUT_WEIGHT
    VIEW_WEIGHT = HyperParameters.WORLDVIEW_QUALITY_VIEW_QUALITY_WEIGHT
    FRAMES_WEIGHT = HyperParameters.WORLDVIEW_QUALITY_NUMBER_OF_FRAMES_WEIGHT

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
        targets = bubble_chamber.new_dict(name="targets")
        return cls(codelet_id, parent_id, bubble_chamber, coderack, targets, urgency)

    def run(self) -> CodeletResult:
        try:
            self.targets["view"] = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < HyperParameters.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept.name == "sentence"
            ).get(key=lambda x: x.activation)
            self.run_competition()
            self._engender_follow_up()
        except MissingStructureError:
            self.result = CodeletResult.FIZZLE
            self._fizzle()
        return self.result

    def run_competition(self):
        competing_view_collection = self._get_competing_view_collection()
        self.bubble_chamber.loggers["activity"].log_set(
            competing_view_collection, "Assembled competing views"
        )
        if competing_view_collection == self.bubble_chamber.worldview.views:
            raise MissingStructureError
        current_worldview_satisfaction = self._calculate_satisfaction(
            self.bubble_chamber.worldview.views
        )
        potential_worldview_satisfaction = self._calculate_satisfaction(
            competing_view_collection
        )
        if self.bubble_chamber.random_machine.randomize_number(
            potential_worldview_satisfaction
        ) > self.bubble_chamber.random_machine.randomize_number(
            self.bubble_chamber.worldview.satisfaction
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
            self._update_publisher_urgency()
            self.result = CodeletResult.FIZZLE

    def _fizzle(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                self.MINIMUM_CODELET_URGENCY,
            )
        )

    def _engender_follow_up(self):
        urgency = max(
            self.bubble_chamber.worldview.satisfaction,
            self.MINIMUM_CODELET_URGENCY,
        )
        self.child_codelets.append(
            self.spawn(self.codelet_id, self.bubble_chamber, self.coderack, urgency)
        )

    def _update_publisher_urgency(self):
        for codelet in self.coderack._codelets:
            if "Publisher" in codelet.codelet_id:
                codelet.urgency = self.bubble_chamber.worldview.satisfaction
                return
        raise Exception

    def _get_competing_view_collection(self) -> StructureSet:
        competing_views = self.bubble_chamber.new_set(name="competing views")
        component_views = []

        def add_to_competing_views(view):
            if view.output in component_views:
                return
            super_views = [view]
            while len(super_views) > 0:
                super_view = super_views.pop()
                component_views.append(super_view.output)
                for sub_view in super_view.sub_views:
                    if sub_view.parent_frame.parent_concept.name == "sentence":
                        super_views.append(sub_view)
            competing_views.add(view)

        add_to_competing_views(self.targets["view"])
        if self.bubble_chamber.worldview.views is not None:
            for view in self.bubble_chamber.worldview.views:
                if self.bubble_chamber.random_machine.coin_flip():
                    add_to_competing_views(view)

        return competing_views

    def _calculate_satisfaction(self, views: StructureSet) -> FloatBetweenOneAndZero:
        if views.is_empty:
            return 0
        proportion_of_input = self._proportion_of_input_in_views(views)
        sum_of_tree_depths = sum(v.parent_frame.tree_depth for v in views)
        view_quality = statistics.fmean([view.quality for view in views])
        self.bubble_chamber.loggers["activity"].log(
            f"proportion of input {proportion_of_input}"
        )
        self.bubble_chamber.loggers["activity"].log(
            f"sum of tree depths {sum_of_tree_depths}"
        )
        self.bubble_chamber.loggers["activity"].log(f"view quality {view_quality}")
        satisfaction = sum(
            [
                self.INPUT_WEIGHT * proportion_of_input,
                self.VIEW_WEIGHT * view_quality,
                self.FRAMES_WEIGHT * 1 / sum_of_tree_depths,
            ]
        )
        view_ids = [view.structure_id for view in views]
        self.bubble_chamber.loggers["activity"].log(
            f"Satisfaction for {view_ids}: {satisfaction}"
        )
        return satisfaction

    def _view_quality_score(self, views: StructureSet) -> FloatBetweenOneAndZero:
        if views.is_empty:
            return 0
        return statistics.fmean([view.quality for view in views])

    def _proportion_of_input_in_views(
        self, views: StructureSet
    ) -> FloatBetweenOneAndZero:
        if views.is_empty:
            return 0
        size_of_raw_input_in_views = len(
            self.bubble_chamber.new_set(
                *[
                    (raw_input_member, correspondence.conceptual_space)
                    for view in views
                    for correspondence in view.members
                    if correspondence.start.is_link
                    and correspondence.start.start.is_chunk
                    and correspondence.start.parent_space is not None
                    and correspondence.start.parent_space.is_main_input
                    for raw_input_member in StructureSet.union(
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
        return proportion

    def _frame_types_score(self, views: StructureSet) -> FloatBetweenOneAndZero:
        if views.is_empty:
            return 0
        frame_types = self.bubble_chamber.new_set()
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

    def _frame_depth_score(self, views: StructureSet) -> FloatBetweenOneAndZero:
        if views.is_empty:
            return 0
        score = statistics.fmean([view.parent_frame.depth / 10 for view in views])
        self.bubble_chamber.loggers["activity"].log(f"Frame depth score: {score}")
        return score
