# -*- coding: utf-8 -*-

from iam import ObjectSet, make_expression
from iam.eval.constants import KEYWORD_BK_IAM_PATH_FIELD_SUFFIX, OP
from iam.eval.expression import _parse_bk_iam_path, field_value_convert


def test_make_expression_and():
    d = {
        "op": "AND",
        "content": [
            {"op": "eq", "field": "host.id", "value": "a1"},
            {"op": "eq", "field": "host.name", "value": "b1"},
        ],
    }
    expr = make_expression(d)
    assert expr.expr() == "((host.id eq 'a1') AND (host.name eq 'b1'))"

    d1 = ObjectSet()
    d1.add_object("host", {"id": "a1", "name": "b1"})

    assert expr.eval(d1)


def test_make_expression_or():
    d = {
        "op": "OR",
        "content": [
            {"op": "eq", "field": "host.id", "value": "a1"},
            {"op": "eq", "field": "host.name", "value": "b1"},
        ],
    }
    expr = make_expression(d)
    assert expr.expr() == "((host.id eq 'a1') OR (host.name eq 'b1'))"

    d1 = ObjectSet()
    d1.add_object("host", {"id": "a1", "name": "b1"})

    assert expr.eval(d1)


def test_make_expression():
    d = {"op": "eq", "field": "host.id", "value": "a1"}
    expr = make_expression(d)

    assert expr.expr() == "(host.id eq 'a1')"

    d1 = ObjectSet()
    d1.add_object("host", {"id": "a1", "name": "b1"})

    assert expr.eval(d1)


def test_parse_bk_iam_path():
    # not a path
    assert "a" == _parse_bk_iam_path("a")

    # path
    assert "/biz,1/set,1/" == _parse_bk_iam_path("/biz,1/set,1/")

    assert "/biz,1/set," == _parse_bk_iam_path("/biz,1/set,*/")

    # tuple
    assert ["a", "b"] == _parse_bk_iam_path(("a", "b"))

    # tuple path
    assert ["/biz,1/set,1/", "/biz,2/module,"] == _parse_bk_iam_path(("/biz,1/set,1/", "/biz,2/module,*/"))

    # int
    assert 1 == _parse_bk_iam_path(1)


def test_field_value_convert():
    assert ("a", "b") == field_value_convert("equal", "a", "b")

    # path, not fit
    assert ("a%s" % KEYWORD_BK_IAM_PATH_FIELD_SUFFIX, "b") == field_value_convert(
        OP.STARTS_WITH, "a%s" % KEYWORD_BK_IAM_PATH_FIELD_SUFFIX, "b"
    )
    assert ("a%s" % KEYWORD_BK_IAM_PATH_FIELD_SUFFIX, "/biz,1/set,2/") == field_value_convert(
        OP.STARTS_WITH, "a%s" % KEYWORD_BK_IAM_PATH_FIELD_SUFFIX, "/biz,1/set,2/"
    )

    # path, fit
    assert ("a%s" % KEYWORD_BK_IAM_PATH_FIELD_SUFFIX, "/biz,1/set,") == field_value_convert(
        OP.STARTS_WITH, "a%s" % KEYWORD_BK_IAM_PATH_FIELD_SUFFIX, "/biz,1/set,*/"
    )
