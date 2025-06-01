import pandas as pd

def load_data(filepath):
    """
    Load EPL match data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded match data.
    """
    return pd.read_csv(filepath)
