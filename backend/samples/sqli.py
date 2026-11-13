"""
Benchmark 04: SQL Injection in User Authentication Query
Type: Logical Data Sanitization & Security Vulnerability
Status: Compiles cleanly, 0 static linter errors.
Flaw: Unsanitized dynamic string formatting directly in SQL cursor.execute(),
allowing authentication bypass via classic payload: ' OR '1'='1
"""

import sqlite3

def query_user_record(username: str, password_hash: str):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INT, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'admin', '5f4dcc3b5aa765d61d8327deb882cf99')")

    # Line 17: Vulnerable SQL query construction via dynamic f-string
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"
    print(f"Executing: {query}")
    cursor.execute(query)
    
    return cursor.fetchone()
