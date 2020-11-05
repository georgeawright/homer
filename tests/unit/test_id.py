from collections import defaultdict
import pytest
from unittest.mock import Mock

from homer.id import ID


@pytest.mark.parametrize(
    "qualifier, expected",
    [("BottomUp", "BottomUpMock1"), ("TopDown", "TopDownMock1"), (None, "Mock1")],
)
def test_new(qualifier, expected):
    ID.COUNTS = defaultdict(int)
    assert expected == ID.new(type(Mock()), qualifier)
