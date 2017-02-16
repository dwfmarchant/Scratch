
import numpy as np
import pandas as pd

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

    formatters = 4*['{:.2f}'.format] + 2*['{:.4e}'.format]

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

def readDCIP(fname, hasZ=True, hasUncert=True):

    if hasZ:
        columns = ['Ax', 'Ay', 'Az',
                   'Bx', 'By', 'Bz',
                   'Mx', 'My', 'Mz',
                   'Nx', 'Ny', 'Nz',
                   'Vp']
        colInds = {'Ax':0, 'Ay':1, 'Az':2,
                   'Bx':3, 'By':4, 'Bz':5,
                   'Mx':0, 'My':1, 'Mz':2,
                   'Nx':3, 'Ny':4, 'Nz':5,
                   'Vp':6, 'Un':7}
    else:
        columns = ['Ax', 'Ay',
                   'Bx', 'By',
                   'Mx', 'My',
                   'Nx', 'Ny',
                   'Vp']
        colInds = {'Ax':0, 'Ay':1,
                   'Bx':2, 'By':3,
                   'Mx':0, 'My':1,
                   'Nx':2, 'Ny':3,
                   'Vp':4, 'Un':5}

    if hasUncert: 
        columns.append('Un')

    survey = pd.DataFrame(columns=columns)

    nLines = sum(1 for line in open(fname, 'r'))+1

    with open(fname, 'r') as f:
        for i in range(nLines):
            line = f.readline()            
            
            # Remove comments
            try:
                commentInd = line.index('!')
                line = line[:commentInd]
            except Exception: 
                pass

            if line.strip().startswith('IPTYPE'): 
                continue
            
            line = line.split()

            # Skip empty lines
            if len(line) == 0: 
                continue

            nRx = int(line[-1])    

            Ax = float(line[colInds['Ax']])*np.ones(nRx)
            Ay = float(line[colInds['Ay']])*np.ones(nRx)
            Bx = float(line[colInds['Bx']])*np.ones(nRx)
            By = float(line[colInds['By']])*np.ones(nRx)
            Mx = np.zeros(nRx)
            My = np.zeros(nRx)            
            Nx = np.zeros(nRx)
            Ny = np.zeros(nRx)
            Vp = np.zeros(nRx)
            if hasZ:
                Az = float(line[colInds['Az']])*np.ones(nRx)
                Bz = float(line[colInds['Bz']])*np.ones(nRx)
                Mz = np.zeros(nRx)
                Nz = np.zeros(nRx)
            if hasUncert: 
                Un = np.zeros(nRx)

            for k in range(nRx):
                line = f.readline().split()

                Mx[k] = float(line[colInds['Mx']])
                My[k] = float(line[colInds['My']])
                Nx[k] = float(line[colInds['Nx']])
                Ny[k] = float(line[colInds['Ny']])
                Vp[k] = float(line[colInds['Vp']])
                if hasZ:
                    Mz[k] = float(line[colInds['Mz']])
                    Nz[k] = float(line[colInds['Nz']])
                if hasUncert: 
                    Un[k] = float(line[colInds['Un']])

                d = {'Ax':Ax, 'Ay':Ay,
                     'Bx':Bx, 'By':By,
                     'Mx':Mx, 'My':My,
                     'Nx':Nx, 'Ny':Ny,
                     'Vp':Vp}
                if hasZ:
                    d['Az'] = Az
                    d['Bz'] = Bz
                    d['Mz'] = Mz
                    d['Nz'] = Nz
                if hasUncert: 
                    d['Un'] = Un

            lineDF = pd.DataFrame(d)
            survey = survey.append(lineDF, ignore_index=True)

    return survey

def readOut(fname='DC_octree_inv.out', onlyLast=True):
    cols = ["beta", "iter", "misfit", "phi_d", "phi_m", "phi", "normg", "grel"]
    out = pd.read_csv(fname, delim_whitespace=True, skiprows=1, names=cols)
    if onlyLast:
        out = out.loc[[0]].append(out.drop_duplicates('beta', keep='last'))
        out = out.reset_index(drop=True)
    return out
