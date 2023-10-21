from dataclasses import asdict
from tpes.data.node import NodeType, WorkflowNode
from tpes.ui import CLIResolveWizzard, resolve
from tpes.todo.formats import get_formatter
from tpes.environment import Environment
from tpes.data.instance import Instance
from tpes.instance_parser import InstanceParser, JSONInstanceParser
from tpes.instance_management import InstanceFactory, InstanceStateMachine, InstanceWriter, JSONInstanceWriter, TransitionRequest
from tpes.views.items import *
from tpes.data.workflow import Workflow
from tpes.views.workflow_details import WorkflowDetails
from tpes.workflow_parser import BPMNParser, XMLParser
import os.path
import os 

class Error:
    def __init__(self, msg) -> None:
        self.msg = msg
    
    def __str__(self) -> str:
        return self.msg

def get_workflow(path: str) -> Workflow:
    env = Environment()
    return env.find_workflow(path) 
def get_intance_candidates():
    return [ x for x in os.listdir(os.getcwd()) if x.endswith(".json")]

def get_instance_state_machine(instance_path: str) -> InstanceStateMachine:
    if instance_path == "" and len(get_intance_candidates()) == 1:
        instance_path = get_intance_candidates()[0]
    parser = JSONInstanceParser(instance_path)
    instance: Instance = parser.parse()
    return InstanceStateMachine(instance)

class CommandExecutor:
    def read(self, workflow: (str, "Workflow given to be displayed")):
        workflow_obj = get_workflow(workflow)
        return WorkflowDetails(TextItem(workflow), ListItem(workflow_obj.nodes), ListItem(workflow_obj.connections), ListItem(workflow_obj.data_objects))
    def show(self, workflow: str, id: str):
        workflow_obj = get_workflow(workflow)
        return workflow_obj.find_node(id)
    def next(self, id: str, workflow: str, *, show_ids_only: bool = False):
        workflow_obj = get_workflow(workflow)
        mynode = workflow_obj.find_node(id)
        if mynode is not None:
            if show_ids_only:
                return "\n".join([n.id for n in workflow_obj.get_next(mynode)])
            else:
                return ListItem(workflow_obj.get_next(mynode))
        else:
            return None
    def start(self, instance: str, *, workflow: str = None, parent_instance: str = None):
        instance_path = instance
        workflow_path = workflow
        if parent_instance is not None and workflow is None:
            pi = get_instance_state_machine(parent_instance).instance
            workflow_path = pi.evaluate(pi.states[0], "path")
        workflow = get_workflow(workflow_path)
        if workflow is None:
            return Error("No workflow found")
        instance_name = os.path.basename(instance_path)
        if instance_name.endswith(".json"):
            instance_name = instance_name[:-5]
        factory = InstanceFactory(workflow, instance_name, {}, None)
        instance:Instance = factory.parse()
        instance.path = instance_path
        print("Parent path: %s" % parent_instance)
        if parent_instance is not None:
            print("Path is not none")
            instance.parent = get_instance_state_machine(parent_instance).instance
        writer = JSONInstanceWriter()
        writer.write(instance)
        env = Environment()
        for do in instance.workflow.data_objects:
            print("Producing " + do.title)
            env.produce_document(instance, do.title)
        return instance 
    def state(self,*, instance: str = "", show_all: bool = False, show_ids_only: bool = False):
        instance_path = instance
        if show_all:
            return get_instance_state_machine(instance_path).instance
        else:
            if not show_ids_only:
                return ListItem(get_instance_state_machine(instance_path).instance.states)
            else:
                return "\n".join([
                    state.id for state in get_instance_state_machine(instance).instance.states
                ])
    def next_states(self, *, instance: str = ""):
        sm = get_instance_state_machine(instance)
        return {
            state.id: sm.instance.workflow.get_next(state) for state in sm.instance.states
        }
    def info(self, *, instance: str = ""):
        i = get_instance_state_machine(instance).instance
        if i.parent is not None:
            print("Parent available")
            i.parent = i.parent.name
        return i
    def follow(self, *, instance: str = "", save: bool = False):
        sm = get_instance_state_machine(instance)
        tasks = sm.advance(sm.instance.tasks)
        if save:
            sm.instance.tasks += tasks
            writer = JSONInstanceWriter()
            writer.write(sm.instance)
        return ListItem([x[0] for x in tasks])
    
    def resolve(self, *, instance: str = "", state: str = ""):
        sm = get_instance_state_machine(instance)
        state = sm.instance.workflow.find_node(state) if state != "" else sm.instance.states[0]
        writer = JSONInstanceWriter()
        result = resolve(sm, state, CLIResolveWizzard())
        writer.write(result)
        return ListItem(result.states)
    def todo(self, *, instance: str = "", add_prefix: bool = True, group_by_hours: int = 0, format: str = ""):
        formatter = get_formatter(format)
        formatter.start()
        sm = get_instance_state_machine(instance)
        prefix = ""
        if add_prefix:
            i = sm.instance
            while i is not None:
                prefix = "%s: %s" % (i.name,  prefix)
                i = i.parent
        result = [] 
        if group_by_hours > 0:
            todo = [] 
            sumh = 0
            for task, h in sm.instance.tasks:
                if task.type == NodeType.REUSABLE:
                    task = WorkflowNode(**dict(asdict(task), title = "Plan " + task.title))
                time = sm.instance.evaluate(task, "time")
                if time == 0: time = 0.1
                if sumh + time > group_by_hours:
                    result.append((", ".join([x.title for x in todo if x.title != ""]), group_by_hours))
                    todo = [task] 
                    sumh = time
                else:
                    todo.append(task)
                    sumh += time
            if len(todo) > 0:
                result.append((", ".join([x.title for x in todo if x.title != ""]), group_by_hours))
            result = [formatter.task_format(x, sm, prefix) for x in result]
        else:
            for task, h in sm.instance.tasks:
                result.append(formatter.task_format(task, sm, prefix))
        output =  "\n".join([x for x in result if x is not None])
        formatter.finish()
        return output
    def clone(self, source: str, destination: str):
        instance = get_instance_state_machine(source).instance
        new_instance = Instance(
            input_params=instance.input_params,
            name=destination.replace(".json", ""),
            parent=instance.parent,
            path=destination,
            states=instance.states,
            tasks=instance.tasks,
            workflow=instance.workflow,
        )
        writer = JSONInstanceWriter()
        writer.write(new_instance)
        env = Environment()
        for do in new_instance.workflow.data_objects:
            print("Producing " + do.title)
            env.produce_document(new_instance, do.title)