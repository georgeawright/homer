import pytest
from unittest.mock import Mock

from homer.template import Template


@pytest.mark.parametrize(
    "words, concepts, expected",
    [
        (["it", "will", "be", None], ["hot"], "it will be hot"),
        (
            ["it", "will", "be", None, "in", "the", None],
            ["hot", "south"],
            "it will be hot in the south",
        ),
    ],
)
def test_get_text_and_words(words, concepts, expected):
    args = []
    for concept in concepts:
        arg = Mock()
        arg.name = concept
        args.append(arg)
    template = Template(words)
    actual_text, actual_words = template.get_text_and_words(*args)
    assert expected == actual_text
    assert expected == " ".join([word.value for word in actual_words])
