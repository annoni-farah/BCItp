#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BCItp
#
# Copyright (C) 2014-2017 BCItp Project
# Author: Rafael Duarte <rmendesduarte@gmail.com>
# URL: <http://bcitp.readthedocs.io/>
# For license information, see LICENSE.TXT

import numpy as np


def load_as_matrix(path):
    '''
        Loads text file content as numpy matrix

        :param path: path to text file

        :param cols: order of columns to be read

        Returns
        -------
        matrix : numpy matrix, shape as written in txt

        Examples
        --------
        >>> data_path = "/PATH/TO/FILE/somematrix.txt"
        >>> matrix_data = loadAsMatrix(data_path)
    '''

    matrix = np.load(open(path, "rb"))

    return matrix


def save_matrix_as_NPY(data_in, path, mode='a'):
    '''
        Saves a numpy format matrix into a .npy file

        :param data_in: numpy matrix
        :param path: path to save file
        :param mode: open method a-append, w-write(optional)

    '''

    with open(path, mode) as data_file:
        np.save(data_file, data_in)
