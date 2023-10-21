
import shutil
import jinja2
from tpes.instance_management import * 
from tpes.workflow_parser import BPMNParser, XMLParser
import os 

def get_tpes_path() -> str: 
    return os.environ.get("TPES_PATH", os.path.join(os.environ["HOME"], "tpes"))
class Environment:
    def get_config(self, name: str, default):
        config_path = os.path.join(get_tpes_path(), "config.json")
        if not os.path.exists(config_path):
            return default
        else:
            f = open(config_path)
            data = json.loads(f.read())
            return type(default)(data.get(name, os.environ.get("TPES_" + name.upper().replace(" ", "_"), default)))

    def find_workflow(self, name) -> Workflow:
        for p in self.get_config("workflow_search_dirs",[]) + ["./"]:
            for ext in ["", ".bpmn"]:
                wf = os.path.join(p, name + ext)
                if os.path.exists(wf):
                    return BPMNParser(XMLParser(wf)).parse()
        return None
    
    def find_instance(self, name) -> Instance:
        return JSONInstanceParser(self.get_instance_path(name)).parse()

    def get_instance_path(self, instance_name: str) -> str:
        for p in self.get_config("instance_search_dirs",[]) + ["./"]:
            for ext in ["", ".json"]:
                wf = os.path.join(p, instance_name + ext)
                if os.path.exists(wf):
                    return wf
        return None
    
    def list_instances(self) -> list[Instance]:
        return [
            JSONInstanceParser(os.path.join(get_tpes_path(), "instances", name)).parse() 
            for name in os.listdir(os.path.join(get_tpes_path(), "instances"))
        ]
    def get_document_template_path(self, doc_name: str) -> str:
        return os.path.join(get_tpes_path(), "templates", doc_name)

    def get_document_destination_path(self, instance: Instance, doc_name: str) -> str:
        return os.path.join(get_tpes_path(), "documents", instance.name, doc_name)

    def produce_document(self, instance: Instance, doc_name: str):
        template_path = self.get_document_template_path(doc_name)
        os.makedirs(os.path.dirname(self.get_document_destination_path(instance, doc_name)), exist_ok=True)
        if os.path.exists(template_path + ".j2"):
            t = jinja2.Template(open(template_path + ".j2").read())
            f = open(self.get_document_destination_path(instance, doc_name), "w")
            f.write(t.render(instance.input_params))
            f.close()
        else:
            shutil.copyfile(self.get_document_template_path(doc_name), self.get_document_destination_path(instance, doc_name))
            