

from dataclasses import dataclass
from typing import Any
from tpes.data.node import * 

@dataclass(frozen=True)
class DataObject:
    id: str
    title: str 
    metadata: dict[str, Any]

    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, o: object) -> bool:
        return isinstance(o, DataObject) and self.id == o.id 

@dataclass
class DataAssociation:
    node: WorkflowNode
    data_object: DataObject