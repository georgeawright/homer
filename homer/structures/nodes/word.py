from __future__ import annotations
from math import prod
import random
from typing import List, Union

from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node, Space
from homer.structures.spaces import ContextualSpace
from homer.word_form import WordForm

from .concept import Concept
from .lexeme import Lexeme


class Word(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        lexeme: Union[Lexeme, None],
        word_form: WordForm,
        locations: List[Location],
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        super_chunks: StructureCollection = None,
    ):
        Node.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            parent_space=parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.name = name
        self.lexeme = lexeme
        self.word_form = word_form
        self.is_word = True
        self.super_chunks = (
            super_chunks if super_chunks is not None else StructureCollection()
        )

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders import WordBuilder

        return WordBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators import WordEvaluator

        return WordEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors import WordSelector

        return WordSelector

    @property
    def is_slot(self):
        return self.name is None

    @property
    def is_abstract(self):
        return self.parent_space is None

    @property
    def concepts(self):
        return self.lexeme.concepts

    @property
    def unchunkedness(self):
        if self.is_abstract:
            return 0
        if len(self.super_chunks) == 0:
            return 1
        return 0.5 * prod([chunk.unchunkedness for chunk in self.super_chunks])

    @property
    def potential_rule_mates(self) -> StructureCollection:
        return StructureCollection.union(self.adjacent, self.super_phrases)

    @property
    def adjacent(self) -> StructureCollection:
        """return non-overlapping but touching phrases"""
        from .phrase import Phrase

        return StructureCollection.union(
            self.parent_space.contents.next_to(self.location).of_type(Word),
            self.parent_space.contents.next_to(self.location).of_type(Phrase),
        )

    @property
    def super_phrases(self) -> StructureCollection:
        """return phrases that contain this phrase"""
        from .phrase import Phrase

        return StructureCollection(
            {
                phrase
                for phrase in self.parent_space.contents.of_type(Phrase)
                if self in phrase.members
            }
        )

    @property
    def potential_labeling_words(self) -> StructureCollection:
        return StructureCollection.union(
            StructureCollection({self}),
            StructureCollection(
                {
                    relation.start
                    for relation in self.relations
                    if relation.parent_concept.name == "nsubj"
                }
            ),
            StructureCollection(
                {
                    relation.start
                    for relation in StructureCollection.union(
                        *[
                            r.start.relations
                            for r in self.relations
                            if r.parent_concept.name == "pobj"
                        ]
                    )
                    if relation.parent_concept.name == "prep"
                }
            ),
        )

    @property
    def potential_relating_words(self) -> StructureCollection:
        get_pobj_preds = lambda x: StructureCollection(
            {
                relation.start
                for relation in StructureCollection.union(
                    *[
                        r.start.relations
                        for r in x.relations
                        if r.parent_concept.name == "pobj"
                    ]
                )
                if relation.parent_concept.name == "prep"
            }
        )
        nsubj_preds = StructureCollection(
            {
                relation.start
                for relation in self.relations
                if relation.parent_concept.name == "nsubj"
            }
        )
        pobj_preds = get_pobj_preds(self)
        dep_preds = StructureCollection.union(
            *[
                get_pobj_preds(relation.start)
                for relation in self.relations
                if relation.parent_concept.name == "dep"
            ]
        )
        return StructureCollection.union(nsubj_preds, pobj_preds, dep_preds)

    @property
    def potential_argument_words(self) -> StructureCollection:
        nsubj_words = StructureCollection(
            {
                relation.end
                for relation in self.relations
                if relation.parent_concept.name == "nsubj"
            }
        )
        pobj_words = StructureCollection(
            {
                relation.end
                for relation in StructureCollection.union(
                    *[
                        r.end.relations
                        for r in self.relations
                        if r.parent_concept.name == "prep"
                    ]
                )
                if relation.parent_concept.name == "pobj"
            }
        )
        dep_words = StructureCollection(
            {
                relation.end
                for word in pobj_words
                for relation in word.relations
                if relation.parent_concept.name == "dep"
            }
        )
        return StructureCollection.union(nsubj_words, pobj_words, dep_words)

    def nearby(self, space: Space = None) -> StructureCollection:
        if space is not None:
            return StructureCollection.difference(
                space.contents.of_type(type(self)).near(self.location_in_space(space)),
                StructureCollection({self}),
            )
        return StructureCollection.difference(
            self.parent_space.contents.of_type(type(self)).near(
                self.location_in_space(self.parent_space)
            ),
            StructureCollection({self}),
        )

    def get_potential_relative(
        self, space: Space = None, concept: Concept = None
    ) -> Word:
        space = self.parent_space if space is None else space
        words = space.contents.where(is_word=True)
        if len(words) == 1:
            raise MissingStructureError
        for _ in range(len(words)):
            word = words.get(exclude=[self])
            if concept.location_in_space(concept.parent_space).end_is_near(
                word.location_in_conceptual_space(concept.parent_space)
            ):
                return word
        return words.get(exclude=[self])

    def copy(self, **kwargs: dict) -> Word:
        """Requires keyword arguments 'bubble_chamber', 'parent_id', and 'parent_space'."""
        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        parent_space = kwargs["parent_space"]
        locations = [
            Location(
                location.coordinates,
                location.space.conceptual_space.instance_in_space(parent_space),
            )
            for location in self.locations
            if not location.space.is_frame
        ] + [Location(self.location.coordinates, parent_space)]
        for location in locations:
            bubble_chamber.logger.log(location.space)
        new_word = Word(
            ID.new(Word),
            parent_id,
            name=self.name,
            lexeme=self.lexeme,
            word_form=self.word_form,
            locations=locations,
            parent_space=parent_space,
            quality=self.quality,
        )
        parent_space.add(new_word)
        bubble_chamber.logger.log(new_word)
        bubble_chamber.words.add(new_word)
        return new_word

    def copy_to_location(
        self, location: Location, parent_id: str = "", quality: float = 0.0
    ) -> Word:
        parent_space = location.space
        locations = [
            location
            for location in self.locations
            if location.space.is_conceptual_space
        ] + [location]
        new_word = Word(
            ID.new(Word),
            parent_id=parent_id,
            name=self.name,
            lexeme=self.lexeme,
            word_form=self.word_form,
            locations=locations,
            parent_space=location.space,
            quality=quality,
        )
        parent_space.add(new_word)
        return new_word

    def copy_with_contents(
        self,
        copies: dict,
        bubble_chamber: "BubbleChamber",
        parent_id: str,
        parent_space: ContextualSpace,
    ):
        new_locations = [
            location
            for location in self.locations
            if location.space.is_conceptual_space
        ]
        new_locations.append(
            Location(
                self.location_in_space(self.parent_space).coordinates, parent_space
            )
        )
        word_copy = Word(
            structure_id=ID.new(Word),
            parent_id=parent_id,
            name=self.name,
            lexeme=self.lexeme,
            word_form=self.word_form,
            locations=new_locations,
            parent_space=parent_space,
            quality=self.quality,
        )
        bubble_chamber.logger.log(word_copy)
        return (word_copy, copies)

    def __repr__(self) -> str:
        return (
            f'<{self.structure_id} "{self.name}" '
            + " in {self.parent_space.structure_id} {self.locations}>"
        )
