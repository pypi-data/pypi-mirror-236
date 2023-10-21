

from dataclasses import dataclass
from typing import Any
from enum import Enum, IntEnum

class NodeType(IntEnum):
    UNKNOWN = 0 
    TASK = 1
    REUSABLE = 2
    INCLUSION = 3
    EXCLUSION = 4 
    PARALLEL = 6
    START = 7
    END = 8


@dataclass(frozen=True)
class WorkflowNode:
    id: str
    title: str 
    metadata: dict[str, Any]
    type: NodeType

    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, o: object) -> bool:
        return isinstance(o, WorkflowNode) and self.id == o.id 