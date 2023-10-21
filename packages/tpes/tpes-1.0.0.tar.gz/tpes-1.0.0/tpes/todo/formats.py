
from tpes.data.instance import Instance
from tpes.data.node import NodeType, WorkflowNode


def task_extract(node: WorkflowNode):
    if isinstance(node, WorkflowNode):
        if node.type == NodeType.REUSABLE:
            return lambda sm: ("Plan " + node.title, sm.instance.evaluate(node, "time"))
        else: 
            return lambda sm: (node.title, sm.instance.evaluate(node, "time"))
    else: return lambda sm: node


def extend_title(i: Instance, prefix: str, mytuple):
    title, time = mytuple
    return prefix + title, time


class TaskFormatter:

    def start(self):
        pass 
    def task_format(self, node, sm, prefix):
        raise NotImplementedError()
    
    def finish(self):
        pass 

def get_formatter(format) -> TaskFormatter:
    return {
        "orgmode": OrgFormatter(False),
        "orgmode+": OrgFormatter(True),
        "": DefaultFormatter(),
        "jira": JiraFormatter()
    }[format]


class DefaultFormatter(TaskFormatter):
    def task_format(self, node, sm, prefix):
        return "%s - %dh" % task_extract(node)(sm)

class OrgFormatter(TaskFormatter):
    def __init__(self, extended) -> None:
        self.extended = extended
    def task_format(self, node, sm, prefix):
        if not self.extended:
            return "*** TODO %s - %dh" % task_extract(node)(sm) if task_extract(node)(sm)[0] != "" else None
        else:
            return "*** TODO %s - %dh" % extend_title(sm.instance, prefix, task_extract(node)(sm)) if task_extract(node)(sm)[0] != "" else None
class JiraFormatter(TaskFormatter):
    def __init__(self) -> None:
        self.duedate = None 
        self.heading = "Summary,Hours\n"
    
    def task_format(self, node, sm, prefix):
        res = self.heading + "%s,%d" % extend_title(sm.instance, prefix, task_extract(node)(sm)) if task_extract(node)(sm)[0] != "" else None
        if res is not None:
            self.heading = ""
        return res 