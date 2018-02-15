""" streamfunction implemented from matlab """
import pylab as pl


def streamfunction(x, y, u, v):
    """ computes the streamfunction associated with the flowfield (u,v) on the
    cartesian coordinate system (x,y)
     INPUT:
     x        vector of length nx with x-coordinates
     y        vector of length ny with y-coordinates
     u        matrix of size (ny,nx) with velocities in x-direction
     y        matrix of size (ny,nx) with velocities in y-direction
     OUTPUT:
     psi      matrix of size (ny,nx) with streamfunction
    """
    NX = len(x)
    NY = len(y)
    #
    psi = pl.zeros(u.shape)
    psix = pl.zeros(NX)
    #
    # inegral of v(x,0) with respect to x
    for j in range(1, NX):
        dx = x[j] - x[j-1]
        psix[j] = psix[j-1] + dx/2 * (v[0, j-1] + v[0, j])
    # inegral of u(x,y) with respect to y
    for j in range(NX):
        for i in range(1, NY):
            dy = y[i] - y[i-1]
            psi[i, j] = psi[i-1, j] - dy/2 * (u[i-1, j] + u[i, j])
    # sum of the two integrals
    for j in range(1, NX):
        psi[:, j] = psi[:, j] + psix[j]
    return psi


def plot_streamfunction(x, y, u, v):
    psi = streamfunction(x, y, u, v)
    # pcolor(x,y,sqrt(u**2+v**2),cmap='YlOrRd')
    # pcolor(x,y,sqrt(u**2+v**2),cmap='YlOrBr')
    # pcolor(x,y,sqrt(u**2+v**2),cmap='hot_r')
    # pcolormesh(x,y,sqrt(u**2+v**2), shading='flat',cmap='hot_r')
    # pcolormesh(x,y,sqrt(u**2+v**2), shading='gouraud',cmap='hot_r',
    # vmin=0,vmax=1.)
    pl.pcolormesh(x, y, pl.sqrt(u**2+v**2), shading='gouraud', cmap='hot_r',
                  rasterized=True)
    # shading interp
    # pcolor(x,y,sqrt(u**2+v**2),cmap='Blues')
    # pcolor(x,y,sqrt(u**2+v**2),cmap='autumn')
    pl.colorbar()
    pl.contour(x, y, psi, 20, colors='black', linestyles='solid',
               linewidths=1.25, rasterized=True)
    # circ = Circle([1.,1.],radius=0.12,color='0.5',fill=True)
    # gca().add_artist(circ)
    pl.xlabel(r'$x$')
    pl.ylabel(r'$y$')


if __name__ == '__main__':
    #
    y = pl.linspace(0, 10, 200)
    x = pl.linspace(-10, 10, 200)
    #
    [X, Y] = pl.meshgrid(x, y)
    #
    U = X
    V = -Y
    #
    PSI = streamfunction(x, y, U, V)
    #
    pl.contourf(x, y, -pl.sqrt(U**2+V**2), 20)
    pl.contour(x, y, PSI, 20, colors='black', linestyles='solid', lw=2)
    pl.show()
