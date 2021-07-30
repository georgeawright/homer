from typing import Dict, List

from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Node
from homer.word_form import WordForm

from .concept import Concept


class Lexeme(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        headword: str,
        word_forms: dict,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Node.__init__(
            self,
            structure_id,
            parent_id,
            locations=[],
            parent_space=None,
            quality=None,
            links_in=links_in,
            links_out=links_out,
        )
        self.headword = headword
        self.word_forms = word_forms

    @property
    def concepts(self) -> StructureCollection:
        return StructureCollection(
            {link.start for link in self.links_in if isinstance(link.start, Concept)}
        )

    def get_form(self, form: WordForm) -> str:
        return self.word_forms[form]

    def __repr__(self) -> str:
        return f"<{self.structure_id} {self.headword}>"
