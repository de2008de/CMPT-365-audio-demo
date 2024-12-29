import numpy as np


class UniformQuantizer:
    def __init__(self):
        self.resampled_data = None
    
    def quantize(self, data, bits):
        min_val = np.min(data)
        max_val = np.max(data)
        levels = 2 ** bits
        step_size = (max_val - min_val) / levels
        resampled_data = np.round((data - min_val) / step_size) * step_size + min_val
        return resampled_data
