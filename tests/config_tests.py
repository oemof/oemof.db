# -*- coding: utf-8 -

"""Tests of the component module.

SPDX-License-Identifier: MIT
"""


from configparser import NoOptionError, NoSectionError
import os

import pytest

from oemof.db import config


TEST_INI = os.path.join(os.path.dirname(__file__), "config_test.ini")


def test_main_basic():
    config.main()
    config.load_config(None)


def test_correct_filename():
    fn = "dahfausf.ini"
    f = open(fn, "w+")
    f.write("[type_tester]\n")
    f.write("asd = hello blubb")
    f.close()
    config.load_config(fn)
    assert config.get("type_tester", "asd") == "hello blubb"
    os.remove(fn)
    config.FILE = ""


def test_init_wrong_filename(caplog):
    config.load_config("wrong_filename")
    assert "For further advice, see in the docs" in caplog.text


def test_init_wrong_filename_with_correct_file(caplog):
    config.FILE = TEST_INI
    config.load_config("wrong_filename")
    assert len(caplog.text) == 0


def test_init_wrong_fidsflename_with_correct_file(caplog):
    config.FILE = "dsfa"
    config.load_config(None)
    # assert len(caplog.text) == 0


def test_get_function():
    """Read config file."""
    config.FILE = TEST_INI
    config.load_config(TEST_INI)
    assert config.get("type_tester", "my_bool") is True
    assert isinstance(config.get("type_tester", "my_int"), int)
    assert config.get("type_tester", "my_int") == 5
    assert isinstance(config.get("type_tester", "my_float"), float)
    assert config.get("type_tester", "my_float") == 4.5
    assert isinstance(config.get("type_tester", "my_string"), str)
    config._loaded = False
    assert config.get("type_tester", "my_string") == "hallo"
    assert isinstance(config.get("type_tester", "my_None"), type(None))
    assert config.get("type_tester", "my_none") is None
    assert isinstance(config.get("type_tester", "my_list"), str)
    assert config.get("type_tester", "my_list") == "4,6,7,9"


def test_missing_value():
    config.FILE = TEST_INI
    with pytest.raises(
        NoOptionError, match="No option 'blubb' in section: 'type_tester'"
    ):
        config.get("type_tester", "blubb")
    with pytest.raises(NoSectionError, match="No section: 'typetester'"):
        config.get("typetester", "my_bool")


def test_set_temp_value():

    config.FILE = TEST_INI
    with pytest.raises(
        NoOptionError, match="No option 'blubb' in section: 'type_tester'"
    ):
        config.get("type_tester", "blubb")
    config.set("type_tester", "blubb", "None")
    assert config.get("type_tester", "blubb") is None
    config.set("type_tester", "blubb", "5.5")
    assert config.get("type_tester", "blubb") == 5.5
    remove_line()


def test_set_temp_without_init():
    config._loaded = False
    config.set("type_tester", "blubb", "None")
    assert config.get("type_tester", "blubb") is None
    config.set("blubb_tester", "blubb", "None")
    remove_line()


def remove_line():
    with open(TEST_INI, "r") as f:
        lines = f.readlines()
    with open(TEST_INI, "w") as f:
        for line in lines:
            print(line)
            if "blubb" not in line:
                f.write(line)
