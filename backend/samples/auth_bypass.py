"""
Benchmark 02: Broken Access Control & IDOR in Order Management
Type: Logical Authorization Vulnerability
Status: Compiles cleanly, 0 linter warnings.
Flaw: Verifies that the user is authenticated, but fails to verify that the
authenticated user actually OWNS the order being updated or refunded.
"""

from typing import Optional, Dict

class UserSession:
    def __init__(self, user_id: str, is_authenticated: bool, role: str = "customer"):
        self.user_id = user_id
        self.is_authenticated = is_authenticated
        self.role = role

orders_db: Dict[str, dict] = {
    "ord_888": {"owner_id": "victim_42", "amount": 1250.00, "status": "CONFIRMED"},
    "ord_999": {"owner_id": "attacker_07", "amount": 15.00, "status": "CONFIRMED"}
}

def cancel_and_refund_order(session: UserSession, order_id: str) -> bool:
    """
    VULNERABLE LOGIC:
    Checks if the caller has a valid active session, but omits the ownership validation check.
    Any logged-in user can cancel and trigger refunds for ANY other customer's order.
    """
    # Line 27: Authenticated check only
    if not session or not session.is_authenticated:
        raise PermissionError("User must be logged in.")

    order = orders_db.get(order_id)
    if not order:
        raise ValueError("Order not found.")

    # MISSING SEMANTIC CHECK:
    # if order["owner_id"] != session.user_id and session.role != "admin":
    #     raise PermissionError("Access denied: You do not own this order.")

    # Line 39: State modification executes regardless of ownership!
    order["status"] = "REFUNDED"
    print(f"Order {order_id} successfully refunded by user {session.user_id}!")
    return True

def test_exploit_idor():
    attacker = UserSession(user_id="attacker_07", is_authenticated=True)
    # Attacker refunds Victim's $1,250 order
    success = cancel_and_refund_order(attacker, "ord_888")
    assert orders_db["ord_888"]["status"] == "REFUNDED", "Unauthorized refund succeeded!"
