from homer.bubble_chamber import BubbleChamber
from homer.codelets import Factory
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure import Structure
from homer.structure_collection_keys import exigency


class ViewDrivenFactory(Factory):
    """Finds a view with unfilled slots
    and spawns a codelet to suggest a structure that could fill a slot"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Factory.__init__(self, codelet_id, parent_id, bubble_chamber, coderack, urgency)

    def follow_up_satisfaction(self) -> FloatBetweenOneAndZero:
        return 1 - self.bubble_chamber.satisfaction

    def _engender_follow_up(self):
        view = self.bubble_chamber.production_views.get(key=exigency)
        slot = view.slots.where(is_unfilled=True)
        follow_up_class = self._get_follow_up_class(slot)
        rand = self.bubble_chamber.random_machine.generate_random_number()
        if self.coderack.proportion_of_codelets_of_type(follow_up_class) < rand:
            follow_up = follow_up_class.make(self.codelet_id, self.bubble_chamber)
            self.child_codelets.append(follow_up)

    def _get_follow_up_class(self, slot: Structure):
        action_concept = self.bubble_chamber.concepts["suggest"]
        space_concept = self.bubble_chamber.concepts["inner"]
        direction_concept = self.bubble_chamber.concepts["forward"]
        if slot.is_label:
            structure_concept = self.bubble_chamber.concepts["label"]
        elif slot.is_relation:
            structure_concept = self.bubble_chamber.concepts["relation"]
        elif slot.is_chunk:
            structure_concept = self.bubble_chamber.concepts["chunk"]
        elif slot.is_view:
            structure_concept = self.bubble_chamber.concepts["view-simplex"]
        return self._get_codelet_type_from_concepts(
            action=action_concept,
            space=space_concept,
            direction=direction_concept,
            structure=structure_concept,
        )
