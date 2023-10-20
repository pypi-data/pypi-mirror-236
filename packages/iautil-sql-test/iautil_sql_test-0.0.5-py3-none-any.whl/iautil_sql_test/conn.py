""" fixtures """

from functools import wraps
from typing import cast, Callable #, Any
from unittest.mock import MagicMock

from psycopg2.extensions import connection, cursor
#import pytest
from pytest import fixture, LogCaptureFixture, raises
#from pytest.helpers import getfixturevalue

#class MockCursor(MagicMock, connection):
#    """ mock cursor object """
#class MockConn(MagicMock, cursor):
#    """ mock connection object """
#    def cursor(self):
#        return MockCursor()

@fixture(autouse=True)
def mock_cursor()->cursor: # pylint: disable=redefined-outer-name
    """ setup a mock cursor """
    # Create a mock cursor object
    mycursor:MagicMock = MagicMock(spec=cursor)
    #mycursor:cursor = MagicMock()
    #mycursor:cursor = MockCursor()
    mycursor.reset_mock()

    return cast(cursor, mycursor)

@fixture(autouse=True)
def mock_conn(mock_cursor:cursor)->connection: # pylint: disable=redefined-outer-name
    """ setup a mock connection linked to a mock cursor """
    # Create a mock connection object
    myconn:MagicMock = MagicMock(spec=connection)
    #myconn:connection = MagicMock()
    #myconn:connection = MockConn()
    myconn.reset_mock()

    # Link the mock objects
    myconn.cursor.return_value.__enter__.return_value = mock_cursor
    #myconn.cursor.return_value = mock_cursor

    return cast(connection, myconn)

def get_cursor(myconn:connection)->cursor:
    """ chain of dereferences """
    return myconn.cursor()#.return_value.__enter__.return_value

ERROR_MESSAGE:str = "An error occurred"

# FixtureRequest
#@fixture(autouse=True)
#def mock_conn_with_exception(mock_conn:connection, request:Any)->connection: # pylint: disable=redefined-outer-name
#    """ setup a mock connection that raises an exception when used """
#    method_name:str = request.param
#
#    mycursor:cursor = get_cursor(mock_conn)
#    mock_method:Any = getattr(mycursor, method_name)
#
#    # Create a mock method that raises an exception when called
#    mock_method.side_effect = Exception(ERROR_MESSAGE)
#
#    return mock_conn






# example
#@mark.parameterize("mock_conn_with_exception", ["execute"])
#@test_exception_handling_and_error_logging
#def test_execute_handles_exceptions_and_logs_errors(caplog, mock_conn_with_exception):
#    execute(mock_conn_with_exception, "SELECT * FROM my_table", (1, 2, 3))


def test_exception_handling_and_error_logging(test_func:Callable[...,None])->Callable[...,None]:
    """A decorator for testing exception handling and logging."""

    @wraps(test_func)
    def wrapper(caplog:LogCaptureFixture, mock_conn_with_exception:connection)->None: # pylint: disable=redefined-outer-name
        """ wrapper """

        # Call the specified function
        with raises(Exception, match=ERROR_MESSAGE):
            # Call the decorated function
            test_func(caplog, mock_conn_with_exception)

        # Get the caplog fixture in the same scope as the test function
        #caplog = getfixturevalue('caplog')

        # Assert that the error message was logged
        assert ERROR_MESSAGE in caplog.text

    return wrapper


# example
#@mark.parameterize("mock_conn_with_exception", ["execute"])
#@test_logs_query
#def test_execute_logs_queries(mock_conn):
#    execute(mock_conn_with_exception, "SELECT * FROM my_table", (1, 2, 3))
#
#def test_logs_query(test_func:Callable[...,None])->Callable[...,None]: # pylint: disable=redefined-outer-name
#    """ a decorator for testing DB query logging """
#
#    @wraps(test_func)
#    def wrapper(caplog:LogCaptureFixture, mock_conn:connection)->None:
#        test_func(caplog, mock_conn)
#
#        # TADA sqlq is defined in test_func
#        assert f"Executing query: {sqlq}" in caplog.text
