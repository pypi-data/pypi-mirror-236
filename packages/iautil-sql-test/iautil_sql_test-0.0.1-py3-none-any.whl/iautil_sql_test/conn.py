""" fixtures """

from unittest.mock import MagicMock

from psycopg2.extensions import connection, cursor
from pytest import fixture

@fixture(autouse=True)
def mock_cursor(): # pylint: disable=redefined-outer-name
    """ setup a mock cursor """
    # Create a mock cursor object
    mycursor = MagicMock(spec=cursor)
    mycursor.reset_mock()

    return mycursor

@fixture(autouse=True)
def mock_conn(mock_cursor): # pylint: disable=redefined-outer-name
    """ setup a mock connection linked to a mock cursor """
    # Create a mock connection object
    myconn = MagicMock(spec=connection)
    myconn.reset_mock()

    # Link the mock objects
    myconn.cursor.return_value.__enter__.return_value = mock_cursor

    return myconn

@fixture(autouse=True)
def mock_conn_with_exception(mock_conn): # pylint: disable=redefined-outer-name
    """ setup a mock connection that raises an exception when used """
    mycursor = mock_conn.cursor.return_value.__enter__.return_value

    # Create a mock cursor object that raises an exception when execute is called
    mycursor.execute.side_effect = Exception("An error occurred")

    return mock_conn
