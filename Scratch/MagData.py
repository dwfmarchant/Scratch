
import pandas as pd
import numpy as np

class MagData(object):
    """Magnetic data set"""
    def __init__(self, fname=None):
        super(MagData, self).__init__()
        self.df = pd.DataFrame(columns=['x', 'y', 'z', 'mag', 'uncert'])
        self.inc = None
        self.dec = None
        self.b0 = None

        if fname is not None:
            self.readDobs(fname)

    def readDobs(self, fname):
        with open(fname, 'r') as f:
            line = f.readline()
        self.inc, self.dec, self.b0 = [float(x) for x in line.strip().split()]        

        dat = np.loadtxt(fname, skiprows=3)
        self.df['x'] = dat[:, 0]
        self.df['y'] = dat[:, 1]
        self.df['z'] = dat[:, 2]
        self.df['mag'] = dat[:, 3]
        self.df['uncert'] = dat[:, 4]

    def getLimits(self, extend=0):
        out = {'xmin':self.x.min()-extend,
               'xmax':self.x.max()+extend,
               'ymin':self.y.min()-extend,
               'ymax':self.y.max()+extend}
        return out

    def writeObs(self, fname='mag.obs'):
        with open(fname, 'w') as f:
            line = '{inc:.2f} {dec:.2f} {b0:.2f}\n{inc:.2f} {dec:.2f} 1\n'.format(**self.fieldDict)
            f.write(line)
            line = '{}\n'.format(self.ndat)
            f.write(line)
            for r in self.df[['x', 'y', 'z', 'mag', 'uncert']].values:
                f.write('{:.2f} {:.2f} {:.2f} {:.2f} {:.2f}\n'.format(*r))
    
    @property
    def x(self):
        return self.df.x

    @property
    def y(self):
        return self.df.y
    
    @property
    def z(self):
        return self.df.z

    @property
    def mag(self):
        return self.df.mag

    @property
    def uncert(self):
        return self.df.uncert

    @property
    def ndat(self):
        return self.df.shape[0]

    @property
    def fieldDict(self):
        return {'inc':self.inc, 'dec':self.dec, 'b0':self.b0}
    