"""Review and validation models."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class SectionWordReport(BaseModel):
    section_name: str
    expected_range: str
    actual_words: int
    passed: bool

class ValidationReport(BaseModel):
    is_valid: bool
    missing_sections: List[str] = Field(default_factory=list)
    word_count_reports: Dict[str, SectionWordReport] = Field(default_factory=dict)
    total_words: int = 0
    ahimsa_passed: bool = True
    prohibited_issues_found: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class ReviewResult(BaseModel):
    chapter_id: int
    naya_name: str
    verdict: str  # "PASS" or "REVISE"
    doctrinal_score: int  # 1 to 10
    ahimsa_compliance: bool
    validation: ValidationReport
    feedback: str
    required_corrections: List[str] = Field(default_factory=list)
