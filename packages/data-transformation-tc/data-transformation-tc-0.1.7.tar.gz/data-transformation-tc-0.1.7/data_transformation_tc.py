import numpy as np
from typing import Union, List

def transpose2d(input_matrix: List[List[Union[float, int]]]) -> List[List[Union[float, int]]]:
    """
    Transpose a 2D matrix
    
    Parameters:
    - input_matrix: A list of lists of real numbers (either float or int) representing a 2D matrix.
    
    Returns:
    - A list of lists of real numbers representing the transposed 2D matrix.
    """
    if not isinstance(input_matrix, list):
        raise ValueError("Input should be a list of lists.")
    
    row_length = len(input_matrix[0])
    for row in input_matrix:
        if not isinstance(row, list):
            raise ValueError("Each element of the input should be a list.")
        if len(row) != row_length:
            raise ValueError("All rows must have the same length.")
        for value in row:
            if not isinstance(value, (float, int)):
                raise ValueError("Each element of the inner lists should be a float or int.")
    
    return [list(row) for row in zip(*input_matrix)]

def window1d(input_array: Union[List[float], np.ndarray], size: int, shift: int = 1, stride: int = 1) -> Union[List[List[float]], List[np.ndarray]]:
    """
    Generate windows for a 1D array or list.
    
    Parameters:
    - input_array (Union[List[float], np.ndarray]): A list or 1D numpy array of real numbers.
    - size (int): The window size.
    - shift (int, optional): The shift (step size) between different windows. Default is 1.
    - stride (int, optional): The stride (step size) within each window. Default is 1.
    
    Returns:
    - Union[List[List[float]], List[np.ndarray]]: A list of lists or 1D numpy arrays of real numbers.
    """

    if size <= 0:
        raise ValueError("Size must be a positive integer.")
    if shift <= 0:
        raise ValueError("Shift must be a positive integer.")
    if stride <= 0:
        raise ValueError("Stride must be a positive integer.")
    if len(input_array) < size:
        raise ValueError("Input array must be longer than the window size.")
    
    windows = []
    for start in range(0, len(input_array) - size + 1, shift):
        if isinstance(input_array, np.ndarray):
            window = input_array[start:start + size:stride]
            windows.append(window)
        else:  
            window = input_array[start:start + size:stride]
            windows.append(list(window))
    
    return windows

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Compute the cross-correlation of a 2D input matrix with a kernel.

    Parameters:
    - input_matrix: A 2D numpy array.
    - kernel: A 2D numpy array.
    - stride: Stride value for the kernel.

    Returns:
    - A 2D numpy array of the result.
    """
    i_h, i_w = input_matrix.shape
    k_h, k_w = kernel.shape
    o_h = (i_h - k_h) // stride + 1
    o_w = (i_w - k_w) // stride + 1
    output = np.zeros((o_h, o_w))
    for x in range(0, i_h - k_h + 1, stride):
        for y in range(0, i_w - k_w + 1, stride):
            output[x // stride, y // stride] = np.sum(input_matrix[x:x+k_h, y:y+k_w] * kernel)
    return output
