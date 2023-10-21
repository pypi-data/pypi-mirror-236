
from dataclasses import asdict, dataclass, field
import json
from tpes.expression import ExpressionEvaluator
from typing import Any, Dict, Optional, Tuple
from tpes.data.node import NodeType
from tpes.data.workflow import * 
import dacite

@dataclass
class Instance:
    workflow: Workflow
    name: str 
    path: str 
    states: list[WorkflowNode]
    parent: Optional["Instance"] = field(default=None)
    tasks: list[tuple[WorkflowNode, bytes]] = field(default_factory=list)
    input_params: Dict[str, Any] = field(default_factory=dict)

    def is_running(self) -> bool:
        return not self.is_ready() and not self.is_completed()
    
    def is_ready(self) -> bool:
        return len(self.states) == 1 and self.states[0].type == NodeType.START
    
    def is_completed(self) -> bool:
        return all(node.type == NodeType.END for node in self.states)
    
    def clone(self, **kw) -> "Instance":
        return Instance(asdict(self), **kw)
    
    def to_dict(self):
        d = asdict(self)
        if d["workflow"] is not None:
            if d["workflow"]["data_objects"] == []:
                del d["workflow"]["data_objects"]
            if d["workflow"]["data_associations"] == []:
                del d["workflow"]["data_associations"]
        return d
    
    def save(self, path: str):
        def ser(obj):
            if isinstance(obj, bytes):
                return obj.hex()
            else:
                return obj
        f = open(path, "w")
        f.write(json.dumps(self.to_dict(), default=ser, indent=True))
        f.close()

    def load(data) -> "Instance":
        return dacite.from_dict(data_class=Instance, data=data, config=dacite.Config(type_hooks={
            NodeType: NodeType,
            bytes: bytes.fromhex,
            list[tuple[WorkflowNode, bytes]]: lambda x: [(y[0], y[1]) for y in x]
        }))

    def evaluate(self, node: WorkflowNode, key: str):
        start_node = [n for n in self.workflow.nodes if n.type == NodeType.START][0]
        if node == start_node:
            return node.metadata.get(key, 0)
        INPUT_DEFAULT_SUFFIX = "InputDefault"
        inputs = [i[:-len(INPUT_DEFAULT_SUFFIX)] for i in start_node.metadata.keys() if i.endswith(INPUT_DEFAULT_SUFFIX)]
        ids = {
            i: self.input_params.get(i, start_node.metadata["%sInputDefault" % i]) for i in inputs
        }
        ids["instance"] = self.name
        evaluator = ExpressionEvaluator(ids, self)
        return evaluator.evaluate(node.metadata.get(key, "0"))