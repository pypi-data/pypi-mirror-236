
from dataclasses import dataclass, field
from typing import Any



dataclass
class TextItem:
    text: str = field(init=True)
    def __init__(self, text) -> None:
        self.text = text
@dataclass
class ListItem:
    items: list[Any]

@dataclass
class KeyValuePairsItem:
    pairs: list[tuple[str, Any]]

