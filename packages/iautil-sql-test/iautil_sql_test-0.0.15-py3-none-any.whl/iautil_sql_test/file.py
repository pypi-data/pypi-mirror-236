""" mock_open_query_string fixture """

from pathlib import Path
from unittest.mock import MagicMock


from pytest import fixture, MonkeyPatch


from iautil_test.file import MockFile


from iautil_sql_test.strings import QUERY_STRING


QUERY_PATH:Path  = Path("etc/query.sql")

with open(QUERY_PATH, mode='r', encoding='utf-8') as file:
    contents:str = file.read()
assert contents == QUERY_STRING


@fixture
def mock_open_query_string(monkeypatch:MonkeyPatch)->None: # pylint: disable=redefined-outer-name
    """ mock open() """
    mock_file:MockFile = MockFile(QUERY_STRING)
    mock_obj:MagicMock = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_obj)
