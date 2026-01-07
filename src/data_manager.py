import pandas as pd

def load_users():
    try:
        return pd.read_csv("data/users.csv").to_dict('records')
    except:
        return []

def load_listings():
    try:
        return pd.read_csv("data/listings.csv").to_dict('records')
    except:
        return []
