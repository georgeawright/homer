from linguoplotter.codelets.selector import Selector
from linguoplotter.codelets.suggesters import ChunkSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import activation
from linguoplotter.structure_collections import StructureSet


class ChunkSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        if self.challengers.not_empty:
            return True
        try:
            champion = self.champions.get()
            self.challengers.add(
                StructureSet.union(champion.sub_chunks, champion.super_chunks)
                .where(is_raw=False)
                .get(key=activation)
            )
        except MissingStructureError:
            pass
        return True

    def _fizzle(self):
        self.child_codelets.append(
            ChunkSuggester.make(self.codelet_id, self.bubble_chamber)
        )

    def _engender_follow_up(self):
        try:
            winning_chunk = self.winners.get()
            targets = self.bubble_chamber.new_dict(
                {"node_one": winning_chunk}, name="targets"
            )
            self.child_codelets.append(
                ChunkSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    winning_chunk.chunking_exigency,
                ),
            )
        except MissingStructureError:
            pass
