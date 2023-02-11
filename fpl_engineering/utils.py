from pathlib import Path
import numpy as np

def get_project_root() -> Path:
    return Path(__file__).parent.parent


def transform_sequences(sequences, scaler, seq_len, n_features): 
    stacked = np.stack(sequences).reshape(-1,seq_len * n_features)
    return scaler.transform(stacked).reshape(-1,seq_len ,n_features)

def target_descaler(values):
    """
    generalized function to descale predicted value(s) from log by taking the exponent with an offset of 5

    Args: 
        values: int or iterable
    """
    v = np.exp(values) - 5
    if isinstance(values, (list, tuple)):
        return [int(round(y)) for y in v]
    return int(round(v))
