
from math import sqrt
import numpy as np
import scipy.interpolate as interp
from numba import jit

def makeGrid(x, y, z, nc=128,method='linear'):

    dx = x.max() - x.min()
    dy = y.max() - y.min()

    gcs = np.max([dx, dy])/(nc-1)

    xv = np.r_[x.min():x.max()+gcs:gcs]
    yv = np.r_[y.min():y.max()+gcs:gcs]

    X, Y = np.meshgrid(xv, yv)

    grdX = (x-x.min())/dx
    grdX = np.round(grdX*(xv.size-1)) 
    grdX = dx*grdX/xv.size + x.min()

    grdY = (y-y.min())/dy
    grdY = np.round(grdY*(yv.size-1))
    grdY = dy*grdY/yv.size + y.min()

    grdXY = np.c_[grdX, grdY]

    b = np.ascontiguousarray(grdXY).view(np.dtype((np.void, grdXY.dtype.itemsize * grdXY.shape[1])))
    _, fwd, inv = np.unique(b, return_index=True, return_inverse=True)
    grdLoc = grdXY[fwd, :]

    avVals = np.bincount(inv, weights=z)/np.bincount(inv)
    Z = interp.griddata(grdLoc, avVals, (X, Y), method=method)
    
    return xv, yv, Z

@jit(nopython=True)
def maskGrid_core(x, y, xv, yv, r, mask):
    for i in range(x.shape[0]):
        for ixv in range(xv.shape[0]):
            for iyv in range(yv.shape[0]):
                dx = x[i] - xv[ixv]
                dy = y[i] - yv[iyv]
                ri = sqrt(dx**2 + dy**2)
                if ri < r:
                    mask[iyv, ixv] = 1

def maskGrid(x, y, xv, yv, r=500):
    mask = np.zeros((yv.shape[0], xv.shape[0]))
    maskGrid_core(x, y, xv, yv, r, mask)
    return mask == 1
