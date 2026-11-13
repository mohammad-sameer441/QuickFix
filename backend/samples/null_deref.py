"""
Benchmark 06: Missing Null / NoneType Check on Database Result
Type: Runtime Exception / Unhandled Null Reference
Status: Compiles cleanly.
Flaw: Dict / DB lookup returns None for nonexistent users; subsequent property access crashes server.
"""

from typing import Optional, Dict

accounts_db: Dict[str, dict] = {
    "usr_01": {"name": "Alice", "tier": "premium"}
}

def get_user_display_name(user_id: str) -> str:
    # Line 15: .get() returns None if user_id not found
    user = accounts_db.get(user_id)
    
    # Line 18: Unchecked dereference crashes with AttributeError / TypeError
    formatted_name = user["name"].upper()
    return f"Customer: {formatted_name} ({user['tier']})"
