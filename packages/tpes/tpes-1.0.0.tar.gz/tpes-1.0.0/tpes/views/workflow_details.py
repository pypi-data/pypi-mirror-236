from dataclasses import dataclass
from .items import * 

@dataclass
class WorkflowDetails:
    name: TextItem
    elements: ListItem
    connections: ListItem
    data_objects: ListItem