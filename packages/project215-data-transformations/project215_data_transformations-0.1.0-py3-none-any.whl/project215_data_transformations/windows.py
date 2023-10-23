import numpy as np

def window1d(input_array, size, shift=1, stride=1) -> list[list | np.ndarray]:
    if not isinstance(input_array, (list, np.ndarray)):
        raise ValueError("Input must be a list or 1D NumPy array.")
    if not isinstance(size, int) or size <= 0:
        raise ValueError("Size must be a positive integer.")
    if not isinstance(shift, int) or shift <= 0:
        raise ValueError("Shift must be a positive integer.")
    if not isinstance(stride, int) or stride <= 0:
        raise ValueError("Stride must be a positive integer.")
    
    if isinstance(input_array, list):
        input_array = np.array(input_array)

    num_samples = len(input_array)
    windows = []

    for start in range(0, num_samples - size + 1, shift):
        end = start + size
        window = input_array[start:end:stride]
        windows.append(window)

    return windows