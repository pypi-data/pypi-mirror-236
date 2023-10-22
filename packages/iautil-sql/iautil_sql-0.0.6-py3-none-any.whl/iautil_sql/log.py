""" Helper functions and decorators for SQL """

from functools import wraps
from logging import Logger
from typing import Callable, Dict, Iterator, Iterable, Optional, Tuple, Union
#from typing import Concatenate

from psycopg2 import Error as PGError
from psycopg2.extensions import connection, cursor
#from psycopg2.sql import SQL

#from iautil_sql.types import C, Q, T
from iautil_sql.types import Query, T

#T = TypeVar('T')
#P = ParamSpec('P')

#def log_query(logger: logging.Logger) -> Callable[
#        [Callable[Concatenate[Union[connection,cursor],str,P], T]],
#        Callable[Concatenate[Union[connection,cursor],str,P], T]]:
def log_query(logger: Logger) -> Callable[[Callable[...,T]],Callable[...,T]]:
#def log_query(logger: Logger) -> Callable[[C],C]:
    """
    Decorator function to log the executed SQL queries.
    """
    #def decorator(func: Callable[
    #        Concatenate[Union[connection,cursor],str,P], T]) -> Callable[
    #        Concatenate[Union[connection,cursor],str,P], T]:
    def decorator(func: Callable[...,T])->Callable[...,T]:
    #def decorator(func: C)->C:
        """
        Decorator function to log the executed SQL queries.
        """
        @wraps(func)
        def wrapper(conn: Union[connection,cursor],
                    sqlq:Query,
                    args:Union[
                        Optional[Union[Tuple,Dict]],
                        Union[Iterable[Union[Tuple, Dict]],
                              Iterator[Union[Tuple, Dict]]]]) -> T:
            """
            Wrapper function to log the executed SQL queries.
            """
            logger.debug('Executing query: %s\nParams: %s', sqlq, args)
            return func(conn, sqlq, args)
        return wrapper
    return decorator


def rollback_exception(func: Callable[...,T])->Callable[...,T]:
    """ Decorator function to rollback failed SQL queries """
    @wraps(func)
    def wrapper(conn:connection, *args, **kwargs) -> T:
        """ wrapper """
        try:
            return func(conn, *args, **kwargs)
        except PGError:
            #logger.error('Error: %s\n%s', e, format_exc())
            conn.rollback()
            raise
    return wrapper
