import random

def fetch_credit_score(mobile: str) -> int:
    """
    Mock Credit Score API.
    In real world, this would call an actual CIBIL/Experian API.
    Mentioned clearly in README.
    """
    try:
        score = random.randint(300, 900)
        return score
    except Exception:
        # Graceful failure - return None so caller can handle it
        return None
