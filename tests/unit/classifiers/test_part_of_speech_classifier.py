import pytest
from unittest.mock import Mock

from homer.classifiers import PartOfSpeechClassifier


@pytest.fixture
def adjective_concept():
    concept = Mock()
    return concept


@pytest.fixture
def noun_concept():
    concept = Mock()
    return concept


@pytest.fixture
def headword_word_form():
    word_form = Mock()
    return word_form


@pytest.fixture
def hot_lexeme(adjective_concept, headword_word_form):
    lexeme = Mock()
    lexeme.parts_of_speech = {headword_word_form: [adjective_concept]}
    return lexeme


@pytest.fixture
def hot_word(hot_lexeme, headword_word_form):
    word = Mock()
    word.lexeme = hot_lexeme
    word.word_form = headword_word_form
    return word


def test_classifies_adjective_as_adjective(adjective_concept, hot_word):
    classifier = PartOfSpeechClassifier()
    assert classifier.classify(concept=adjective_concept, start=hot_word)


def test_does_not_classify_adjective_as_noun(noun_concept, hot_word):
    classifier = PartOfSpeechClassifier()
    assert not classifier.classify(concept=noun_concept, start=hot_word)
