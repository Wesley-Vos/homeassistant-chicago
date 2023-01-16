from dataclasses import dataclass
from typing import List


@dataclass
class ChicagoData:
    all_options: List[str]
    selected_option: str
