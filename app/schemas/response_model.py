from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    frame: str
    text: str
    pattern: str
    fix: str
    violations: List[str]
    mapped_violations: List[str]
