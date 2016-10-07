import numpy as np
import biosig
import sys

def loadBiosig(fname):
    """Loads biosig compatible datasets.
    Parameters
    ----------
    fname : path to dataset

    Returns
    -------
    data : dataset as a numpy matrix
    sample_rate : dataset sample rate

    Examples
    --------
    >>> data_path = "/PATH/TO/PATH/dataset.gdf"
    >>> EEGdata = loadBiosig(data_path)
    """

    # Loads GDF competition data
    HDR = biosig.constructHDR(0, 0)
    HDR = biosig.sopen(fname, 'r', HDR)

    sample_rate = HDR.SampleRate
    data = biosig.sread(0, HDR.NRec, HDR)

    biosig.sclose(HDR)
    biosig.destructHDR(HDR)

    return data, sample_rate


gdf_data, fs = loadBiosig(sys.argv[1])

np.save(sys.argv[2], gdf_data)