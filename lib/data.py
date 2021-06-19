import json
import pandas as pd


def load_from_tsv(path):
    return pd.read_csv(path, sep='\t')


def save_to_tsv(df: pd.DataFrame, path: str):
    return df.to_csv(path, sep='\t', index=False)


def save_to_json(data, path, indent=3):
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def load_from_json(path):
    with open(path, 'rb') as f:
        data = json.load(f)
    return data
