from homer.codelets.selector import Selector
from homer.codelets.suggesters import ChunkSuggester
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation


class ChunkSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_chunk = self.champions.get()
            challenger_chunk = champion_chunk.nearby().get(key=activation)
            self.challengers = StructureCollection({challenger_chunk})
        except MissingStructureError:
            return True
        members_intersection = StructureCollection.intersection(
            champion_chunk.members, challenger_chunk.members
        )
        if not (
            len(members_intersection) > 0.5 * len(champion_chunk.members)
            and len(members_intersection) > 0.5 * len(challenger_chunk.members)
        ):
            self.challengers = None
        return True

    def _fizzle(self):
        self.child_codelets.append(
            ChunkSuggester.make(self.codelet_id, self.bubble_chamber)
        )

    def _engender_follow_up(self):
        new_target = self.winners.get()
        self.child_codelets.append(
            ChunkSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {"target_one": new_target},
                new_target.activation,
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
