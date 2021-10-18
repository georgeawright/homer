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
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
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
            parent_spaces=parent_spaces,
        )
        self.headword = headword
        self.word_forms = word_forms
        self.is_lexeme = True

    @property
    def concepts(self) -> StructureCollection:
        return self.relatives.where(is_concept=True)

    def get_form(self, form: WordForm) -> str:
        return self.word_forms[form]

    def __repr__(self) -> str:
        return f"<{self.structure_id} {self.headword}>"
