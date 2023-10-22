from enum import Enum, auto


class NODETYPE(Enum):
    QUERY_MUTATION = auto()
    INPUT = auto()
    UNION = auto()
    CUSTOM_OBJ = auto()
