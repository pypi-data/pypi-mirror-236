"""
This module conatins some useful process management functions. 
"""

__all__ = ["is_worker"]





def is_worker() -> bool:
    """
    Returns True if the LocalProcess is a Worker process (used to execute tasks given by its parent).
    """
    return False