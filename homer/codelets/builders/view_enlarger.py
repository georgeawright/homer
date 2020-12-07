from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structures import Concept
from homer.structures.chunks import View
from homer.structures.links import Correspondence


class ViewEnlarger(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        urgency: float,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_view
        self.candidate_member = None
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

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        try:
            self.candidate_member = self.target_view.nearby().get_random()
        except MissingStructureError:
            return False
        return not self.bubble_chamber.has_view(
            StructureCollection.union(
                self.target_view.members,
                StructureCollection({self.candidate_member}),
            )
        )

    def _calculate_confidence(self):
        confidence = float("inf")
        self.correspondences_to_add = {self.candidate_member}
        for correspondence in self.target_view.members:
            (
                new_confidence,
                third_correspondence,
            ) = self._calculate_confidence_based_on_single_correspondence(
                correspondence
            )
            if new_confidence < confidence:
                confidence = new_confidence
            self.correspondences_to_add.add(third_correspondence)
        self.confidence = confidence

    def _calculate_confidence_based_on_single_correspondence(
        self, correspondence: Correspondence
    ):
        common_arguments = correspondence.common_arguments_with(self.candidate_member)
        if len(common_arguments) == 1:
            third_target_start = (
                correspondence.start
                if correspondence.start != common_arguments.get_random()
                else correspondence.end
            )
            third_target_end = (
                self.candidate_member.end
                if self.candidate_member.end != common_arguments.get_random()
                else self.candidate_member.start
            )
            try:
                third_correspondence = third_target_start.correspondences_with(
                    third_target_end
                ).get_most_active()
                confidence = min(
                    correspondence.quality,
                    self.candidate_member.quality,
                    third_correspondence.quality,
                )  # you are only as strong as your weakest link
                return (confidence, third_correspondence)
            except MissingStructureError:
                return (0.0, None)
        elif len(common_arguments) == 0:
            confidence = min(
                correspondence.quality,
                self.candidate_member.quality,
            )
            return (confidence, None)
        else:  # if there are 2 common arguments, the correspondences are equivalent/competing
            return (0.0, None)

    def _process_structure(self):
        self.target_view.members.add(self.candidate_member)

    def _engender_follow_up(self):
        self.child_codelets.append(
            ViewEnlarger.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_view,
                self.confidence,
            )
        )

    def _fizzle(self):
        self.child_codelets.append(
            ViewEnlarger.spawn(
                self.codelet_id, self.bubble_chamber, self.target_view, self.urgency / 2
            )
        )

    def _fail(self):
        self.child_codelets.append(
            ViewEnlarger.spawn(
                self.codelet_id, self.bubble_chamber, self.target_view, self.urgency / 2
            )
        )
