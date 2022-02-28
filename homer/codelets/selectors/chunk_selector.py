from homer.codelets.selector import Selector
from homer.codelets.suggesters import ChunkSuggester
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation, chunking_exigency


class ChunkSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_chunk = self.champions.where(is_chunk=True, is_slot=False).get()
            self.bubble_chamber.loggers["activity"].log(
                self, f"Champion chunk: {champion_chunk}"
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Nearby champion chunk: {champion_chunk.nearby()}"
            )
            challenger_chunk = champion_chunk.nearby().get(key=activation)
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_chunk
            )
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
        try:
            new_target = self.winners.where(is_slot=True).get()
            target_space = new_target.parent_space
            target_rule = None
        except MissingStructureError:
            winning_chunk = self.winners.where(is_slot=False).get()
            target_space = winning_chunk.parent_space
            new_target = target_space.contents.where(is_chunk=True).get(
                key=chunking_exigency
            )
            target_rule = winning_chunk.rule.friends.get(key=activation)
        self.child_codelets = [
            ChunkSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_space": target_space,
                    "target_node": new_target,
                    "target_rule": target_rule,
                },
                new_target.activation,
            ),
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            ),
        ]
