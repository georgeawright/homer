from __future__ import annotations
from typing import List, Union

from homer.perceptlet import Perceptlet


class RawPerceptlet(Perceptlet):
    """A single piece of perceived raw data, ie a number or symbol"""

    def __init__(self, value: Union[str, int, float], neighbours: List[RawPerceptlet]):
        Perceptlet.__init__(value, neighbours)
