from typing import Dict, List

from homer.id import ID
from homer.word_form import WordForm
from homer.structure_collection import StructureCollection
from homer.structures import Node

from .concept import Concept


class Lexeme(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        headword: str,
        forms: Dict[WordForm, str],
        parts_of_speech: Dict[WordForm, List[Concept]],
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
        self.forms = forms
        self.parts_of_speech = parts_of_speech

    @property
    def concepts(self) -> StructureCollection:
        return StructureCollection(
            {link.start for link in self.links_in if isinstance(link.start, Concept)}
        )

    @property
    def syntactic_concepts(self) -> StructureCollection:
        return StructureCollection(
            {
                concept
                for concept in self.concepts
                if concept.parent_space.name == "grammar"
                or concept.parent_space.name == "dependency"
            }
        )

    @property
    def semantic_concepts(self) -> StructureCollection:
        return StructureCollection.difference(self.concepts, self.syntactic_concepts)

    def get_form(self, form: WordForm) -> str:
        return self.forms[form]

    def __repr__(self) -> str:
        return f"<{self.structure_id} {self.headword}>"
