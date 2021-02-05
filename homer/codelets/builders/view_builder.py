from __future__ import annotations
from typing import List, Set, Tuple

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.chunks import View
from homer.structures.links import Correspondence
from homer.structures.spaces import WorkingSpace


class ViewBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_view
        self.second_target_view = None
        self.correspondences = None
        self.correspondences_to_add = None
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            urgency,
        )

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target = bubble_chamber.views.get_exigent()
        return cls.spawn(parent_id, bubble_chamber, target, target.unhappiness)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        try:
            self.second_target_view = self.target_view.nearby().get_random()
        except MissingStructureError:
            return False
        return not self.bubble_chamber.has_view(
            StructureCollection.union(
                self.target_view.members, self.second_target_view.members
            )
        )

    def _calculate_confidence(self):
        self.confidence = 1.0
        self.correspondences = self.target_view.members.copy()
        self.correspondences_to_add = self.second_target_view.members.copy()
        while not self.correspondences_to_add.is_empty():
            new = self.correspondences_to_add.pop()
            for old in self.target_view.members:
                common_arguments = StructureCollection.intersection(
                    old.arguments, new.arguments
                )
                if len(common_arguments) == 0:
                    self.confidence = min(self.confidence, old.quality, new.quality)
                    self.correspondences.add(new)
                elif len(common_arguments) == 1:
                    all_arguments = StructureCollection.union(
                        old.arguments, new.arguments
                    )
                    distinct_arguments = StructureCollection.difference(
                        all_arguments, common_arguments
                    )
                    try:
                        third = self.second_target_view.members.where(
                            arguments=distinct_arguments
                        ).get_random()
                        self.confidence = min(
                            self.confidence, old.quality, new.quality, third.quality
                        )
                        self.correspondences_to_add.add(third)
                        self.correspondences.add(new)
                    except MissingStructureError:
                        self.confidence = 0
                        return
                else:  # 2 common arguments means equivalent/incompatible correspondences
                    self.confidence = 0
                    return

    def _process_structure(self):
        view = View.new(
            bubble_chamber=self.bubble_chamber,
            parent_id=self.codelet_id,
            members=self.correspondences,
        )
        self.bubble_chamber.logger.log(view)
        self.child_structure = view

    def _engender_follow_up(self):
        from homer.codelets.evaluators import ViewEvaluator

        self.child_codelets.append(
            ViewEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structure,
                self.confidence,
            )
        )

    def _fizzle(self):
        from homer.codelets.builders import CorrespondenceBuilder

        self.child_codelets.append(
            CorrespondenceBuilder.make(self.codelet_id, self.bubble_chamber)
        )

    def _fail(self):
        self.child_codelets.append(self.make(self.codelet_id, self.bubble_chamber))
