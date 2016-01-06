from pylab import *

def streamfunction(x,y,u,v):
	#%
	#% computes the streamfunction associated with the flowfield (u,v) on 
	#% the cartesian coordinate system (x,y)
	#%
	#% INPUT:
	#% x        vector of length Nx with x-coordinates
	#% y        vector of length Ny with y-coordinates
	#% u        matrix of size (Ny,Nx) with velocities in x-direction
	#% y        matrix of size (Ny,Nx) with velocities in y-direction
	#%
	#% OUTPUT:
	#% psi      matrix of size (Ny,Nx) with streamfunction
	#%
	#
	Nx = len(x)
	Ny = len(y)
	#
	psi = zeros(u.shape)
	psix = zeros(Nx)
	#
	# %% inegral of v(x,0) with respect to x
	for j in range(1,Nx):
		dx = x[j] - x[j-1]
		psix[j] = psix[j-1] + dx/2 * (v[0,j-1] + v[0,j])
	# %%% inegral of u(x,y) with respect to y
	for j in range( Nx ):
		for i in range(1,Ny):
			dy = y[i] - y[i-1]
			psi[i,j] = psi[i-1,j] - dy/2 * (u[i-1,j] + u[i,j])
	#%% sum of the two integrals
	for j in range(1,Nx):
		psi[:,j] = psi[:,j] + psix[j]
	return psi

def plot_streamfunction( x, y, u, v):
	psi = streamfunction(x,y,u,v);
	#pcolor(x,y,sqrt(u**2+v**2),cmap='YlOrRd')
	#pcolor(x,y,sqrt(u**2+v**2),cmap='YlOrBr')
	#pcolor(x,y,sqrt(u**2+v**2),cmap='hot_r')
	#pcolormesh(x,y,sqrt(u**2+v**2), shading='flat',cmap='hot_r')
	#pcolormesh(x,y,sqrt(u**2+v**2), shading='gouraud',cmap='hot_r',vmin=0,vmax=1.)
	pcolormesh(x,y,sqrt(u**2+v**2), shading='gouraud',cmap='hot_r')
	#shading interp
	#pcolor(x,y,sqrt(u**2+v**2),cmap='Blues')
	#pcolor(x,y,sqrt(u**2+v**2),cmap='autumn')
	colorbar()
	contour(x,y,psi,20,colors='black',linestyles='solid',linewidths=1.25)
	#circ = Circle([1.,1.],radius=0.12,color='0.5',fill=True)
	#gca().add_artist(circ)
	xlabel(r'$x$')
	ylabel(r'$y$')


if __name__ == '__main__':
	#
	y = linspace(0,10,200);
	x = linspace(-10,10,200);
	# 
	[X,Y] = meshgrid(x,y);
	# 
	u = X;
	v = -Y;
	#
	psi = streamfunction(x,y,u,v);
	#
	contourf(x,y,-sqrt(u**2+v**2),20)
	contour(x,y,psi,20,colors='black',linestyles='solid',lw=2)
	show()
