import numpy as np

def calcK(Ax, Ay, Bx, By, Mx, My, Nx, Ny):
    dx_am = Ax-Mx
    dx_an = Ax-Nx
    dx_bm = Bx-Mx
    dx_bn = Bx-Nx

    dy_am = Ay-My
    dy_an = Ay-Ny
    dy_bm = By-My
    dy_bn = By-Ny

    ram = np.sqrt(dx_am**2 + dy_am**2)
    ran = np.sqrt(dx_an**2 + dy_an**2)
    rbm = np.sqrt(dx_bm**2 + dy_bm**2)
    rbn = np.sqrt(dx_bn**2 + dy_bn**2)

    K = 1/ram - 1/rbm - 1/ran + 1/rbn
    return K

def appRes(Ax, Ay, Bx, By, Mx, My, Nx, Ny, Vp, In=1.):
    
    K = calcK(Ax, Ay, Bx, By, Mx, My, Nx, Ny)
    rho = (2*np.pi*Vp)/(K*In)
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

