import sys, os
import pytest

#PATHS
TEST_DIR=os.path.realpath(os.path.dirname(__file__))
BASE_DIR=os.path.dirname(TEST_DIR)
sys.path.append(BASE_DIR)

from rimsdash.external.rims import clean

@pytest.mark.parametrize("name, expected_output", \
                            [
                                ('John Smith (s4123456)', 'John Smith'),
                                ('John Smith (uqjsmi)', 'John Smith'),
                                ('John Smith (uqjsmit1)', 'John Smith'),
                                ('John Smith (john.smith1)', 'John Smith'),
                                ('John Smith (Johnny)', 'John Smith (Johnny)'),
                            ]
                        )
def test_strip_brackets(name, expected_output):
    assert clean.strip_brackets(name) == expected_output


def test_fix_special_chars():
    sample = "This is a [[sqote]]test[[sqote]] for special [[dqote]]character[[dqote]] replacement for titles [[and]] descriptions"
    expected_output = "This is a \'test\' for special \"character\" replacement for titles & descriptions"

    assert clean.fix_special_chars(sample) == expected_output

