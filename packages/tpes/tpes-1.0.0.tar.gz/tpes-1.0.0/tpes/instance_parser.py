
from abc import ABC, abstractmethod
from tpes.data.instance import * 

class InstanceParser(ABC):

    @abstractmethod
    def parse(self) -> Instance:
        pass 

class JSONInstanceParser(InstanceParser):

    def __init__(self, path: str) -> None:
        self.path = path 
        
    def parse(self) -> Instance:
        f = open(self.path)
        d = json.loads(f.read())
        return Instance.load(d)

