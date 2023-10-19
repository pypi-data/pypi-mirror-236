""" Helper functions and decorators for SQL """

from functools import wraps
import logging
from typing import Callable, List, Tuple, TypeVar

#from psycopg2 import connect  # type: ignore
#from psycopg2 import sql  # type: ignore
from psycopg2.extensions import connection  # type: ignore

from iautil.log import configure_logging, handle_exception, trace # type: ignore

logger = configure_logging(__name__)

T = TypeVar('T')

def log_query(mylogger:logging.Logger)->Callable[[Callable[...,T]],Callable[...,T]]:
    """
    Decorator function to log the executed SQL queries.
    """
    def decorator(func:Callable[...,T])->Callable[...,T]:
        """
        Decorator function to log the executed SQL queries.
        """
        @wraps(func)
        def wrapper(conn:connection, sqlq:str, *args:Tuple)->T:
            """
            Wrapper function to log the executed SQL queries.
            """
            mylogger.debug('Executing query: %s\nParams: %s', sqlq, args)
            return func(conn, sqlq, *args)
        return wrapper
    return decorator


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def execute(func:Callable)->Callable:
    """ cur.execute() """
    @wraps(func)
    def wrapper(conn: connection, sqlq: str, *args: Tuple) -> None:
        """ wrapper function """
        with conn.cursor() as curs:
            curs.execute(sqlq, *args)
    return wrapper


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def select(func:Callable)->Callable:
    """ curs.execute(); curs.fetchall() """
    @wraps(func)
    def wrapper(conn: connection, sqlq: str, *args: Tuple) -> List[Tuple]:
        """ wrapper function """
        with conn.cursor() as curs:
            curs.execute(sqlq, *args)
            return curs.fetchall()
    return wrapper


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def select_single(func:Callable)->Callable:
    """ curs.execute(); curs.fetchone() """
    @wraps(func)
    def wrapper(conn: connection, sqlq: str, *args: Tuple) -> Tuple:
        """ wrapper function """
        with conn.cursor() as curs:
            curs.execute(sqlq, *args)
            return curs.fetchone()
    return wrapper
