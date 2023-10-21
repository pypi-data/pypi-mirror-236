from dataclasses import dataclass
from tpes.data.node import NodeType, WorkflowNode


@dataclass
class Task:
    name: str 
    time_hours: float 

def convert_to_task(node: WorkflowNode) -> Task:
    if node.type == NodeType.TASK:
        return Task(node.title, node.metadata.get("time", 0.1))
    elif node.type in [NodeType.PARALLEL, NodeType.INCLUSION, NodeType.EXCLUSION, NodeType.REUSABLE]:
        return Task("Plan %s" % node.title, 0.1)
    else:
        None

def convert_to_tasks(nodes: list[WorkflowNode]) -> list[Task]:
    return [convert_to_task(n) for n in nodes if convert_to_task(n) is not None]

