"""
Benchmark 05: Unclosed File Descriptor & Resource Exhaustion Leak
Type: Operating System Resource Management Flaw
Status: Compiles cleanly.
Flaw: Opens file descriptors in a high-frequency loop without a deterministic 'with' context manager.
Exceptions during read/processing cause file descriptor exhaustion.
"""

def process_transaction_logs(log_paths):
    records = []
    for path in log_paths:
        # Line 12: File handle acquired without context manager
        f = open(path, "r", encoding="utf-8")
        data = f.read()
        
        # If parsing fails or exception occurs, f.close() is never reached
        records.append(data.strip())
        f.close()
    return records
