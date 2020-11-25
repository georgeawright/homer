from typing import Dict, List

from homer.word_form import WordForm
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Lexeme(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        headword: str,
        forms: Dict[WordForm, str],
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        location = None
        quality = None
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            location,
            quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.headword = headword
        self.forms = forms

    @classmethod
    def new(cls, headword: str, forms: Dict[WordForm, str], parent_concept):
        from homer.structures import Concept
        from homer.structures.links import Relation

        lexeme = cls(headword, forms)
        link_to_concept = Relation(parent_concept, lexeme, None, None, 0.0)
        link_to_concept._activation = 1.0
        parent_concept.links_out.add(link_to_concept)
        lexeme.links_in.add(link_to_concept)
        return lexeme

    def get_form(self, form: WordForm) -> str:
        return self.forms[form]
