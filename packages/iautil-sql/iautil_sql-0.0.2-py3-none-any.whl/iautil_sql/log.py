""" Helper functions and decorators for SQL """

from functools import wraps
from logging import Logger
from typing import Callable, Dict, Iterator, Iterable, Optional, ParamSpec, Tuple, TypeVar, Union
#from typing import Concatenate

from psycopg2.extensions import connection, cursor

T = TypeVar('T')
P = ParamSpec('P')

#def log_query(logger: logging.Logger) -> Callable[
#        [Callable[Concatenate[Union[connection,cursor],str,P], T]],
#        Callable[Concatenate[Union[connection,cursor],str,P], T]]:
def log_query(logger: Logger) -> Callable[[Callable[...,T]],Callable[...,T]]:
    """
    Decorator function to log the executed SQL queries.
    """
    #def decorator(func: Callable[
    #        Concatenate[Union[connection,cursor],str,P], T]) -> Callable[
    #        Concatenate[Union[connection,cursor],str,P], T]:
    def decorator(func: Callable[...,T])->Callable[...,T]:
        """
        Decorator function to log the executed SQL queries.
        """
        @wraps(func)
        def wrapper(conn: Union[connection,cursor],
                    sqlq: str, args:Union[
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
