from unittest.mock import Mock

from homer.structures.spaces import ConceptualSpace, WorkingSpace


def test_instance_returns_working_space():
    conceptual_space = ConceptualSpace("name", Mock(), Mock())
    instance = conceptual_space.instance
    assert isinstance(instance, WorkingSpace)
