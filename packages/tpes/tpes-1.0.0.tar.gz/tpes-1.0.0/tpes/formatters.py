
from abc import *
import dataclasses
from tpes.data.node import WorkflowNode
from tpes.data import workflow
from tpes.views.items import *
from typing import Any

class ViewFormatter(ABC):
    @abstractmethod
    def format(self, view: Any):
        pass 

class RichTextFormatter(ViewFormatter):
    def __init__(self) -> None:
        self.ident = 0
    def print(self, s, *args, **kw):
        print("  " * self.ident + s, *args, **kw)
    def inc(self):
        self.ident += 1
    def dec(self):
        self.ident -= 1
    def format(self, view: Any):
        if isinstance(view, TextItem):
            self.print(view.text)
        elif isinstance(view, ListItem):
            self.print("")
            self.inc()
            for e in view.items:
                self.format(e)
            self.dec()
        elif isinstance(view, WorkflowNode):
            self.print("")
            self.print("%s: %s" % (view.type, view.title))
            self.inc()
            for m, v in view.metadata.items():
                self.print("\t%s: %s" % (m,v))
            self.print("ID: %s" % view.id)
            self.dec()
        elif dataclasses.is_dataclass(view):
            self.print("")
            self.inc()
            for f in dataclasses.fields(view):
                self.print(f.name + ": ", end="")
                self.format(getattr(view, f.name))
            self.dec()
        else:
            print(view)