""" fixtures """

from typing import Any
from unittest.mock import MagicMock

from psycopg2.extensions import connection, cursor
from pytest import fixture

@fixture(autouse=True)
def mock_cursor()->cursor: # pylint: disable=redefined-outer-name
    """ setup a mock cursor """
    # Create a mock cursor object
    mycursor = MagicMock(spec=cursor)
    mycursor.reset_mock()

    return mycursor

@fixture(autouse=True)
def mock_conn(mock_cursor:cursor)->connection: # pylint: disable=redefined-outer-name
    """ setup a mock connection linked to a mock cursor """
    # Create a mock connection object
    myconn = MagicMock(spec=connection)
    myconn.reset_mock()

    # Link the mock objects
    myconn.cursor.return_value.__enter__.return_value = mock_cursor

    return myconn

def get_cursor(myconn:connection)->cursor:
    """ chain of dereferences """
    return myconn.cursor()#.return_value.__enter__.return_value

@fixture(autouse=True)
def mock_conn_with_exception(mock_conn:connection, request:Any)->connection: # pylint: disable=redefined-outer-name
    """ setup a mock connection that raises an exception when used """
    method_name = request.param

    mycursor = get_cursor(mock_conn)
    mock_method = getattr(mycursor, method_name)

    # Create a mock method that raises an exception when called
    mock_method.side_effect = Exception("An error occurred")

    return mock_conn
