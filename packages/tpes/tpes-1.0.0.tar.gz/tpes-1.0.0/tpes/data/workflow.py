
from dataclasses import dataclass, field
from tpes.data.data_objects import DataAssociation, DataObject
from typing import List
from tpes.data.node import WorkflowNode
from tpes.data.connection import Connection

@dataclass
class Workflow:
    nodes: list[WorkflowNode]
    connections: list[Connection]
    data_objects: list[DataObject] = field(default_factory=list)
    data_associations: list[DataAssociation] = field(default_factory=list)

    def find_node(self, node_id: str) -> WorkflowNode:
        nodes = [n for n in self.nodes if n.id == node_id]
        if len(nodes) == 0:
            return None 
        else:
            return nodes[0]
    
    def get_next(self, node: WorkflowNode) -> List[WorkflowNode]:
        return [conn.target for conn in self.connections if conn.source == node]
    
    def get_prev(self, node: WorkflowNode) -> List[WorkflowNode]:
        return [conn.source for conn in self.connections if conn.target == node]
    
    def is_reachable(self, start, end):
        if start == end:
            return True 
        visited = []
        q = [start] 
        while len(q) != 0:
            x, *q = q
            if x not in visited:
                visited.append(x)
                q = q + self.get_next(x)
        return end in visited