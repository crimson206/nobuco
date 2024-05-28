from pydantic import BaseModel
from typing import List, Any, Dict

class Session(BaseModel):
    header: str
    content: str
    
class Item(BaseModel):
    name: str
    docs: str
    parsed_docs: List[Session] = []
    meta_data: Dict[str, Any] = {}

class ItemHolder(BaseModel):
    file_name: str
    items: List[Item] = []
    failed_items: List[str] = []
    meta_data: Dict[str, Any] = {}
