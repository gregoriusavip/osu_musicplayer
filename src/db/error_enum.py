from enum import Enum

class Error(Enum):
    SUCCESS = 1
    PATH_ERROR = 2
    SQL_CONNECTION_ERROR = 3
    SQL_EXECUTE_ERROR = 4
    SQL_ERROR = 5   # General SQL Error