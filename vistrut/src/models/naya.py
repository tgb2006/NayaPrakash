"""Naya Prakash Book Core Models."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class NayaCatalogItem(BaseModel):
    id: int
    khanda_id: int
    khanda_name: str
    name_hindi: str
    name_sanskrit: str
    category: str
    aspect: str
    definition_brief: str
    status: str = "pending"

class KhandaDefinition(BaseModel):
    id: int
    slug: str
    name_hindi: str
    root_naya: str
    sanskrit_name: str
    primary_division: str
    tri_aspect: str
    chapters_count: int
    range: List[int]
    core_sutra: str
    agamic_definition: str
    philosophical_essence: str

class ExampleItem(BaseModel):
    id: int
    chapter_id: int
    naya_name: str
    example_number: int
    title: str
    theme: str
    core_incident_summary: str
    keywords: List[str] = Field(default_factory=list)

class ChapterSection(BaseModel):
    number: int
    title: str
    content: str
    word_count: int = 0

class ChapterMetadata(BaseModel):
    id: int
    naya_name_hindi: str
    khanda_id: int
    file_path: Optional[str] = None
    total_words: int = 0
    section_word_counts: Dict[str, int] = Field(default_factory=dict)
    is_valid: bool = False
