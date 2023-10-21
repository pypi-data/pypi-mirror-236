
from abc import ABC, abstractmethod
from enum import Enum
from hashlib import sha256
from inspect import istraceback
from types import TracebackType
from tpes.data import workflow
from typing import Any, Callable, Tuple
from tpes.data import instance
from tpes.data.instance import * 
from tpes.instance_parser import * 


class InstanceWriter(ABC):
    @abstractmethod
    def write(self, instance: Instance):
        pass 

class JSONInstanceWriter(InstanceWriter):
    def write(self, instance: Instance):
        instance.save(instance.path)

class InstanceFactory(InstanceParser):
    def __init__(self, workflow: Workflow, name: str, inputs: dict[str, Any] = {}, parent = None) -> None:
        self.workflow = workflow
        self.name = name
        self.inputs = inputs
        self.parent = parent

    def parse(self) -> Instance:
        return Instance(self.workflow, self.name, "", [node for node in self.workflow.nodes if node.type == NodeType.START], self.parent)

class TransitionRequest(Enum):
    MANUAL_INTERVENTION = 0
    SELECT_ONE = 1
    SELECT_SUNSET = 2
    CREATE_CHILD_INSTANCES = 3
    WAITING = 4


@dataclass
class StateTransition:
    initial: WorkflowNode
    request: Optional[TransitionRequest]
    new_states: list[WorkflowNode]

class InstanceStateMachine:
    def __init__(self, instance: Instance) -> None:
        self.instance = instance 
        
    def next(self, state: WorkflowNode) -> StateTransition:
        next_states = self.instance.workflow.get_next(state)
        if len([s for s in self.instance.states if self.instance.workflow.is_reachable(s, state)]) > 1:
            return StateTransition(state, TransitionRequest.WAITING, [state])
        return {
            NodeType.START: lambda n: StateTransition(state, None, next_states) if n == 1 else None,
            NodeType.TASK: lambda n: StateTransition(state, None, next_states) if n == 1 else None,
            NodeType.END: lambda n: StateTransition(state, None, []) if n == 0 else None,
            NodeType.EXCLUSION: lambda n: StateTransition(state, TransitionRequest.SELECT_ONE, next_states) if n > 0 else None,
            NodeType.INCLUSION: lambda n: StateTransition(state, TransitionRequest.SELECT_SUNSET, next_states) if n > 0 else None, 
            NodeType.PARALLEL: lambda n: StateTransition(state, None, next_states) if n > 0 else None,
            NodeType.REUSABLE: lambda n: StateTransition(state, TransitionRequest.CREATE_CHILD_INSTANCES, next_states) if n == 1 else None
        }[state.type](len(next_states))
    
    def follow(self, state: WorkflowNode) -> Tuple[WorkflowNode, list[StateTransition]]:
        transitions = [] 
        transitions.append(self.next(state))
        while self.next(state).request is None and len(self.next(state).new_states) == 1:
            state = self.next(state).new_states[0]
            transitions.append(self.next(state))
        return (state, transitions)

    def manual_transition(self, transition: StateTransition, states):
        return states
    
    def select_subset(self, transition: StateTransition, filter: Callable[[WorkflowNode], bool]) -> list[WorkflowNode]:
        return [state for state in transition.new_states if filter(state)]
    
    def select_one(self, transition: StateTransition, state: WorkflowNode) -> list[WorkflowNode]:
        if state in transition.new_states:
            return [state]
        else:
            raise ValueError("Selected state not in list of possibl4e next states")
    
    def hash_task_with_history(self, node: WorkflowNode, previous_task_hashes: list[bytes]) -> bytes:
        def hash_task(task: WorkflowNode) -> bytes:
            return sha256(task.title.encode("utf-8")).digest()
        if previous_task_hashes == [] or previous_task_hashes is None:
            return hash_task(node)
        else:
            result = sha256(previous_task_hashes[0]).digest()
            for t in previous_task_hashes[1:]:
                result = sha256(result + t).digest()
            return sha256(result + hash_task(node)).digest()
    
    def advance(self, previous_tasks: List[Tuple[WorkflowNode, bytes]] = None) -> list[Tuple[WorkflowNode, bytes]]:
        def task_history(first, previous_tasks):
                return [y for x,y in previous_tasks if self.instance.workflow.is_reachable(x, first) and x != first]
        followups = [self.follow(state) for state in self.instance.states]
        track_start = []
        tasks = []
        if previous_tasks is not None:
            for _, transitions in followups:
                first = transitions[0].initial
                past = task_history(first, previous_tasks)
                if (first, self.hash_task_with_history(first, past)) not in previous_tasks:
                    track_start += [transitions[0].initial]
        else:
            track_start = [transitions[0].initial for _, transitions in followups]
        self.instance.states = list(set([newstate for newstate, _ in followups]))
        tasks = track_start + [transition.initial for _, transitions in followups for transition in transitions[1:]]
        result = [] 
        history_hashes = [] 
        if previous_tasks is not None:
            history_hashes = [h for t,h in previous_tasks]
        for task in tasks:
            if task not in [x[0] for x in result]:
                h = self.hash_task_with_history(task, history_hashes)
                history_hashes.append(h)
                result.append((task, h))
        if previous_tasks is not None:
            return [x for x in result if x not in previous_tasks]
        else:
            return result 