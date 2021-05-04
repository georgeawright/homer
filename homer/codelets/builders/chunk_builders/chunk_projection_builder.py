from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ChunkBuilder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence
from homer.structures.nodes import Chunk, Word


class ChunkProjectionBuilder(ChunkBuilder):
    """Builds a chunk in a new space with a correspondence to a node in another space.
    The chunk has no value or location coordinates."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_word: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        ChunkBuilder.__init__(
            self, codelet_id, parent_id, bubble_chamber, None, urgency
        )
        self.target_view = target_view
        self.target_word = target_word

    @classmethod
    def get_target_class(cls):
        return Chunk

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_word: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            target_word,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.monitoring_views.get_active()
        target_word = StructureCollection(
            {
                word
                for word in target_view.text_space.contents.where(is_word=True)
                if word.has_label(bubble_chamber.concepts["noun"])
            }
        ).get_unhappy()
        urgency = urgency if urgency is not None else target_word.unhappiness
        return cls.spawn(parent_id, bubble_chamber, target_view, target_word, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        return not self.target_word.has_correspondence_to_space(
            self.target_view.interpretation_space
        )

    def _calculate_confidence(self):
        self.confidence = 1.0

    def _process_structure(self):
        chunk = Chunk(
            structure_id=ID.new(Chunk),
            parent_id=self.codelet_id,
            value=None,
            locations=[Location([], self.target_view.interpretation_space)],
            members=StructureCollection(),
            parent_space=self.target_view.interpretation_space,
            quality=0.0,
        )
        self.target_view.interpretation_space.add(chunk)
        self.bubble_chamber.chunks.add(chunk)
        self.bubble_chamber.logger.log(chunk)
        start_space = self.target_word.parent_space
        end_space = self.target_view.interpretation_space
        correspondence = Correspondence(
            structure_id=ID.new(Correspondence),
            parent_id=self.codelet_id,
            start=self.target_word,
            end=chunk,
            start_space=start_space,
            end_space=end_space,
            locations=[self.target_word.location, chunk.location_in_space(end_space)],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.concepts["text"],
            parent_view=self.target_view,
            quality=0.0,
        )
        chunk.links_in.add(correspondence)
        chunk.links_out.add(correspondence)
        self.target_word.links_in.add(correspondence)
        self.target_word.links_out.add(correspondence)
        start_space.add(correspondence)
        end_space.add(correspondence)
        self.target_view.members.add(correspondence)
        self.bubble_chamber.correspondences.add(correspondence)
        self.bubble_chamber.logger.log(correspondence)
        self.bubble_chamber.logger.log(self.target_view)
        self.child_structures = StructureCollection({chunk, correspondence})

    def _fizzle(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )

    def _fail(self):
        self._fizzle()
