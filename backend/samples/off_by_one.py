"""
Benchmark 03: Off-by-One Buffer & Pagination Sliding Window
Type: Boundary Condition / Logical Edge-Case Defect
Status: Compiles cleanly.
Flaw: Binary search or pagination slice where high boundary uses <= instead of <,
causing IndexError or reading uninitialized/next partition data.
"""

from typing import List, Optional

def fetch_paginated_records(dataset: List[dict], page_index: int, page_size: int) -> List[dict]:
    """
    VULNERABLE LOGIC:
    Calculates start and end indexes for window slicing, but incorrectly adds +1 to upper bound,
    leaking the first record of the subsequent page or throwing out of bounds when window reaches dataset end.
    """
    total = len(dataset)
    start_idx = page_index * page_size
    
    # Line 20: Flawed boundary logic (end_idx includes page_size + 1 elements)
    end_idx = start_idx + page_size + 1

    if start_idx >= total:
        return []

    # Slices 1 item too many, violating page contract
    return dataset[start_idx:end_idx]

def binary_search_boundary(sorted_list: List[int], target: int) -> int:
    low = 0
    # Line 31: Flaw: should be len(sorted_list) - 1
    high = len(sorted_list)

    while low <= high:
        mid = (low + high) // 2
        # Can trigger IndexError when target > all elements and mid reaches len(sorted_list)
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
