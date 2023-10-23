import numpy as np

def cross_correlation2d(input_matrix, kernel, stride=1) -> np.ndarray:
        """ 
    Cross-correlation is similar to convolution, but with one of the inputs 
     flipped horizontally and vertically before performing the operation
    """
    
    if not isinstance(input_matrix, np.ndarray) or not isinstance(kernel, np.ndarray):
        raise ValueError("Both input_matrix and kernel must be 2D Numpy arrays.")
    if input_matrix.ndim != 2 or kernel.ndim != 2:
        raise ValueError("Both input_matrix and kernel must be 2D arrays.")
    if not isinstance(stride, int) or stride <= 0:
        raise ValueError("Stride must be a positive integer.")

    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape

    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1

    output_matrix = np.zeros((output_height, output_width), dtype=float)
    flipped_kernel = np.flip(np.flip(kernel, axis=0), axis=1)

    for i in range(0, input_height - kernel_height + 1, stride):
        for j in range(0, input_width - kernel_width + 1, stride):
            output_matrix[i // stride, j // stride] = np.sum(input_matrix[i:i+kernel_height, j:j+kernel_width] * flipped_kernel)

    return output_matrix