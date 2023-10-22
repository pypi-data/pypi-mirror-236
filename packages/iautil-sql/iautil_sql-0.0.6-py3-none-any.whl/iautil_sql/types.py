""" Helper functions and decorators for SQL """

from pathlib import Path
from typing import (
    #Callable,
    Dict, List, Iterator, Iterable,
    Optional, Tuple, TypeVar, Union)

#from psycopg2.extensions import connection, cursor
from psycopg2.sql import SQL


# query args
QueryArg = Optional[Union[Tuple,Dict]]

# query arg list
QueryArgList = Union[Iterable[Union[Tuple, Dict]],
          Iterator[Union[Tuple, Dict]]]

# query
Query = Union[str,SQL]
QueryPath = Union[str,Path]
QueryPaths = Union[QueryPath, Iterable[QueryPath]]


# helpers (callable)
T = TypeVar('T', None, List[Tuple], Union[Tuple,None], List[List[Tuple]])
#C = TypeVar('C',
#              Callable[[connection,Q,A],T], # execute
#              Callable[[connection,Q,A],T], # select
#              Callable[[connection,Q,A],T], # select_single
#              Callable[[connection,Q,L],T], # execute_batch
#              Callable[[connection,Q,L],T], # select_batch
#              Callable[[cursor,str,A],T], # bulk_helper
#              Callable[[connection,List[Q],L],T], # execute_bulk
#              Callable[[connection,List[Q],L],T] # select_bulk
#)
