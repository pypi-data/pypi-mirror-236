import numpy as np

def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    Transpose a 2D matrix.

    Args:
        input_matrix (list[list[float]]): The input 2D matrix to be transposed.

    Returns:
        list[list[float]]: The transposed 2D matrix.

    """
    #validations
    assert isinstance(input_matrix, list), 'input_matrix has to be a list.'
    assert input_matrix, 'input_matrix has to have lists of floats.'
    assert all(isinstance(row, list) and all(isinstance(val, float) for val in row) for row in input_matrix), 'input_matrix has to contain lists of floats'

    nrow = len(input_matrix)
    ncol = len(input_matrix[0])
    #create output list containing all the rows (lists)
    out = []
    for _ in range(ncol):
        out.append([])
    #iterate through elements and add them to the new matrix
    for col in range(ncol):
        for row in range(nrow):
            out[col].append(input_matrix[row][col])

    return out


def window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]:
    """
    Extract window sub-arrays from list or numpy array with optional shift and stride

    Args:
        input_array (list or np.ndarray): The input 1D array or list from which windows are extracted.
        size (int): The size of the windows to extract.
        shift (int, optional): The number of elements to shift the starting position of the window (default is 1).
        stride (int, optional): The step size between consecutive windows (default is 1).

    Returns:
        list of lists or np.ndarrays: A list containing windows of the specified size extracted from the input array.

    Size, shift and stride parameters are supposed to be positive integers.
    """  
    #validations
    assert isinstance(input_array, (list,np.ndarray)), 'input_array has to be list or numpy.ndarray.'

    parameters = {'size':size, 'shift':shift, 'stride':stride}
    for p in parameters.keys():
        assert isinstance(parameters[p], int), f'{p} has to be positive integer.'
        assert parameters[p] > 0, f'{p} has to be positive integer.'
        assert parameters[p] < len(input_array), f'{p} has to be smaller the a length of input_array.'
    
    out_lst = []
    first = 0
    #maximum of len(input_array) iterations
    for n in range(len(input_array)):
        #first window element
        first = n*shift
        #last is the first plus size times of steps
        last = first + stride * size
        #slice the original list or np.array
        new_lst = input_array[first:last:stride]

        #break if list is smaller then window size
        if(len(new_lst) < size):
            break
        
        out_lst.append(new_lst)

    return out_lst


def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride : int = 1) -> np.ndarray:
    """
    Perform 2D convolution for numpy array.

    Args:
        input_matrix (numpy.ndarray): The input 2D matrix to be convolved.
        kernel (numpy.ndarray): The convolution kernel (filter) to apply.
        stride (int, optional): The stride for the convolution operation (default is 1).

    Returns:
        numpy.ndarray: The result of the 2D convolution operation.
    """
    #validations
    assert isinstance(input_matrix, np.ndarray), 'input_matrix has to be np.ndarray.'
    assert isinstance(kernel, np.ndarray), 'kernel has to be np.ndarray.'
    assert isinstance(stride, int), 'stride has to be positive integer.'
    assert stride > 0, 'stride has to be positive integer.'

    #get the shapes
    i_nrow, i_ncol = input_matrix.shape
    k_nrow, k_ncol = kernel.shape
    
    # output array dimensions
    out_nrow = (i_nrow - k_nrow) // stride + 1
    out_ncol = (i_ncol - k_ncol) // stride + 1
    #create output
    output = np.zeros((out_nrow, out_ncol))
    
    for i in range(0, i_nrow - k_nrow + 1, stride):
        for j in range(0, i_ncol - k_ncol + 1, stride):
            
            #select the region, multiply martices elementwise and sum
            output_value = np.sum(input_matrix[i:i+k_nrow, j:j+k_ncol] * kernel)
            #store the result in the output
            output[i//stride, j//stride] = output_value
    
    return output
