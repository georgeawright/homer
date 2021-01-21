from homer.float_between_one_and_zero import FloatBetweenOneAndZero
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
