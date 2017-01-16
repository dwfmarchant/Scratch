
import pandas as pd
import numpy as np

def readMag(obs_fname, pred_fname=None):

    opts = {'skiprows':3,
            'delim_whitespace':True,
            'names':['x', 'y', 'z', 'mag', 'uncert']}

    dat = pd.read_csv(obs_fname, **opts)

    if pred_fname is not None:
        dat['pred'] = np.loadtxt(pred_fname, skiprows=3)[:, -1]

    return dat
