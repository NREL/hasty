from haste.lib.helpers import is_number, is_false


def test_is_number():
    number = 5
    assert is_number(5) == True


def test_is_false():
    false = False
    assert is_false(false) == False

