from __future__ import annotations

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Lexeme, Space


class Word(Chunk):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        value: str,
        lexeme: Lexeme,
        location: Location,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        members: StructureCollection = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Chunk.__init__(
            self,
            structure_id,
            parent_id,
            value,
            [location],
            members,
            parent_space,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.lexeme = lexeme

    @property
    def concepts(self):
        from .slot import Slot

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
