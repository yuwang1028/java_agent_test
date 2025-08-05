import re
from pydantic import BaseModel
from typing import List

# Result model for inspector
class ObservabilityIssue(BaseModel):
    file: str
    method: str
    issue: str

def inspect_observability(file_path: str, method_name: str, method_content: str) -> List[ObservabilityIssue]:
    """
    Simple static rule inspection:
    - Check if method has trace/span/log instrumentation.
    """
    issues = []
    # Rule 1: trace/span
    if not re.search(r"tracer\.spanBuilder|@WithSpan", method_content):
        issues.append(ObservabilityIssue(
            file=file_path,
            method=method_name,
            issue="Missing trace/span instrumentation"
        ))
    # Rule 2: logging presence
    if not re.search(r"Logger|System\.out\.println|log\(", method_content):
        issues.append(ObservabilityIssue(
            file=file_path,
            method=method_name,
            issue="Missing logging"
        ))
    return issues
