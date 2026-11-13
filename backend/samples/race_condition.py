"""
Benchmark 01: E-Commerce Wallet Balance Double-Spend / Race Condition
Type: Logical Concurrency Vulnerability
Status: Compiles cleanly, passes all static linters (flake8, pylint).
Flaw: Check-then-act race condition in withdraw/checkout logic where balance is validated,
an asynchronous payment gateway call occurs, and the balance is deducted afterwards.
Two simultaneous requests allow a user to spend the same balance twice.
"""

import time
import asyncio
from typing import Dict

user_wallets: Dict[str, float] = {
    "user_101": 100.0  # User has $100
}

async def process_checkout(user_id: str, item_id: str, price: float) -> bool:
    """
    VULNERABLE IMPLEMENTATION:
    1. Reads balance.
    2. Verifies balance >= price.
    3. Simulates external payment gateway I/O delay.
    4. Deducts balance.
    """
    current_balance = user_wallets.get(user_id, 0.0)
    
    # Line 28: Logical check without atomic lock or immediate reservation
    if current_balance < price:
        print(f"[{user_id}] Insufficient funds: {current_balance} < {price}")
        return False

    # Simulate network latency to payment gateway (I/O yield)
    # During this delay, a concurrent request can pass the check on line 28!
    await asyncio.sleep(0.1)

    # Line 37: Deduction happens too late!
    user_wallets[user_id] = current_balance - price
    print(f"[{user_id}] Purchased {item_id}! Remaining balance: {user_wallets[user_id]}")
    return True

# Reproduction test verifying the race condition
async def test_exploit_race_condition():
    user_wallets["user_101"] = 100.0
    # User fires two $80 purchases concurrently with $100 balance
    results = await asyncio.gather(
        process_checkout("user_101", "item_A", 80.0),
        process_checkout("user_101", "item_B", 80.0)
    )
    # If both succeed, balance becomes negative or doubled goods purchased: BUG!
    print(f"Test results: {results}, Final Balance: {user_wallets['user_101']}")
    assert user_wallets["user_101"] >= 0, "Double-spend occurred! Logical race vulnerability confirmed."
