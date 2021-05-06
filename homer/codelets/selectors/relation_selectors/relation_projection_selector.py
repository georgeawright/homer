import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders.relation_builders import RelationProjectionBuilder
from homer.codelets.selectors import RelationSelector
from homer.structure_collection import StructureCollection


class RelationProjectionSelector(RelationSelector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        target_view = bubble_chamber.monitoring_views.get_active()
        target_relation = target_view.interpretation_space.contents.where(
            is_relation=True
        ).get_random()
        target_correspondence = target_relation.correspondences_to_space(
            target_view.text_space
        ).get_random()
        target_structures = StructureCollection(
            {target_relation, target_correspondence}
        )
        urgency = statistics.fmean(
            [structure.activation for structure in target_structures]
        )
        return cls.spawn(parent_id, bubble_chamber, target_structures, urgency)

    def _passes_preliminary_checks(self):
        return True

    def _fizzle(self):
        raise NotImplementedError

    def _engender_follow_up(self):
        self.child_codelets.append(
            RelationProjectionBuilder.make(
                self.codelet_id,
                self.bubble_chamber,
            )
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )
