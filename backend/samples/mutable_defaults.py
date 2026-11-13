"""
Benchmark 07: Cross-Request State Leakage via Mutable Default Arguments
Type: Python Interpreter State Contamination Defect
Status: Passes flake8, pylint without warnings.
Flaw: Def initializes default argument items=[] which is created only once.
Different user requests share the same list instance, leaking sensitive records.
"""

def append_audit_trail(event_name: str, payload: dict, audit_log: list = []):
    # Line 10: audit_log persists across separate invocations!
    audit_log.append({"event": event_name, "data": payload})
    return audit_log
