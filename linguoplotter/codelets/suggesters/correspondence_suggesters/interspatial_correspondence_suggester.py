from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import CorrespondenceSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collection_keys import (
    activation,
    exigency,
    uncorrespondedness,
)
from linguoplotter.structure_collections import StructureSet
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
        target_start_space = None
        target_end_space = None
        for link in child_codelet.targets["view"].parent_frame.interspatial_links:
            for correspondee in link.correspondees:
                if (
                    link.start.parent_space
                    == child_codelet.targets["end"].start.parent_space
                ):
                    target_start_space = correspondee.start.parent_space
                if (
                    link.is_relation
                    and link.end.parent_space
                    == child_codelet.targets["end"].start.parent_space
                ):
                    target_start_space = correspondee.end.parent_space
                if (
                    child_codelet.targets["end"].is_relation
                    and link.start.parent_space
                    == child_codelet.targets["end"].end.parent_space
                ):
                    target_end_space = correspondee.start.parent_space
                if (
                    link.is_relation
                    and child_codelet.targets["end"].is_relation
                    and link.end.parent_space
                    == child_codelet.targets["end"].end.parent_space
                ):
                    target_end_space = correspondee.end.parent_space
        for sub_frame in child_codelet.targets["view"].parent_frame.sub_frames:
            if (
                child_codelet.targets["end"].start in sub_frame.input_space.contents
                or child_codelet.targets["end"].start in sub_frame.output_space.contents
            ):
                start_sub_frame = sub_frame
            if child_codelet.targets["end"].is_relation and (
                child_codelet.targets["end"].end in sub_frame.input_space.contents
                or child_codelet.targets["end"].end in sub_frame.output_space.contents
            ):
                end_sub_frame = sub_frame
        if target_start_space is None:
            potential_start_views = bubble_chamber.views.filter(
                lambda x: x.parent_frame.parent_concept
                == start_sub_frame.parent_concept
            )
            potential_start_views = potential_start_views.sample(
                len(potential_start_views) // 2
            )
        else:
            potential_start_views = child_codelet.targets["view"].sub_views.filter(
                lambda x: target_start_space
                in [x.parent_frame.input_space, x.parent_frame.output_space]
            )
        if potential_start_views.is_empty:
            raise MissingStructureError
        potential_start_targets = StructureSet.union(
            *[
                view.output_space.contents.filter(
                    lambda x: x.is_letter_chunk and x.members.is_empty
                )
                if child_codelet.targets["end"]
                in child_codelet.targets["view"].parent_frame.output_space.contents
                else view.parent_frame.input_space.contents.filter(
                    lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                )
                for view in potential_start_views
            ]
        )
        if target_end_space is None:
            potential_end_views = bubble_chamber.views.filter(
                lambda x: x.parent_frame.parent_concept == end_sub_frame.parent_concept
                and x not in potential_start_views
            )
        else:
            potential_end_views = child_codelet.targets["view"].sub_views.filter(
                lambda x: target_end_space
                in [x.parent_frame.input_space, x.parent_frame.output_space]
            )
        if potential_end_views.is_empty:
            raise MissingStructureError
        potential_end_targets = StructureSet.union(
            *[
                view.output_space.contents.filter(
                    lambda x: x.is_letter_chunk and x.members.is_empty
                )
                if child_codelet.targets["end"]
                in child_codelet.targets["view"].parent_frame.output_space.contents
                else view.parent_frame.input_space.contents.filter(
                    lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                )
                for view in potential_end_views
            ]
        )
        if child_codelet.targets["end"].is_label:
            matching_labels = source_collection.filter(
                lambda x: x.is_label
                and x.is_interspatial
                and x.quality * x.activation > 0
                and x.start in potential_start_targets
                and x.parent_concept == child_codelet.targets["end"].parent_concept
                and x.parent_spaces.where(is_conceptual_space=True)
                == child_codelet.targets["end"].parent_spaces.where(
                    is_conceptual_space=True
                )
            )
            bubble_chamber.loggers["activity"].log_set(
                matching_labels, "matching input labels"
            )
            child_codelet.targets["start"] = matching_labels.get(
                key=lambda x: x.quality * x.activation * x.uncorrespondedness
            )
        elif child_codelet.targets["end"].is_relation:
            matching_relations = source_collection.filter(
                lambda x: x.is_relation
                and x.quality * x.activation > 0
                and x.start in potential_start_targets
                and x.end in potential_end_targets
                and any(
                    [
                        x.parent_concept == child_codelet.targets["end"].parent_concept,
                        child_codelet.targets["end"].parent_concept.is_slot,
                        (
                            x.parent_concept.is_compound_concept
                            and x.parent_concept.args[0]
                            == child_codelet.targets["end"].parent_concept
                        )
                        and child_codelet.targets["view"].members.not_empty,
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
