import pytest
from unittest.mock import Mock

from homer import fuzzy
from homer.classifiers import RuleClassifier
from homer.structure_collection import StructureCollection


def test_classify_det_relation():
    det_classifier = RuleClassifier(
        lambda kwargs: fuzzy.AND(
            kwargs["start"].location.coordinates[0][0]
            == kwargs["end"].location.coordinates[0][0] + 1,
            kwargs["start"].has_label_with_name("noun"),
            kwargs["end"].has_label_with_name("det"),
        )
    )
    det_word = Mock()
    det_word.location.coordinates = [[0]]
    det_word.has_label_with_name = lambda x: x == "det"
    noun_word = Mock()
    noun_word.location.coordinates = [[1]]
    noun_word.has_label_with_name = lambda x: x == "noun"
    verb_word = Mock()
    verb_word.location.coordinates = [[2]]
    verb_word.has_label_with_name = lambda x: x == "verb"
    assert det_classifier.classify(start=noun_word, end=det_word)
    assert not det_classifier.classify(start=det_word, end=noun_word)
    assert not det_classifier.classify(start=verb_word, end=noun_word)


def test_classify_nsubj_relation():
    nsubj_classifier = RuleClassifier(
        lambda kwargs: fuzzy.AND(
            kwargs["end"].has_label_with_name("noun"),
            fuzzy.OR(
                kwargs["start"].has_label_with_name("vbz"),
                fuzzy.AND(
                    fuzzy.OR(
                        kwargs["start"].has_label_with_name("jj"),
                        kwargs["start"].has_label_with_name("jjr"),
                    ),
                    kwargs["start"].has_relation_with_name("cop"),
                ),
            ),
            kwargs["end"].location.coordinates[0][0]
            < kwargs["start"].location.coordinates[0][0],
        ),
    )
    noun = Mock()
    noun.location.coordinates = [[0]]
    noun.has_label_with_name = lambda x: x == "noun"
    verb = Mock()
    verb.location.coordinates = [[1]]
    verb.has_label_with_name = lambda x: x == "vbz"
    adj = Mock()
    adj.location.coordinates = [[2]]
    adj.has_label_with_name = lambda x: x == "jj"
    adj.has_relation_with_name = lambda x: x == "cop"
    assert nsubj_classifier.classify(start=verb, end=noun)
    assert nsubj_classifier.classify(start=adj, end=noun)
    assert not nsubj_classifier.classify(start=verb, end=adj)


def test_classify_cop_relation():
    cop_classifier = RuleClassifier(
        lambda kwargs: fuzzy.AND(
            kwargs["end"].has_label_with_name("cop"),
            fuzzy.OR(
                kwargs["start"].has_label_with_name("jj"),
                kwargs["start"].has_label_with_name("jjr"),
            ),
            kwargs["start"].location.coordinates[0][0]
            == kwargs["end"].location.coordinates[0][0] + 1,
        )
    )
    cop = Mock()
    cop.location.coordinates = [[1]]
    cop.has_label_with_name = lambda x: x == "cop"
    adj = Mock()
    adj.location.coordinates = [[2]]
    adj.has_label_with_name = lambda x: x == "jj"
    assert cop_classifier.classify(start=adj, end=cop)
    assert not cop_classifier.classify(start=cop, end=adj)


def test_classify_prep_relation():
    prep_classifier = RuleClassifier(
        lambda kwargs: fuzzy.AND(
            kwargs["end"].has_label_with_name("prep"),
            fuzzy.OR(
                kwargs["start"].has_label_with_name("vbz"),
                fuzzy.AND(
                    fuzzy.OR(
                        kwargs["start"].has_label_with_name("jj"),
                        kwargs["start"].has_label_with_name("jjr"),
                    ),
                    kwargs["start"].has_relation_with_name("cop"),
                ),
            ),
            kwargs["start"].location.coordinates[0][0]
            < kwargs["end"].location.coordinates[0][0],
        )
    )
    verb = Mock()
    verb.location.coordinates = [[9]]
    verb.has_label_with_name = lambda x: x == "vbz"
    prep = Mock()
    prep.location.coordinates = [[10]]
    prep.has_label_with_name = lambda x: x == "prep"
    assert prep_classifier.classify(start=verb, end=prep)
    assert not prep_classifier.classify(start=prep, end=verb)


def test_classify_pobj_relation():
    pobj_classifier = RuleClassifier(
        lambda kwargs: fuzzy.AND(
            kwargs["end"].has_label_with_name("noun"),
            kwargs["start"].has_label_with_name("prep"),
            kwargs["start"].location.coordinates[0][0]
            < kwargs["end"].location.coordinates[0][0],
        )
    )
    prep = Mock()
    prep.location.coordinates = [[10]]
    prep.has_label_with_name = lambda x: x == "prep"
    det = Mock()
    det.location.coordinates = [[11]]
    det.has_label_with_name = lambda x: x == "det"
    noun = Mock()
    noun.location.coordinates = [[12]]
    noun.has_label_with_name = lambda x: x == "noun"
    assert pobj_classifier.classify(start=prep, end=noun)
    assert not pobj_classifier.classify(start=prep, end=det)


def test_classify_dep_relation():
    dep_classifier = RuleClassifier(
        lambda kwargs: fuzzy.AND(
            kwargs["end"].has_label_with_name("noun"),
            kwargs["start"].has_label_with_name("prep"),
            (
                lambda: kwargs["start"]
                .relation_with_name("prep")
                .start.has_relation_with_name("pobj")
            )(),
            kwargs["end"].location.coordinates[0][0]
            > kwargs["start"].location.coordinates[0][0],
        )
    )
    south = Mock()
    south.location.coordinates = [[10]]
    south.has_label_with_name = lambda x: x == "noun"
    south.has_relation_with_name = lambda x: x == "pobj"
    than_south_relation = Mock()
    than_south_relation.start = south
    than = Mock()
    than.location.coordinates = [[11]]
    than.has_label_with_name = lambda x: x == "prep"
    than.relation_with_name.return_value = than_south_relation
    the = Mock()
    the.location.coordinates = [[12]]
    the.has_label_with_name = lambda x: x == "det"
    north = Mock()
    north.location.coordinates = [[13]]
    north.has_label_with_name = lambda x: x == "noun"
    assert dep_classifier.classify(start=than, end=north)
    assert not dep_classifier.classify(start=than, end=south)
    assert not dep_classifier.classify(start=than, end=the)
