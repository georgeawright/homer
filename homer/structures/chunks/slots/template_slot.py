from typing import List

from homer.location import Location
from homer.word_form import WordForm
from homer.structure_collection import StructureCollection
from homer.structures import Concept, Space
from homer.structures.chunks.slot import Slot


class TemplateSlot(Slot):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        parent_space: Space,
        prototype: Concept,
        form: WordForm,
        locations: List[Location],
    ):
        Slot.__init__(
            self,
            structure_id,
            parent_id,
            parent_space,
            value=prototype,
            locations=locations,
        )
        self.form = form
