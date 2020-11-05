from typing import Dict, List

from homer.word_form import WordForm
from homer.structure import Structure
from homer.structure_collection import StructureCollection


class Lexeme(Structure):
    def __init__(
        self,
        headword: str,
        forms: Dict[WordForm, str],
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        location = None
        Structure.__init__(self, location, links_in, links_out)
        self.headword = headword
        self.forms = forms

    def get_form(self, form: WordForm) -> str:
        return self.forms[form]
