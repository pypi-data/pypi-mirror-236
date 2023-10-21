""" Helper functions and decorators for SQL """

from functools import wraps
from logging import Logger
from pathlib import Path
from typing import (
    Callable, List,
    #Optional,
    TypeVar, Iterable
)

from psycopg2.extensions import connection

from iautil.log import (
    configure_logging,
    handle_exception,
    trace)

#from iautil_sql.log import log_query
from iautil_sql.sql import (
    execute, select, select_single,
    execute_batch, select_batch,
    execute_bulk, select_bulk)
from iautil_sql.types import QueryPath, QueryPaths#, T


logger:Logger = configure_logging(__name__)

R = TypeVar('R')


@handle_exception(logger)
@trace(logger)
#def query_string_helper(query:Union[str,Path,SQL])->SQL:
def query_strings_helper(sqlq:QueryPaths)->Iterable[str]:
    """ get the query string(s) """
    if isinstance(sqlq, List):
        return map(query_string_helper, sqlq)
    return [query_string_helper(sqlq)]

@handle_exception(logger)
@trace(logger)
def query_string_helper(sqlq:QueryPath)->str:
    """ get the query string """
    #if isinstance(query, SQL):
    #    return query
    if isinstance(sqlq, str):
        return sqlq
    #    return SQL(query)
    assert isinstance(sqlq,Path)
    with sqlq.open() as file:
        return file.read()

#@handle_exception(logger)
#@trace(logger)
#def query_decorator(query:QueryPaths,
#                    query_function: Callable[..., None]) -> Callable[
#                        [Callable[...,R]],
#                        Callable[[connection],R]]:
#    """ Generic query decorator """
#    query_str: str = query_strings_helper(query)
#
#    def decorator(func: Callable[..., R]) -> Callable[[connection], R]:
#        """ Decorator function """
#        @wraps(func)
#        def wrapper(conn: connection, *args) -> R:
#            """ Wrapper function """
#            query_function(conn, query_str, *args)
#            return func(conn)
#
#        return wrapper
#    return decorator

F = TypeVar('F')
@handle_exception(logger)
@trace(logger)
def query(sqlq:QueryPaths,
                     query_function: Callable[..., F]) -> Callable[
                         [Callable[...,R]],
                         Callable[[connection,F],R]]:
    """ Generic query decorator """
    query_str: str = query_strings_helper(sqlq)

    def decorator(func: Callable[..., R]) -> Callable[[connection,F], R]:
        """ Decorator function """
        @wraps(func)
        def wrapper(conn: connection, *args) -> R:
            """ Wrapper function """
            res:F = query_function(conn, query_str, *args)
            return func(conn, res)

        return wrapper
    return decorator


@trace(logger)
def execute2(sqlq:QueryPaths):
    """ execute(); rewrites signature """
    return query(sqlq, execute)

@trace(logger)
def select2(sqlq:QueryPaths):
    """ select(); rewrites signature """
    #return query_decorator(query, select)
    return query(sqlq, select)

@trace(logger)
def select_single2(sqlq:QueryPaths):
    """ select_single(); rewrites signature """
    #return query_decorator(query, select_single)
    return query(sqlq, select_single)

@trace(logger)
def execute_batch2(sqlq:QueryPaths):
    """ execute_batch(); rewrites signature """
    return query(sqlq, execute_batch)

@trace(logger)
def select_batch2(sqlq:QueryPaths):
    """ select_batch(); rewrites signature """
    #return query_decorator(query, select_batch)
    return query(sqlq, select_batch)

@trace(logger)
def execute_bulk2(sqlq:QueryPaths):
    """ execute_bulk(); rewrites signature """
    return query(sqlq, execute_bulk)

@trace(logger)
def select_bulk2(sqlq:QueryPaths):
    """ select_bulk(); rewrites signature """
    #return query_decorator(query, select_bulk)
    return query(sqlq, select_bulk)
