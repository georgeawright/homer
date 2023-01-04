from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection_keys import (
    activation,
    exigency,
    uncorrespondedness,
)
from linguoplotter.structures.nodes import Concept


class InterspatialCorrespondenceSuggester(CorrespondenceSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.correspondence_builders import (
            InterspatialCorrespondenceBuilder,
        )

        return InterspatialCorrespondenceBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.views.get(key=exigency)
        end = target_view.unfilled_interspatial_structures.get(key=uncorrespondedness)
        urgency = urgency if urgency is not None else end.uncorrespondedness
        targets = bubble_chamber.new_dict(
            {"target_view": target_view, "end": end}, name="targets"
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.views.get(key=activation)
        end = target_view.unfilled_interspatial_structures.get(key=uncorrespondedness)
        urgency = urgency if urgency is not None else end.uncorrespondedness
        targets = bubble_chamber.new_dict(
            {"target_view": target_view, "end": end, "concept": concept},
            name="targets",
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            targets,
            urgency,
        )

    def _passes_preliminary_checks(self):
        self._get_target_conceptual_space(self, self)
        if (
            self.targets["start"] is not None
            and self.targets["concept"] is not None
            and not (
                self.targets["view"].members.is_empty
                and self.targets["view"].super_views.is_empty
            )
        ):
            if self.targets["space"] is not None and self.targets["space"].is_slot:
                classification_space = self.targets["start"].conceptual_space
            else:
                classification_space = self.targets["space"]
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=classification_space,
                start=self.targets["start"],
                end=self.targets["end"],
                view=self.targets["view"],
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Preliminary classification: {classification}"
            )
            if classification < 0.5:
                self.targets["concept"] = self.bubble_chamber.new_compound_concept(
                    self.bubble_chamber.concepts["not"], [self.targets["concept"]]
                )
        else:
            self.targets["concept"] = self.bubble_chamber.concepts["same"]
        try:
            if self.targets["start"] is None:
                self._get_target_structure_one(self, self)
        except MissingStructureError:
            self.bubble_chamber.loggers["activity"].log(
                "MissingStructureError when searching for input target space and structure",
            )
            return False
        if not self.targets["view"].can_accept_member(
            self.targets["concept"],
            self.targets["space"],
            self.targets["start"],
            self.targets["end"],
        ):
            self.bubble_chamber.loggers["activity"].log(
                "Target view cannot accept suggested member."
            )
            return False
        return True

    def _fizzle(self):
        pass

    @staticmethod
    def _get_target_structure_one(parent_codelet, child_codelet):
        bubble_chamber = parent_codelet.bubble_chamber
        source_collection = bubble_chamber.interspatial_relations
        if (
            child_codelet.targets["end"].start
            in child_codelet.targets["view"].grouped_nodes
        ):
            start_node_group = [
                group
                for group in child_codelet.targets["view"].node_groups
                if child_codelet.targets["end"].start in group.values()
            ][0]
            try:
                structure_one_start = start_node_group[None]
            except KeyError:
                bubble_chamber.loggers["activity"].log(
                    "Start node group has no member in target space one",
                )
                structure_one_start = None
        else:
            bubble_chamber.loggers["activity"].log(
                "Structure two start not in grouped nodes"
            )
            structure_one_start = None
        if (
            child_codelet.targets["end"].end
            in child_codelet.targets["view"].grouped_nodes
        ):
            end_node_group = [
                group
                for group in child_codelet.targets["view"].node_groups
                if child_codelet.targets["end"].end in group.values()
            ][0]
            try:
                structure_one_end = end_node_group[None]
            except KeyError:
                bubble_chamber.loggers["activity"].log(
                    "End node group has no member in target space one"
                )
                structure_one_end = None
        else:
            bubble_chamber.loggers["activity"].log(
                "Structure two end not in grouped nodes"
            )
            structure_one_end = None
        matching_relations = source_collection.filter(
            lambda x: x.is_relation
            and x.quality * x.activation > 0
            and (x.start == structure_one_start or structure_one_start is None)
            and (x.end == structure_one_end or structure_one_end is None)
            and any(
                [
                    x.parent_concept == child_codelet.targets["end"].parent_concept,
                    child_codelet.targets["end"].parent_concept.is_slot,
                    (
                        x.parent_concept.is_compound_concept
                        and x.parent_concept.args[0]
                        == child_codelet.targets["end"].parent_concept
                    ),
                ]
            )
            and child_codelet.targets["end"].parent_concept.parent_space.subsumes(
                x.parent_concept.parent_space
            )
            and child_codelet.targets["space"].subsumes(x.conceptual_space)
            and (
                x.parent_concept
                in child_codelet.targets["end"].parent_concept.possible_instances
                if child_codelet.targets[
                    "end"
                ].parent_concept.possible_instances.not_empty
                else True
            )
        )
        bubble_chamber.loggers["activity"].log_set(
            matching_relations, "matching input relations"
        )
        child_codelet.targets["start"] = matching_relations.get(
            key=lambda x: x.quality * x.activation * x.uncorrespondedness
        )
        for view in bubble_chamber.views:
            if (
                child_codelet.targets["start"].start
                in view.parent_frame.input_space.contents
                or child_codelet.targets["start"].start
                in view.parent_frame.output_space.contents
            ):
                child_codelet.targets["start_sub_view"] = view
            if (
                child_codelet.targets["start"].end
                in view.parent_frame.input_space.contents
                or child_codelet.targets["start"].end
                in view.parent_frame.output_space.contents
            ):
                child_codelet.targets["end_sub_view"] = view
        for sub_frame in child_codelet.targets["view"].parent_frame.sub_frames:
            if (
                child_codelet.targets["end"].start in sub_frame.input_space.contents
                or child_codelet.targets["end"].start in sub_frame.input_space.contents
            ):
                child_codelet.targets["start_sub_frame"] = sub_frame
            if (
                child_codelet.targets["end"].end in sub_frame.input_space.contents
                or child_codelet.targets["end"].end in sub_frame.input_space.contents
            ):
                child_codelet.targets["end_sub_frame"] = sub_frame
