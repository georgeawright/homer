from linguoplotter.codelets.selector import Selector
from linguoplotter.codelets.evaluators import ChunkEvaluator
from linguoplotter.codelets.suggesters import ChunkSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structure_collection_keys import activation


class ChunkSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_chunk = self.champions.where(is_chunk=True).get()
            self.bubble_chamber.loggers["activity"].log(
                self, f"Champion chunk: {champion_chunk}"
            )
            challenger_chunk = (
                champion_chunk.nearby()
                .filter(
                    lambda x: len(
                        StructureCollection.intersection(
                            champion_chunk.members, x.members
                        )
                    )
                    > 0.5 * len(champion_chunk.members)
                    and len(
                        StructureCollection.intersection(
                            champion_chunk.members, x.members
                        )
                    )
                    > 0.5 * len(x.members)
                )
                .get(key=activation)
            )
            self.challengers = self.bubble_chamber.new_structure_collection(
                challenger_chunk
            )
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found challenger: {challenger_chunk}"
            )
        except MissingStructureError:
            pass
        return True

    def _fizzle(self):
        self.child_codelets.append(
            ChunkSuggester.make(self.codelet_id, self.bubble_chamber)
        )

    def _engender_follow_up(self):
        winning_chunk = self.winners.get()
        self.child_codelets = [
            ChunkSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_structure_one": winning_chunk,
                },
                winning_chunk.chunking_exigency,
            ),
            ChunkEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            ),
        ]
