
class LineBuilder:
    
    """
    Example:
        fig = plt.figure(1)
        ax = fig.add_subplot(111, aspect='equal')
        line, = ax.plot([], [], '-ko')  # empty line
        linebuilder = LineBuilder(line)
        plt.show()
    """

    def __init__(self, line):
        self.line = line
        self.x_pts = list(line.get_xdata())
        self.y_pts = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
        self.kid = line.figure.canvas.mpl_connect('key_press_event', self)

    def __call__(self, event):
        if event.name == 'button_press_event':
            if event.inaxes != self.line.axes: 
                return
            self.x_pts.append(event.xdata)
            self.y_pts.append(event.ydata)
            self.line.set_data(self.x_pts, self.y_pts)
            self.line.figure.canvas.draw()
        elif event.name == 'key_press_event':
            if event.key == 'd':
                self.x_pts = self.x_pts[:-1]
                self.y_pts = self.y_pts[:-1]
                self.line.set_data(self.x_pts, self.y_pts)
                self.line.figure.canvas.draw()
            else:
                pass
        else:
            pass

    def to_file(self, fname='pts.txt'):

        with open(fname, 'w') as f:
            for pt in zip(self.x_pts, self.y_pts):
                f.write('{:.2f} {:.2f}\n'.format(*pt))
