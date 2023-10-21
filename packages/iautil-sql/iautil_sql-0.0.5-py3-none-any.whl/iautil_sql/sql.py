""" Helper functions and decorators for SQL """

from logging import Logger
from typing import List, Tuple, Union
#from typing import Callable

from psycopg2.extensions import connection, cursor
from psycopg2.sql import SQL

from iautil.log import (
    configure_logging, handle_exception, trace)
from iautil_sql.log import log_query
from iautil_sql.types import QueryArg, QueryArgList, Query


logger:Logger = configure_logging(__name__)


@handle_exception(logger)
@trace(logger)
def convert_query(conn: connection, query:Query) -> str:
    """ force string type """
    if isinstance(query, SQL):
        return query.as_string(conn)
    return query


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def execute(conn: connection, sqlq:Query,
            args:QueryArg) -> None:
    """ cursor.execute() """
    sqls = convert_query(conn, sqlq)
    with conn.cursor() as curs:
        curs.execute(sqls, args)

@handle_exception(logger)
@trace(logger)
@log_query(logger)
def select(conn: connection, sqlq:Query,
           args:QueryArg) -> List[Tuple]:
    """ cursor.execute(); cursor.fetchall() """
    sqls = convert_query(conn, sqlq)
    with conn.cursor() as curs:
        curs.execute(sqls, args)
        return curs.fetchall()


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def select_single(conn: connection, sqlq:Query,
                  args:QueryArg) -> Union[Tuple,None]:
    """ cursor.execute(); cursor.fetchone() """
    sqls = convert_query(conn, sqlq)
    with conn.cursor() as curs:
        curs.execute(sqls, args)
        return curs.fetchone()


@handle_exception(logger)
@trace(logger)
@log_query(logger)
def execute_batch(conn:connection,
                  sqlq:Query,
                  args_list:QueryArgList) -> None:
    """ cursor.executemany() """
    sqls = convert_query(conn, sqlq)
    with conn.cursor() as curs:
        curs.executemany(sqls, args_list)

@handle_exception(logger)
@trace(logger)
@log_query(logger)
def select_batch(conn: connection,
                 sqlq:Query,
                 args_list:QueryArgList) -> List[Tuple]:
    """ cursor.executemany(); cursor.fetchall() """
    sqls = convert_query(conn, sqlq)
    with conn.cursor() as curs:
        curs.executemany(sqls, args_list)
        return curs.fetchall()


@handle_exception(logger)
@trace(logger)
@log_query(logger)
#def bulk_helper(curs:cursor, sqlq:Query, args:QueryArg) -> None:
def bulk_helper(curs:cursor,
                sqls:str,
                args:QueryArg) -> None:
    """ cursor.execute() """
    #sqls = convert_query(sqlq)
    curs.execute(sqls, args)

@trace(logger)
def convert_query_bulk_helper(conn:connection):
    """ helper for converting bulk queries """
    def helper(sqlq:Query):
        """ binds the connection """
        return convert_query(conn, sqlq)
    return helper


@handle_exception(logger)
@trace(logger)
#@log_query(logger)
def execute_bulk(conn:connection,
                 sqlq_list:List[Query],
                 args_list:QueryArgList) -> None:
    """ bulk_helper() """
    sqls_list = map(convert_query_bulk_helper(conn), sqlq_list)
    with conn.cursor() as curs:
        #for sqlq, args in zip(sqlq_list, args_list):
        for sqlq, args in zip(sqls_list, args_list):
            #curs.execute(sqlq, args)
            bulk_helper(curs, sqlq, args)

@handle_exception(logger)
@trace(logger)
#@log_query(logger)
def select_bulk(conn:connection,
                sqlq_list:List[Query],
                args_list:QueryArgList) -> List[List[Tuple]]:
    """ bulk_helper(); cursor.fetchall() """
    sqls_list = map(convert_query_bulk_helper(conn), sqlq_list)
    with conn.cursor() as curs:
        result_sets:List[List[Tuple]] = []
        #for sqlq, args in zip(sqlq_list, args_list):
        for sqlq, args in zip(sqls_list, args_list):
            #curs.execute(sqlq, args)
            bulk_helper(curs, sqlq, args)
            result_sets.append(curs.fetchall())
        return result_sets
