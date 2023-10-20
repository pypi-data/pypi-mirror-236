# data_transformation_tc

### Overview

data_transformation_tc is a Python library designed to streamline common data transformations required in machine learning and data science workflows, such as transpose a matrix, create time series windows, or apply 2D convolution.

### Features

1. Transpose: Quickly transpose any 2D matrix with the transpose2d function.
2. Time Series Windowing: Generate windows for your 1D data arrays or lists with the window1d function. Customize window size, shift, and stride as per your needs.
3. 2D Convolution: Apply 2D convolution on matrices using the convolution2d function. This function computes the cross-correlation of an input matrix with a specified kernel.

### Installation

To install the data_transforms package, use pip:

`pip install data-transformation-tc`

### Usage

A quick example to get you started:

```python
from data_transformation_tc import transpose2d, window1d, convolution2d
import numpy as np
from typing import Union, List

# Transpose a matrix
matrix = [
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0]
]
transposed_matrix = transpose2d(matrix)
print(transposed_matrix)

# Create time series windows
input_data = np.array([0, 1, 2, 3, 4, 5, 6])
windows = window1d(input_data, size=3, shift=1, stride=2)
print(windows)

# Apply 2D convolution
input_matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
kernel = np.array([
    [1, 0],
    [0, -1]
])
conv_result = convolution2d(input_matrix, kernel)
print(conv_result)


```