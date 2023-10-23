from io import StringIO
from dig_ini_editor.editor import Editor

SECTION_FIRST = "main section"
KEY_FIRST = "main key"
VALUE_FIRST = "main value"

SECTION_SECOND = "sample"
KEY_SECOND = "command"
VALUE_SECOND = "python"
KEY_THIRD = "args"
VALUE_THIRD = "--version"

SECTION_RANDOM = "629e7a7c-0094-4f33-8c1f-58a04810b33f"
KEY_RANDOM = "9ec2ca18-c55f-466a-b519-877c8b4661a7"
VALUE_RANDOM = "88424517-ae75-49d4-a3b0-5ef16d935916"

TEST_INI = f"""
[{SECTION_FIRST}]
{KEY_FIRST} = {VALUE_FIRST}
[{SECTION_SECOND}]
{KEY_SECOND}={VALUE_SECOND}
{KEY_THIRD}={VALUE_THIRD}
"""


def test_ensure_not_collision_for_tests():
    assert SECTION_FIRST != SECTION_SECOND
    assert SECTION_FIRST != SECTION_RANDOM
    assert SECTION_SECOND != SECTION_RANDOM

    assert KEY_FIRST != KEY_SECOND
    assert KEY_FIRST != KEY_THIRD
    assert KEY_FIRST != KEY_RANDOM
    assert KEY_SECOND != KEY_THIRD
    assert KEY_SECOND != KEY_RANDOM
    assert KEY_THIRD != KEY_RANDOM

    assert VALUE_FIRST != VALUE_SECOND
    assert VALUE_FIRST != VALUE_THIRD
    assert VALUE_FIRST != VALUE_RANDOM
    assert VALUE_SECOND != VALUE_THIRD
    assert VALUE_SECOND != VALUE_RANDOM
    assert VALUE_THIRD != VALUE_RANDOM


def test_get_sections():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    assert f"{SECTION_FIRST},{SECTION_SECOND}" == editor.get(None, None, ",")


def test_get_keys():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    assert KEY_FIRST == editor.get(SECTION_FIRST, None, ",")
    assert f"{KEY_SECOND},{KEY_THIRD}" == editor.get(SECTION_SECOND, None, ",")


def test_get_values():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    assert VALUE_FIRST == editor.get(SECTION_FIRST, KEY_FIRST, ",")
    assert VALUE_SECOND == editor.get(SECTION_SECOND, KEY_SECOND, ",")
    assert VALUE_THIRD == editor.get(SECTION_SECOND, KEY_THIRD, ",")


def test_set_value_new_section():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    section = SECTION_RANDOM
    key = KEY_RANDOM
    value = VALUE_RANDOM
    editor.set(section, key, value)
    assert VALUE_FIRST == editor.get(SECTION_FIRST, KEY_FIRST, ",")
    assert VALUE_SECOND == editor.get(SECTION_SECOND, KEY_SECOND, ",")
    assert VALUE_THIRD == editor.get(SECTION_SECOND, KEY_THIRD, ",")
    assert value == editor.get(section, key, ",")


def test_set_value_exist_section_new_key():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    section = SECTION_FIRST
    key = KEY_RANDOM
    value = VALUE_RANDOM
    editor.set(section, key, value)
    assert VALUE_FIRST == editor.get(SECTION_FIRST, KEY_FIRST, ",")
    assert VALUE_SECOND == editor.get(SECTION_SECOND, KEY_SECOND, ",")
    assert VALUE_THIRD == editor.get(SECTION_SECOND, KEY_THIRD, ",")
    assert value == editor.get(section, key, ",")


def test_set_value_exist_section_override_key():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    section = SECTION_FIRST
    key = KEY_FIRST
    value = VALUE_RANDOM
    editor.set(section, key, value)
    assert value == editor.get(SECTION_FIRST, KEY_FIRST, ",")
    assert VALUE_SECOND == editor.get(SECTION_SECOND, KEY_SECOND, ",")
    assert VALUE_THIRD == editor.get(SECTION_SECOND, KEY_THIRD, ",")


def test_delete_section_not_exists():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    editor.delete(SECTION_RANDOM, None)
    assert f"{SECTION_FIRST},{SECTION_SECOND}" == editor.get(None, None, ",")


def test_delete_section_exists():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    editor.delete(SECTION_FIRST, None)
    assert SECTION_SECOND == editor.get(None, None, ",")


def test_delete_section_not_exists_key_not_exists():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    editor.delete(SECTION_RANDOM, VALUE_RANDOM)
    assert f"{SECTION_FIRST},{SECTION_SECOND}" == editor.get(None, None, ",")


def test_delete_section_exists_key_not_exists():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    editor.delete(SECTION_FIRST, VALUE_RANDOM)
    assert KEY_FIRST == editor.get(SECTION_FIRST, None, ",")
    editor.delete(SECTION_SECOND, VALUE_RANDOM)
    assert f"{KEY_SECOND},{KEY_THIRD}" == editor.get(SECTION_SECOND, None, ",")


def test_delete_section_exists_key_exists():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    editor.delete(SECTION_FIRST, KEY_FIRST)
    assert not editor.contains(SECTION_FIRST, KEY_FIRST)
    editor.delete(SECTION_SECOND, KEY_THIRD)
    assert KEY_SECOND == editor.get(SECTION_SECOND, None, ",")
    assert not editor.contains(SECTION_SECOND, KEY_THIRD)


def test_exists_not_section():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    assert not editor.contains(SECTION_RANDOM, None)
    assert not editor.contains(SECTION_RANDOM, KEY_RANDOM)


def test_exists_section_not_key():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    assert editor.contains(SECTION_FIRST, None)
    assert not editor.contains(SECTION_FIRST, KEY_RANDOM)


def test_exists_section_and_key():
    editor = Editor()
    editor.read(StringIO(TEST_INI))
    assert editor.contains(SECTION_FIRST, None)
    assert editor.contains(SECTION_FIRST, KEY_FIRST)
    assert editor.contains(SECTION_SECOND, None)
    assert editor.contains(SECTION_SECOND, KEY_THIRD)
