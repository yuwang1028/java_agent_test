from typing import List
from pydantic import BaseModel

# Result model for validation output
class ValidationResult(BaseModel):
    score: int
    status: str
    message: str

def validate_observability(issues: List):
    """
    Simple scoring:
    - Start from 100 points
    - -10 per issue
    - Pass >=60
    """
    score = max(0, 100 - len(issues) * 10)
    status = "pass" if score >= 60 else "fail"
    message = f"Found {len(issues)} observability issues."
    return ValidationResult(score=score, status=status, message=message)
