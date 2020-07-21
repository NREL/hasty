from lib.helpers import is_number, is_false


def test_is_number():
    assert is_number(5)


def test_is_false():
    false = False
    assert is_false(false) is False
