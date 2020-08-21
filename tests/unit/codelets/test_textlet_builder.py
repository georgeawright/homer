from unittest.mock import Mock

from homer.codelets import TextletBuilder


def test_engender_follow_up():
    phrase_builder = TextletBuilder(Mock(), Mock(), Mock(), Mock(), Mock())
    phrase_builder.confidence = 1.0
    follow_up = phrase_builder._engender_follow_up()
    assert type(follow_up) == TextletBuilder


def test_engender_alternative_follow_up():
    phrase_builder = TextletBuilder(Mock(), Mock(), Mock(), 1.0, Mock())
    follow_up = phrase_builder._engender_alternative_follow_up()
    assert type(follow_up) == TextletBuilder
