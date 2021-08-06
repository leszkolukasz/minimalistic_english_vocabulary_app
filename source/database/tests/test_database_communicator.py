import pytest
from ..database_entry import Entry
from ..database_communicator import DatabaseCommunicator

communicator = DatabaseCommunicator('dictionary.pickle')

@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_methods():
    assert communicator.find_words(test_input) == expected