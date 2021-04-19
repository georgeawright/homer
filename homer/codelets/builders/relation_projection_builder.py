import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Space, View
from homer.structures.links import Correspondence, Relation
from homer.structures.nodes import Chunk, Concept, Word
from homer.tools import add_vectors, project_item_into_space


class RelationProjectionBuilder(Builder):
    """Builds a relation in a new space with a correspondence to a node in another space.
    Sets or alters the value or coordinates of its arguments
    according to the parent concept's prototype."""

    # target is a word with an adverb label in one space and the chunks in the target space
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_structure_one: Structure,
        target_word: Word,
        urgency: FloatBetweenOneAndZero,
        target_structure_two: Structure = None,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.target_view = target_view
        self.target_structure_one = target_structure_one
        self.target_structure_two = target_structure_two
        self.target_word = target_word
        self.parent_concept = None
        self.conceptual_space = None
        self.target_space = None
        self.child_structure = None

    @classmethod
    def get_target_class(cls):
        return Relation

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_view: View,
        target_structure_one: Structure,
        target_word: Word,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_view,
            target_structure_one,
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
        target_chunk = target_view.interpretation_space.contents.of_type(
            Chunk
        ).get_unhappy()
        potential_relating_words = (
            target_chunk.correspondences_to_space(target_view.text_space)
            .get_random()
            .arguments.get_random(exclude=[target_chunk])
            .potential_relating_words
        )
        target_word = StructureCollection(
            {
                word
                for word in potential_relating_words
                if not word.has_correspondence_to_space(
                    target_view.interpretation_space
                )
            }
        ).get_unhappy()
        urgency = (
            urgency
            if urgency is not None
            else statistics.fmean([target_chunk.unlinkedness, target_word.unlinkedness])
        )
        return cls.spawn(
            parent_id, bubble_chamber, target_view, target_chunk, target_word, urgency
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        self.conceptual_space = (
            self.target_word.lexeme.concepts.get_random()
            .parent_spaces.where(no_of_dimensions=1)
            .get_random()
        )
        self.parent_concept = (
            self.bubble_chamber.spaces["relational concepts"]
            .contents.of_type(Space)
            .get_random()
            .contents.of_type(Concept)
            .get_random()
        )
        self.target_space = self.conceptual_space.instance_in_space(
            self.target_view.interpretation_space
        )
        target_structure_one_corresponding_word = (
            self.target_structure_one.correspondences_to_space(
                self.target_view.text_space
            )
            .get_random()
            .arguments.get_random(exclude=[self.target_structure_one])
        )
        if self.target_structure_two is None:
            try:
                target_structure_two_corresponding_word = (
                    self.target_word.potential_argument_words().get_exigent(
                        exclude=[target_structure_one_corresponding_word]
                    )
                )
                self.target_structure_two = (
                    target_structure_two_corresponding_word.correspondences_to_space(
                        self.target_view.interpretation_space
                    )
                    .get_random()
                    .arguments.get_random(
                        exclude=[target_structure_two_corresponding_word]
                    )
                )
            except MissingStructureError:
                return False
        return not self.target_structure_one.has_relation(
            self.target_space,
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
        ) and not self.target_word.has_correspondence_to_space(
            self.target_view.interpretation_space
        )

    def _calculate_confidence(self):
        target_word_concept = self.target_word.lexeme.concepts.get_random()
        self.confidence = (
            target_word_concept.relations_with(self.parent_concept)
            .get_random()
            .activation
        )

    def _process_structure(self):
        self.bubble_chamber.logger.log(self.target_space)
        if self.target_structure_one not in self.target_space.contents:
            project_item_into_space(self.target_structure_one, self.target_space)
        if self.target_structure_two not in self.target_space.contents:
            project_item_into_space(self.target_structure_two, self.target_space)
        if self.target_space.relevant_value == "value":
            self.target_structure_one.value = self.target_space.parent_concept.value
            self.target_structure_two.value = add_vectors(
                self.target_structure_one.value, self.parent_concept.value
            )
        if self.target_space.relevant_value == "coordinates":
            self.target_structure_one.location_in_space(
                self.target_space
            ).coordinates = self.target_space.parent_concept.location_in_space(
                self.conceptual_space
            ).coordinates
            self.target_structure_two.location_in_space(
                self.target_space
            ).coordinates = add_vectors(
                self.target_space.parent_concept.location_in_space(
                    self.conceptual_space
                ).coordinates,
                self.parent_concept.value,
            )
        relation = Relation(
            structure_id=ID.new(Relation),
            parent_id=self.codelet_id,
            start=self.target_structure_one,
            end=self.target_structure_two,
            parent_concept=self.parent_concept,
            parent_space=self.target_space,
            quality=0,
        )
        self.child_structure = relation
        self.target_structure_one.links_out.add(relation)
        self.target_structure_two.links_in.add(relation)
        start_space = self.target_word.parent_space
        end_space = self.target_space
        correspondence = Correspondence(
            structure_id=ID.new(Correspondence),
            parent_id=self.codelet_id,
            start=self.target_word,
            end=relation,
            start_space=start_space,
            end_space=end_space,
            locations=[self.target_word.location, relation.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.conceptual_space,
            parent_view=self.target_view,
            quality=0,
        )
        relation.links_out.add(correspondence)
        relation.links_in.add(correspondence)
        self.target_word.links_out.add(correspondence)
        self.target_word.links_in.add(correspondence)
        start_space.add(correspondence)
        end_space.add(correspondence)
        self.target_view.members.add(correspondence)
        self.bubble_chamber.correspondences.add(correspondence)
        self.bubble_chamber.logger.log(correspondence)
        self.bubble_chamber.logger.log(self.target_view)

    def _fizzle(self):
        self._re_engender()

    def _fail(self):
        self._re_engender()

    def _re_engender(self):
        self.child_codelets.append(
            self.make(self.codelet_id, self.bubble_chamber, urgency=self.urgency / 2)
        )
