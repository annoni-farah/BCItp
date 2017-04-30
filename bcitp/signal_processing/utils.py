#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BCItp
#
# Copyright (C) 2014-2017 BCItp Project
# Author: Rafael Duarte <rmendesduarte@gmail.com>
# URL: <http://bcitp.readthedocs.io/>
# For license information, see LICENSE.TXT


import numpy as np  # numpy - used for array and matrices operations


def nanCleaner(d):
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
    >>> EEGdata_clean = nanCleaner(EEGdata_withNaN)
    """

    for i in range(d.shape[0]):

        bad_idx = np.isnan(d[i, :])
        d[i, bad_idx] = np.interp(bad_idx.nonzero()[0],
                                  (~bad_idx).nonzero()[0], d[i, ~bad_idx])

    return d
