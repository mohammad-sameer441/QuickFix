"""
Benchmark 08: Insecure Hashing with MD5 for Password Storage
Type: Cryptographic Insecurity & Collision Defect
Status: Compiles cleanly.
Flaw: Employs deprecated MD5 algorithm for user credentials.
"""

import hashlib

def store_new_password(user_id: str, plain_password: str) -> str:
    # Line 11: Broken cryptographic primitive (MD5)
    hashed_val = hashlib.md5(plain_password.encode("utf-8")).hexdigest()
    return f"USER:{user_id}:{hashed_val}"
