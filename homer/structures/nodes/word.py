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
        return self.value is None

    @property
    def concepts(self):
        return self.lexeme.concepts if self.lexeme is not None else None

    def copy(
        self,
        bubble_chamber: "BubbleChamber",
        parent_id: str = "",
        parent_space: Space = None,
    ) -> Word:
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
