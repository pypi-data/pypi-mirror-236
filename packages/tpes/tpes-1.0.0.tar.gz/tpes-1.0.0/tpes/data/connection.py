
from dataclasses import dataclass
from tpes.data import WorkflowNode

@dataclass
class Connection:
    source: WorkflowNode
    target: WorkflowNode