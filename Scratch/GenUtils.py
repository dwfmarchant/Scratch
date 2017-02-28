import numpy as np

def rotatePoints(x, y, theta, x0=0., y0=0.):

    # Convert theta to radians
    theta = theta*2.*np.pi/360.

    # Build rotation matrix
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])

    xy = np.c_[x - x0, y - y0]
    xyR = R.dot(xy.T).T

    xR = xyR[:, 0] + x0
    yR = xyR[:, 1] + y0

    return xR, yR
