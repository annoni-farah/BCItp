import numpy as np

import json


def load_as_matrix(path):
    """Loads text file content as numpy matrix
    Parameters
    ----------
    path : path to text file

    cols : order of columns to be read

    Returns
    -------
    matrix : numpy matrix, shape as written in txt

    Examples
    --------
    >>> data_path = "/PATH/TO/FILE/somematrix.txt"
    >>> matrix_data = loadAsMatrix(data_path)
    """

    matrix = np.load(open(path, "rb"))

    # return np.fliplr(matrix.T).T
    return matrix


def clean_nan(data_in):
    """Removes NaN from data by interpolation
    Parameters
    ----------
    data_in : input data - np matrix channels x samples

    Returns
    -------
    data_out : clean dataset with no NaN samples

    Examples
    --------
    >>> data_path = "/PATH/TO/DATASET/dataset.gdf"
    >>> EEGdata_withNaN = loadBiosig(data_path)
    >>> EEGdata_clean = clean_nan(EEGdata_withNaN)
    """
    for i in range(data_in.shape[0]):

        bad_idx = np.isnan(data_in[i, ...])
        data_in[i, bad_idx] = np.interp(bad_idx.nonzero()[0],
                                        (~bad_idx).nonzero()[0],
                                        data_in[i, ~bad_idx])

    return data_in


def save_matrix_as_NPY(data_in, path, mode='a'):

    with open(path, mode) as data_file:
        np.save(data_file, data_in)


def save_obj_as_json(obj, filename):
    with open(filename, "w") as file:
        file.write(json.dumps(obj.__dict__, file, indent=4))
