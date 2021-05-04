from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structures import Node
from homer.structures.links import Correspondence


class CorrespondenceSelector(Selector):
    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        champion = bubble_chamber.correspondences.where(
            is_privileged=False
        ).get_active()
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({champion}),
            champion.activation,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_correspondence = self.champions.get_random()
        candidates = champion_correspondence.start.correspondences_to_space(
            champion_correspondence.end_space
        )
        if len(candidates) > 1:
            challenger_correspondence = candidates.get_active(
                exclude=[champion_correspondence]
            )
            self.challengers = StructureCollection({challenger_correspondence})
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        winner_correspondence = self.winners.get_random()
        try:
            if isinstance(winner_correspondence.start, Node):
                new_target = winner_correspondence.start.links.not_of_type(
                    Correspondence
                ).get_random()
            else:
                new_target = (
                    winner_correspondence.start.arguments.get_random()
                    .links.not_of_type(Correspondence)
                    .get_random()
                )
            new_target_space = new_target.parent_space
        except MissingStructureError:
            return
        self.child_codelets.append(
            CorrespondenceBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                winner_correspondence.parent_view,
                new_target_space,
                new_target,
                new_target.unlinkedness,
                parent_concept=winner_correspondence.parent_concept,
            )
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.losers,
            )
        )
