import pandas as pd
import os
from pathlib import Path


def load_sample_dataframe():
    """Load dataset CSV.

    Order of resolution:
    1. Path from PRODUCTS_CSV env var
    2. products.csv in project root (two levels above this file)
    3. raise FileNotFoundError with helpful message
    """
    # 1) env var
    env_path = os.environ.get('PRODUCTS_CSV')
    if env_path:
        p = Path(env_path)
        if p.exists():
            return pd.read_csv(p)
        else:
            raise FileNotFoundError(f"PRODUCTS_CSV is set but file not found: {p}")

    # 2) look for products.csv in project root
    this_file = Path(__file__).resolve()
    project_root = this_file.parents[1]
    candidate = project_root / 'products.csv'
    if candidate.exists():
        return pd.read_csv(candidate)

    # helpful error
    raise FileNotFoundError(
        f"products.csv not found. Expected at: {candidate}\n"
        "Either set the PRODUCTS_CSV environment variable to the CSV path, "
        "or place products.csv in the project root."
    )