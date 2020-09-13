import pytest

from agon import Agon


def test_search():
    agon = Agon("foo.bar")
    assert agon.search({"foo": {"bar": "baz"}}) == "baz"
    assert agon.search({"foo": {}}) is None


def test_projection():
    agon = Agon("foo.bar")
    assert {"foo": {"bar": "baz"}} | agon == "baz"
    assert {"foo": {}} | agon is None


def test_chaining():
    agon = Agon("foo.bar") | Agon("[0]")
    assert agon == Agon("foo.bar | [0]")

    agon = Agon("foo.bar") | "[0]"
    assert agon == Agon("foo.bar | [0]")

    agon = Agon("foo.bar | [0]")
    assert agon == Agon("foo.bar | [0]")


def test_integration():
    assert {"foo": {"bar": "baz"}} | Agon("foo | bar") == "baz"
    assert {"foo": {"bar": "baz"}} | Agon("foo") | Agon("bar") == "baz"
    with pytest.raises(TypeError):
        assert {"foo": {"bar": "baz"}} | Agon("foo") | "bar" == "baz"
    assert {"foo": {"bar": "baz"}} | (Agon("foo") | "bar") == "baz"
    assert Agon("foo | bar") == Agon("foo") | Agon("bar") == Agon("foo") | "bar"
