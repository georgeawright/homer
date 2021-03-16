from __future__ import annotations
from typing import Union

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.structure_collection import StructureCollection
from homer.structures import Node


class Phrase(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        chunk: "Chunk",
        label: "Label",
        quality: FloatBetweenOneAndZero,
        left_branch: Union[Phrase, "Word"] = None,
        right_branch: Union[Phrase, "Word"] = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Node.__init__(
            self,
            structure_id,
            parent_id,
            value=label.value,
            locations=chunk.locations,
            parent_space=chunk.parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.chunk = chunk
        self.label = label
        self.left_branch = left_branch
        self.right_branch = right_branch

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders import PhraseBuilder

        return PhraseBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators import PhraseEvaluator

        return PhraseEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors import PhraseSelector

        return PhraseSelector

    @property
    def value(self):
        return self.label.value

    @property
    def locations(self):
        return self.chunk.locations

    @property
    def parent_concept(self):
        return self.label.parent_concept

    @property
    def parent_space(self):
        return self.chunk.parent_space

    @property
    def members(self):
        return self.chunk.members

    @property
    def is_slot(self):
        return self.chunk.is_slot

    @property
    def size(self):
        return self.chunk.size

    @property
    def unchunkedness(self):
        return self.chunk.unchunkedness
