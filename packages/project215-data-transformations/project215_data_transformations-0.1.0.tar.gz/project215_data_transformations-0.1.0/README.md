## Introduction

In this project, the goal was to build and publish a python package to PyPI via poetry.

Data Transformations is a Python package that provides 3 functions for data transformation tasks. It includes functions for 2D matrix operations, 1D windowing, and 2D cross-correlation. This package is designed to help data scientists internally.

## Installation

You can install Data Transformations using `pip`:

```bash
pip install data-transformations
```
## Usage

Here's how you can use the functions from Data Transformations in your Python code:


```python

from data_transformations import transpose2d, window1d, cross_correlation2d

# Example usage of the transpose2d function
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = transpose2d(matrix)
print(transposed)

# Example usage of the window1d function
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
windows = window1d(data, size=3, shift=1, stride=1)
print(windows)

# Example usage of the cross_correlation2d function
import numpy as np
input_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
kernel = np.array([[0, 1], [1, 0]])
result = cross_correlation2d(input_matrix, kernel, stride=1)
print(result)
```
