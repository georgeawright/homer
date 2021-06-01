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
            value=headword,
            locations=[],
            parent_space=None,
            quality=None,
            links_in=links_in,
            links_out=links_out,
        )
        self.headword = headword
        self.forms = forms
        self.parts_of_speech = parts_of_speech

    @classmethod
    def new(cls, headword: str, forms: Dict[WordForm, str], parent_concept):
        from homer.structures.links import Relation

        lexeme = cls(ID.new(cls), "", headword, forms)
        link_to_concept = Relation(
            ID.new(Relation), "", parent_concept, lexeme, None, None, 0.0
        )
        link_to_concept._activation = 1.0
        parent_concept.links_out.add(link_to_concept)
        lexeme.links_in.add(link_to_concept)
        return lexeme

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
