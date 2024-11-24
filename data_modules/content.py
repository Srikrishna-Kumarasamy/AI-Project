from dataclasses import dataclass
from typing import Optional, Dict, Union

@dataclass
class Content:
    title: str
    source: str
    url: str
    description: Union[str, Dict, None] = None
    additional_info: Optional[str] = None
