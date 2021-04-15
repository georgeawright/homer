import pytest
from unittest.mock import Mock

from homer.word_form import WordForm
from homer.structures.nodes import Lexeme


@pytest.mark.parametrize(
    "headword, forms, required_form, expected",
    [
        (
            "cold",
            {
                WordForm.HEADWORD: "cold",
                WordForm.COMPARATIVE: "colder",
                WordForm.SUPERLATIVE: "coldest",
            },
            WordForm.HEADWORD,
            "cold",
        ),
        (
            "hot",
            {
                WordForm.HEADWORD: "hot",
                WordForm.COMPARATIVE: "hotter",
                WordForm.SUPERLATIVE: "hottest",
            },
            WordForm.COMPARATIVE,
            "hotter",
        ),
        (
            "north",
            {
                WordForm.HEADWORD: "north",
                WordForm.COMPARATIVE: "further north",
                WordForm.SUPERLATIVE: "furthest north",
            },
            WordForm.COMPARATIVE,
            "further north",
        ),
    ],
)
def test_get_form(headword, forms, required_form, expected):
    lexeme = Lexeme(Mock(), Mock(), headword, forms, Mock())
    assert expected == lexeme.get_form(required_form)
