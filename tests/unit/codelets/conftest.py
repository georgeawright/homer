import pytest
from unittest.mock import Mock


@pytest.fixture
def target_perceptlet(scope="module"):
    target_perceptlet = Mock()
    target_perceptlet.location = [0, 0, 0]
    return target_perceptlet
