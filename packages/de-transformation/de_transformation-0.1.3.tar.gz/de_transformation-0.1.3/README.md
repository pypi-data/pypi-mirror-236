### Advanced Python & Linux Shell Commands: Project

## Python package project

### Description
This project has a python package <code>de-transformation</code> code to make data transformations. The package consists of 3 functions:
 * transpose2d
 * window1d
 * convolution2d


### transpose2d

#### Description

Transposes a 2D matrix.

#### Parameters

- `input_matrix` (list[list[float]]): The input 2D matrix to be transposed.

#### Return Value

- `list[list[float]]`: The transposed 2D matrix, where rows become columns and columns become rows.

#### Example

```python
from de_transformation.utils import transpose2d

# Example input matrix
input_matrix = [[1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]]

# Transpose the matrix
transposed_matrix = transpose2d(input_matrix)

# Output:
# transposed_matrix is now:
# [[1.0, 4.0],
#  [2.0, 5.0],
#  [3.0, 6.0]]
```
### window1d

#### Description

Extracts window sub-arrays from a 1D list or numpy array, with the option to specify the size of the windows,
the shift for the starting position of the window, and the stride between consecutive windows.

#### Parameters

- `input_array` (list or np.ndarray): The input 1D array or list from which windows are extracted.
- `size` (int): The size of the windows to extract.
- `shift` (int, optional): The number of elements to shift the starting position of the window (default is 1).
- `stride` (int, optional): The step size between consecutive windows (default is 1).

#### Return Value

- `list of lists or np.ndarrays`: A list containing windows of the specified size extracted from the input array.

#### Example

```python
from de_transformation.utils import window1d

# Example input array
input_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Extract windows of size 3 with a shift of 2
windows = window1d(input_array, size=3, shift=2)

# Output:
# windows is now:
# [[1, 2, 3],
#  [3, 4, 5],
#  [5, 6, 7],
#  [7, 8, 9]]
```

### convolution2d

#### Description

Performs 2D convolution on a numpy array using a specified convolution kernel and stride.

#### Parameters

- `input_matrix` (numpy.ndarray): The input 2D matrix to be convolved.
- `kernel` (numpy.ndarray): The convolution kernel (filter) to apply.
- `stride` (int, optional): The stride for the convolution operation (default is 1).

#### Return Value

- `numpy.ndarray`: The result of the 2D convolution operation, which is a numpy array.

#### Usage Example

```python
from de_transformation.utils import convolution2d

# Example input matrix
input_matrix = np.array([[1, 2, 3],
                         [4, 5, 6],
                         [7, 8, 9]])

# Example kernel
kernel = np.array([[1, 0],
                   [0, -1]])

# Perform 2D convolution
result = convolution2d(input_matrix, kernel)

# Output:
# result is now:
# [[  1.  -2.]
#  [ -1.  -2.]]
