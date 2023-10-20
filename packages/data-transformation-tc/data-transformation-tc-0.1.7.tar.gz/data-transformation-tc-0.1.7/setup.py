# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['data_transformation_tc']
install_requires = \
['numpy>=1.24.2,<2.0.0']

setup_kwargs = {
    'name': 'data-transformation-tc',
    'version': '0.1.7',
    'description': 'data_transformation_tc is a Python library designed to streamline common data transformations required in machine learning and data science workflows, such as transpose a matrix, create time series windows, or apply 2D convolution',
    'long_description': '# data_transformation_tc\n\n### Overview\n\ndata_transformation_tc is a Python library designed to streamline common data transformations required in machine learning and data science workflows, such as transpose a matrix, create time series windows, or apply 2D convolution.\n\n### Features\n\n1. Transpose: Quickly transpose any 2D matrix with the transpose2d function.\n2. Time Series Windowing: Generate windows for your 1D data arrays or lists with the window1d function. Customize window size, shift, and stride as per your needs.\n3. 2D Convolution: Apply 2D convolution on matrices using the convolution2d function. This function computes the cross-correlation of an input matrix with a specified kernel.\n\n### Installation\n\nTo install the data_transforms package, use pip:\n\n`pip install data-transformation-tc`\n\n### Usage\n\nA quick example to get you started:\n\n```python\nfrom data_transformation_tc import transpose2d, window1d, convolution2d\nimport numpy as np\nfrom typing import Union, List\n\n# Transpose a matrix\nmatrix = [\n    [1.0, 2.0, 3.0],\n    [4.0, 5.0, 6.0],\n    [7.0, 8.0, 9.0]\n]\ntransposed_matrix = transpose2d(matrix)\nprint(transposed_matrix)\n\n# Create time series windows\ninput_data = np.array([0, 1, 2, 3, 4, 5, 6])\nwindows = window1d(input_data, size=3, shift=1, stride=2)\nprint(windows)\n\n# Apply 2D convolution\ninput_matrix = np.array([\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n])\nkernel = np.array([\n    [1, 0],\n    [0, -1]\n])\nconv_result = convolution2d(input_matrix, kernel)\nprint(conv_result)\n\n\n```',
    'author': '______________',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
