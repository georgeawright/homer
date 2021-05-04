from __future__ import annotations
from typing import Union

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node, Space
from homer.word_form import WordForm

from .lexeme import Lexeme


class Word(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        lexeme: Union[Lexeme, None],
        word_form: WordForm,
        location: Location,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        value = lexeme.forms[word_form] if lexeme is not None else None
        Node.__init__(
            self,
            structure_id,
            parent_id,
            value=value,
            locations=[location],
            parent_space=parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.lexeme = lexeme
        self.word_form = word_form
        self.is_word = True

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
    def concepts(self):
        return self.lexeme.concepts

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

    def copy(self, **kwargs: dict) -> Word:
        """Requires keyword arguments 'bubble_chamber', 'parent_id', and 'parent_space'."""
        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        parent_space = kwargs["parent_space"]
        location = Location(self.location.coordinates, parent_space)
        new_word = Word(
            ID.new(Word),
            parent_id,
            self.value,
            self.lexeme,
            location,
            parent_space,
            self.quality,
        )
        bubble_chamber.words.add(new_word)
        return new_word
