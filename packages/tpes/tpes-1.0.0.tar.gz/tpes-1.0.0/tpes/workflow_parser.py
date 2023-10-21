
from tpes.data.data_objects import DataObject
from typing import Dict
from tpes.data.connection import Connection
from tpes.data.node import NodeType, WorkflowNode
from lxml import etree as ET
from tpes.data.workflow import Workflow
from abc import *

class WorkflowParser(ABC):
    @abstractmethod
    def parse(self) -> Workflow:
        pass 


def get_meta(element) -> Dict[str, str]:
    metadata = [x for y in element.getchildren() for x in y if "metaData" in x.tag]
    return {d.attrib["name"]: d.getchildren()[0].text for d in metadata}

class XMLParser:
    def __init__(self, path: str) -> None:
        self.xml = ET.parse(path, ET.get_default_parser()).getroot()
    def xpath(self, path: str):
        return self.xml.xpath(path, namespaces=self.xml.nsmap)
class BPMNParser(WorkflowParser):
    def __init__(self, parser: XMLParser) -> None:
        self.xml = parser 
        self.node_type_mapping = {
            "startEvent": NodeType.START,
            "task": NodeType.TASK,
            "endEvent": NodeType.END,
            "parallelGateway": NodeType.PARALLEL,
            "exclusiveGateway": NodeType.EXCLUSION,
            "inclusiveGateway": NodeType.INCLUSION,
            "callActivity": NodeType.REUSABLE
        }
    
    def find_node_type(self, tag: str):
        for t, nt in self.node_type_mapping.items():
            if tag.endswith(t):
                return nt
        return NodeType.UNKNOWN

    def parse(self) -> Workflow:
        try:
            flows = self.xml.xpath("bpmn2:process/bpmn2:sequenceFlow")
            elements = sum([self.xml.xpath("bpmn2:process/bpmn2:%s" % t) for t in self.node_type_mapping.keys()], [])
            my_data_objects = self.xml.xpath("bpmn2:process/bpmn2:dataObject")
            elements = [WorkflowNode(e.attrib["id"], e.attrib.get("name", ""), get_meta(e), self.find_node_type(e.tag)) for e in elements]
            my_data_objects = [DataObject(e.attrib["id"], e.attrib.get("name", ""), get_meta(e)) for e in my_data_objects]
            connections: list[Connection] = []
            for flow in flows:
                src = flow.attrib["sourceRef"]
                tgt = flow.attrib["targetRef"]
                source_task = [elem for elem in elements if elem.id == src]
                target_task = [elem for elem in elements if elem.id == tgt]
                if len(source_task) == 1 and len(target_task) == 1:
                    connections.append(Connection(source_task[0], target_task[0]))
            return Workflow(elements,connections, my_data_objects)
        except IndexError:
            return None