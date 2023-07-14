import statistics

from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict, StructureSet
from linguoplotter.structures import View


class WorldviewSetter(Codelet):
    CORRECTNESS_WEIGHT = HyperParameters.WORLDVIEW_QUALITY_CORRECTNESS_WEIGHT
    COMPLETENESS_WEIGHT = HyperParameters.WORLDVIEW_QUALITY_COMPLETENESS_WEIGHT
    CONCISENESS_WEIGHT = HyperParameters.WORLDVIEW_QUALITY_CONCISENESS_WEIGHT
    COHESIVENESS_WEIGHT = HyperParameters.WORLDVIEW_QUALITY_COHESION_WEIGHT

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
        try:
            self.targets["view"] = self.bubble_chamber.views.filter(
                lambda x: x.parent_frame.number_of_items_left_to_process == 0
                and x.parent_frame.parent_concept.location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
                == self.bubble_chamber.concepts["sentence"].location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
                and x != self.bubble_chamber.worldview.view
            ).get(key=lambda x: fuzzy.AND(x.activation, 1 - 1 / x.parent_frame.depth))
            self.run_competition()
            self._engender_follow_up()
        except MissingStructureError:
            self.result = CodeletResult.FIZZLE
            self._fizzle()
        return self.result

    def run_competition(self):
        choices = {
            view: self._calculate_satisfaction(view)
            for view in [self.targets["view"], self.bubble_chamber.worldview.view]
        }
        winner = self.bubble_chamber.random_machine.select(
            choices.keys(), key=lambda x: choices[x]
        )
        self.bubble_chamber.worldview.satisfaction = choices[winner]
        if winner != self.bubble_chamber.worldview.view:
            self.bubble_chamber.worldview.view = winner
            self.bubble_chamber.concepts["publish"].decay_activation(
                self.bubble_chamber.general_satisfaction
            )
            self.result = CodeletResult.FINISH
        else:
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

    def _calculate_satisfaction(self, view: View) -> FloatBetweenOneAndZero:
        if view is None:
            return 0.0
        correctness = self._calculate_correctness(view)
        completeness = self._calculate_completeness(view)
        conciseness = self._calculate_conciseness(view)
        cohesiveness = self._calculate_cohesiveness(view)
        satisfaction = sum(
            [
                self.CORRECTNESS_WEIGHT * correctness,
                self.COMPLETENESS_WEIGHT * completeness,
                self.CONCISENESS_WEIGHT * conciseness,
                self.COHESIVENESS_WEIGHT * cohesiveness,
            ]
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Calculating satisfaction for {view}\n"
            + f"Correctness: {correctness}\n"
            + f"Completeness: {completeness}\n"
            + f"Conciseness: {conciseness}\n"
            + f"Cohesiveness: {cohesiveness}\n"
            + f"Overall satisfaction: {satisfaction}"
        )
        return satisfaction

    def _calculate_correctness(self, view: View) -> FloatBetweenOneAndZero:
        return view.quality

    def _calculate_completeness(self, view: View) -> FloatBetweenOneAndZero:
        size_of_raw_input_in_views = len(
            self.bubble_chamber.new_set(
                *[
                    (raw_input_member, correspondence.conceptual_space)
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

    def _calculate_conciseness(self, view: View) -> FloatBetweenOneAndZero:
        if view.parent_frame.parent_concept.location_in_space(
            self.bubble_chamber.spaces["grammar"]
        ) != self.bubble_chamber.concepts["sentence"].location_in_space(
            self.bubble_chamber.spaces["grammar"]
        ):
            return 0
        return 1 + max([self._calculate_conciseness(v) for v in view.sub_views])

    def _calculate_cohesiveness(self, view: View) -> FloatBetweenOneAndZero:
        # TODO: this needs to be generalised for recursive cohesion views
        if view.parent_frame.cross_view_links.where(is_relation=True).is_empty:
            return 0.0
        space_one = (
            view.parent_frame.cross_view_links.where(is_relation=True)
            .get()
            .correspondences.get()
            .start.start.parent_space
        )
        view_one = view.sub_views.filter(
            lambda x: space_one in (x.parent_frame.input_space, x.output_space)
        ).get()
        view_two = view.sub_views.excluding(view_one).get()
        same_and_less_relations = StructureSet.union(
            view_one.parent_frame.input_space.contents, view_one.output_space.contents
        ).filter(
            lambda x: x.is_relation
            and x.is_cross_view
            and x.parent_concept
            in (
                self.bubble_chamber.concepts["same"],
                self.bubble_chamber.concepts["less"],
            )
            and (
                x.end in view_two.parent_frame.input_space.contents
                or x.end in view_two.output_space.contents
            )
        )
        conceptual_spaces = StructureSet.union(
            view_one.parent_frame.input_space.conceptual_spaces,
            view_one.output_space.conceptual_spaces,
            view_two.parent_frame.input_space.conceptual_spaces,
            view_two.output_space.conceptual_spaces,
        )
        relations_by_space = {
            space: same_and_less_relations.where(conceptual_space=space)
            for space in conceptual_spaces
        }
        relation_quality_by_space = {
            space: statistics.fmean([r.quality for r in relations])
            for space, relations in relations_by_space.items()
            if relations.not_empty
        }
        total_cohesion_quality = sum([q for s, q in relation_quality_by_space.items()])
        average_cohesion_quality = total_cohesion_quality / len(conceptual_spaces)
        return average_cohesion_quality
