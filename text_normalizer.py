import re
import pandas as pd

def normalize_ingredient(name) -> str:
    """Convert to lowercase, strip, remove extra spaces. Handles NaN and non-strings."""
    if pd.isna(name):
        return ""
    name = str(name).strip().lower()
    name = re.sub(r'\s+', ' ', name)
    return name