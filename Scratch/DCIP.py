import numpy as np

def appRes(ax, ay, bx, by, mx, my, nx, ny, V, I):
    dx_am = ax-mx
    dx_an = ax-nx
    dx_bm = bx-mx
    dx_bn = bx-nx

    dy_am = ay-my
    dy_an = ay-ny
    dy_bm = by-my
    dy_bn = by-ny

    ram = np.sqrt(dx_am**2 + dy_am**2)
    ran = np.sqrt(dx_an**2 + dy_an**2)
    rbm = np.sqrt(dx_bm**2 + dy_bm**2)
    rbn = np.sqrt(dx_bn**2 + dy_bn**2)

    k = 1/ram - 1/rbm - 1/ran + 1/rbn

    rho = (2*np.pi*V)/(k*I)
    return rho

def writeDCIP(fname, data):
    formatters = 4*[lambda x: '{:.2f}'.format(x)] + 2*[lambda x: '{:.4e}'.format(x)]

    grp = data.groupby(['Ax', 'Ay', 'Bx', 'By'])
    with open(fname, 'w') as f:
        for k in grp.groups.keys():
            txDat = grp.get_group(k)
            out = [*txDat.iloc[0][['Ax', 'Ay', 'Bx', 'By']].values, txDat.shape[0]]
            txLine = '{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:d}\n'.format(*out)
            f.write(txLine)
            txDat.to_string(f, columns=['Mx', 'My', 'Nx', 'Ny', 'Vp', 'VpUncert'], 
                            formatters=formatters,
                            header=False, index=False)
            f.write('\n')

