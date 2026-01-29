import numpy as np

def remove_dc_offset(samples: np.ndarray) -> np.ndarray:
    return samples - np.mean(samples)
