""" Helper functions and decorators for SQL """

from logging import Logger
from typing import Dict, Iterable, Iterator, List, Optional, ParamSpec, Tuple, TypeVar, Union
#from typing import Callable

from psycopg2.extensions import connection, cursor

from iautil.log import configure_logging, handle_exception, trace # mypy: disable=import-untyped
from iautil_sql.log import log_query # mypy: disable=import-untyped


logger:Logger = configure_logging(__name__)

T = TypeVar('T')
P = ParamSpec('P')


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def execute(conn: connection, sqlq: str,
            args:Optional[Union[Tuple, Dict]]) -> None:
    """ cursor.execute() """
    with conn.cursor() as curs:
        curs.execute(sqlq, args)

@handle_exception(logger)
@trace(logger)
@log_query(logger)
def select(conn: connection, sqlq: str,
           args:Optional[Union[Tuple, Dict]]) -> List[Tuple]:
    """ cursor.execute(); cursor.fetchall() """
    with conn.cursor() as curs:
        curs.execute(sqlq, args)
        return curs.fetchall()


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def select_single(conn: connection, sqlq: str,
                  args:Optional[Union[Tuple, Dict]]) -> Union[Tuple,None]:
    """ cursor.execute(); cursor.fetchone() """
    with conn.cursor() as curs:
        curs.execute(sqlq, args)
        return curs.fetchone()



@handle_exception(logger)
@trace(logger)
@log_query(logger)
def execute_batch(conn: connection, sqlq: str,
                  args_list: Union[Iterable[Union[Tuple, Dict]],
                                   Iterator[Union[Tuple, Dict]]]) -> None:
    """ cursor.executemany() """
    with conn.cursor() as curs:
        curs.executemany(sqlq, args_list)


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def select_batch(conn: connection, sqlq: str,
                 args_list: Union[Iterable[Union[Tuple, Dict]],
                                  Iterator[Union[Tuple, Dict]]]) -> List[Tuple]:
    """ cursor.executemany(); cursor.fetchall() """
    with conn.cursor() as curs:
        curs.executemany(sqlq, args_list)
        return curs.fetchall()


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def bulk_helper(curs:cursor, sqlq:str, args:Optional[Union[Tuple,Dict]]) -> None:
    """ cursor.execute() """
    curs.execute(sqlq, args)

@handle_exception(logger)
@trace(logger)
#@log_query(logger)
def execute_bulk(conn: connection, sqlq_list: List[str],
                 args_list: Union[Iterable[Union[Tuple, Dict]],
                                  Iterator[Union[Tuple, Dict]]]) -> None:
    """ bulk_helper() """
    with conn.cursor() as curs:
        for sqlq, args in zip(sqlq_list, args_list):
            #curs.execute(sqlq, args)
            bulk_helper(curs, sqlq, args)

@handle_exception(logger)
@trace(logger)
#@log_query(logger)
def select_bulk(conn: connection, sqlq_list: List[str],
                args_list: Union[Iterable[Union[Tuple, Dict]],
                                 Iterator[Union[Tuple, Dict]]]) -> List[List[Tuple]]:
    """ bulk_helper(); cursor.fetchall() """
    with conn.cursor() as curs:
        result_sets:List[List[Tuple]] = []
        for sqlq, args in zip(sqlq_list, args_list):
            #curs.execute(sqlq, args)
            bulk_helper(curs, sqlq, args)
            result_sets.append(curs.fetchall())
        return result_sets
