
from GeoMesh import TensorMesh2D
import numpy as np

def removePadding2D(mesh, modelIn=0, nEast=0, nWest=0, nTop=0, nBottem=0):
    
    hx = mesh.hx.copy()
    hz = mesh.hz.copy()
    x0 = mesh.x0
    z0 = mesh.z0
    if nWest > 0:
        x0 += hx[:nWest].sum()
        hx = hx[nWest:]
    if nEast > 0:
        hx = hx[:-nEast]
    if nBottem > 0:
        z0 += hz[:nBottem].sum()
        hz = hz[nBottem:]
    if nTop > 0:
        hz = hz[:-nTop]
    meshOut = TensorMesh2D([hx, hz], [x0, z0])

    if modelIn is not None:
        isVec = min(np.atleast_2d(modelIn).shape) == 1
        modelOut = modelIn.copy()
        if isVec: 
            modelOut = mesh.r(modelOut, format='M')    
        if nWest > 0:
            modelOut = modelOut[nWest:, :]
        if nEast > 0:
            modelOut = modelOut[:-nEast, :]
        if nBottem > 0:
            modelOut = modelOut[:, nBottem:]
        if nTop > 0:
            modelOut = modelOut[:, :-nTop]
        if isVec:
            modelOut = meshOut.r(modelOut, format='V')
        return meshOut, modelOut
    else:
        return meshOut

    
