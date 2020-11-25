from __future__ import annotations
import statistics

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Concept
from homer.structures.chunks import View
from homer.structures.links import Correspondence
from homer.structures.spaces import WorkingSpace

from .view_enlarger import ViewEnlarger


class ViewBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_correspondence: Correspondence,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
        self.target_correspondence = target_correspondence
        self.second_target_correspondence = None
        self.third_target_correspondence = None
        self.correspondences = []
        self.confidence = 0.0
        self.child_structure = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_correspondence: Correspondence,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_correspondence,
            urgency,
        )

    def _passes_preliminary_checks(self):
        try:
            self.second_target_correspondence = (
                self.target_correspondence.nearby().get_random()
            )
        except MissingStructureError:
            return False
        return not self.bubble_chamber.has_view(
            StructureCollection(
                {self.target_correspondence, self.second_target_correspondence}
            )
        )

    def _calculate_confidence(self):
        common_arguments = self.target_correspondence.common_arguments_with(
            self.second_target_correspondence
        )
        if len(common_arguments) == 1:
            third_target_start = (
                self.target_correspondence.start
                if self.target_correspondence.start != common_arguments.get_random()
                else self.target_correspondence.end
            )
            third_target_end = (
                self.second_target_correspondence.end
                if self.second_target_correspondence.end
                != common_arguments.get_random()
                else self.second_target_correspondence.start
            )
            try:
                self.third_target_correspondence = (
                    third_target_start.correspondences_with(
                        third_target_end
                    ).get_most_active()
                )
                self.confidence = min(
                    self.target_correspondence.quality,
                    self.second_target_correspondence.quality,
                    self.third_target_quality,
                )  # you are only as strong as your weakest link
                self.correspondences = StructureCollection(
                    {
                        self.target_correspondence,
                        self.second_target_correspondence,
                        self.third_target_correspondence,
                    }
                )
            except MissingStructureError:
                self.confidence = 0.0
                return
        elif len(common_arguments) == 0:
            self.confidence = min(
                self.target_correspondence.quality,
                self.second_target_correspondence.quality,
            )
            self.correspondences = StructureCollection(
                {
                    self.target_correspondence,
                    self.second_target_correspondence,
                }
            )
        else:  # if there are 2 common arguments, the correspondences are equivalent/competing
            self.confidence = 0.0

    def _boost_activations(self):
        pass

    def _process_structure(self):
        view_output_space = WorkingSpace(
            ID.new(WorkingSpace),
            self.codelet_id,
            self.codelet_id,
            StructureCollection(),
            0.0,
            self.bubble_chamber.concepts["text"],
        )
        view = View(
            ID.new(View),
            self.codelet_id,
            self.correspondences,
            self.bubble_chamber.spaces["top level working"],
            view_output_space,
            self.confidence,
        )
        self.bubble_chamber.views.add(view)
        self.bubble_chamber.spaces.add(view_output_space)
        self.child_structure = view

    def _engender_follow_up(self):
        self.child_codelets.append(
            ViewEnlarger.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.child_structure,
                self.confidence,
            )
        )

    def _fizzle(self):
        new_target = self.bubble_chamber.correspondences.get_unhappy()
        self.child_codelets.append(
            ViewBuilder.spawn(
                self.codelet_id, self.bubble_chamber, new_target, new_target.unhappiness
            )
        )

    def _fail(self):
        new_target = self.bubble_chamber.correspondences.get_unhappy()
        self.child_codelets.append(
            ViewBuilder.spawn(
                self.codelet_id, self.bubble_chamber, new_target, new_target.unhappiness
            )
        )
