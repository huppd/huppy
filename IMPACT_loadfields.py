import sys
import h5py
#import mayavi.mlab as mlab
import pylab as pl
from pylab import sin,cos,sinh,cosh
from matplotlib.colors import LogNorm
from numpy import zeros
from streamplot import streamplot 
from streamfunction import plot_streamfunction
import velocity_profiles as vp



def lod_sfield( di='.', i=0, fType = 'S'):
    if( 'S'==fType ):
        key = 'pre'
    else:
        key = 'vel'+fType
    f = h5py.File(di+'/'+key+'_'+str(i).zfill(5)+'.h5')
    s = f.get(key).value
    print( key+': ',s.shape )
    #
    x = f.get('VectorX').value
    y = f.get('VectorY').value
    return x,y,s



def lod_vfield( di='.', i=0):
    u = {'X':0,'Y':0,'Z':0}
    for field in ['X','Y']:
        x,y,f = lod_sfield( di=di, i=i, fType=field)
	u[field] = f
    #
    u['Z'] = zeros(u['X'].shape)
    #x = f.get('VectorX').value
    #y = f.get('VectorY').value
    return x,y,u




def plot_vfield(x,y,u,I=1):
	pl.figure()
	pl.gca().set_aspect('equal')
	M = pl.sqrt( u['X'][::I,::I]**2+u['Y'][::I,::I]**2 )
	pl.quiver(x[::I],y[::I],u['X'][::I,::I],u['Y'][::I,::I],M)
	pl.xlabel('x')
	pl.ylabel('y')
	pl.colorbar()
	pl.show()

def lodnplot_sfield( di='.', i=0, I=1, fType='S' ):
	x,y,u = lod_sfield( di, i, fType )
	plot_sfield(x,y,u,I)
        return x,y,u

def lodnplot_vfield( di='.', i=0, I=1):
	x,y,u = lod_vfield( di, i )
	plot_vfield(x,y,u,I)
	return x,y,u

	
def lodnplot_stream( di='.', i=0 ):
	x,y,u = lod_vfield( di, i )
	plot_stream(x,y,u)
	return x,y,u

	
def lodnplot_streamfunc( di='.', i=0 ):
	x,y,u = lod_vfield( di, i )
	plot_streamfunction(x,y,u['X'],u['Y'])
	return x,y,u

	
	
def lodnplots_streamfunc( di='.', i=0, nf=1 ):
  for m in range(2*nf+1):
    pl.figure()
    lodnplot_streamfunc( di, i=i+m )
    #pl.xlim( (0.75, 4.75))
    if m==0:
      pl.title( r'$\mathcal{R}(\hat{\mathbf{u}}_0)$')
      #pl.savefig('uc0.pdf',bbox_inches='tight')
      pl.savefig('uc0.pdf')
    elif m%2==1:
      pl.title( r'$\mathcal{R}(\hat{\mathbf{u}}_'+str((m+1)/2)+')$')
      pl.savefig('uc'+str((m+1)/2)+'.pdf',bbox_inches='tight')
    else:
      pl.title( r'$\mathcal{I}(\hat{\mathbf{u}}_'+str((m+1)/2)+')$')
      pl.savefig('us'+str((m+1)/2)+'.pdf',bbox_inches='tight')
  

def lodnplot_mstreamfunc( di='.', i=0, I=1, nf=1, t=0 ):
	x,y,u = lod_mvfield( di=di, i=i, nf=nf, t=t )
	plot_streamfunction(x,y,u['X'],u['Y'])
	#pl.figure()
	#pl.plot( x, u['X'][0,:],'.',label=r'$t='+str(t/pl.pi)+'\pi$' )
	#pl.title(r'$t='+str(t/pl.pi)+'\pi$')
	pl.xlabel(r'$x$')
	pl.ylabel(r'$y$')
	#pl.legend(loc=0)
	pl.title(r'$\mathbf{u}(t='+str(t/pl.pi)+'\pi)$')
	#pl.xlim( (0.75, 4.75))
	#pl.gca().set_aspect('equal')
	return x,y,u
	
def lod_mvfield( di='.', i=0, nf=1, t=0 ):
	x,y,u = lod_vfield( di, i )
	print('0 mode:  \tnorm:\t'+str( pl.norm(pl.norm(u['X'])+pl.norm(u['Y'])+pl.norm(u['Z'])) ) )
	for m in range(nf):
		x,y,uc = lod_vfield( di, 2*m+1+i )
		x,y,us = lod_vfield( di, 2*m+2+i )
		norc = 0 
		nors = 0
		for f in ['X','Y','Z']:
			norc += pl.norm(uc[f])
			nors += pl.norm(us[f])
			u[f] += uc[f]*cos((m+1)*t)+us[f]*sin((m+1)*t)
		print('c mode:  '+str(m+1)+'\tnorm:\t'+str(norc) )
		print('s mode:  '+str(m+1)+'\tnorm:\t'+str(nors) )
	return x,y,u


def plot_energyspec( di='.', i=0, nf=1 ):
	e = pl.empty( nf+1 )
	x,y,u = lod_vfield( di, i )
	e[0] =  pl.sqrt( pl.norm(u['X'])**2 + pl.norm(u['Y'])**2 + pl.norm(u['Z'])**2 )
	for m in range(nf):
		x,y,uc = lod_vfield( di, 2*m+1+i )
		x,y,us = lod_vfield( di, 2*m+2+i )
		norc = 0 
		nors = 0
		for f in ['X','Y','Z']:
			norc += pl.norm(uc[f])**2
			nors += pl.norm(us[f])**2
		e[m+1] = pl.sqrt( norc+nors )
	pl.semilogy(e)
	pl.grid(True)
	pl.xlabel(r'mode: $k$')
	pl.ylabel(r'$e=\sqrt{ \mathbf{\hat{u}}_k^c\cdot\mathbf{\hat{u}}_k^c+\mathbf{\hat{u}}^s_k\cdot\mathbf{\hat{u}}_k^s }$',ha='left',va='bottom',rotation=0)
	pl.gca().yaxis.set_label_coords(-0.075, 1.02)
	
#print('c mode:  '+str(m+1)+'\tnorm:\t'+str(norc) )
#print('s mode:  '+str(m+1)+'\tnorm:\t'+str(nors) )
#return x,y,u

def lodnplot_mumodeprof( di='.', i=0, I=1, nf=1, t=0 ):
	#pl.figure()
	x,y,u = lod_mvfield( di=di, i=i, nf=nf, t=t )
	pl.plot( x, u['X'][0,:],',-',label=r'$t='+str(t/pl.pi)+'\pi$' )
	#pl.title(r'$t='+str(t/pl.pi)+'\pi$')
	pl.xlabel(r'$x$')
	pl.ylabel(r'$u$')
	pl.title(r'$\mathbf{u}(\mathbf{x},t='+str(t)+')$')
	pl.legend(loc=0)
	return x,y,u


def lodnplot_mvfield( di='.', i=0, I=1, nf=1, t=0 ):
	x,y,u = lod_mvfield( di=di, i=i, nf=nf, t=t )
	plot_vfield(x,y,u,I)
	#pl.figure()
	#pl.plot( x, u['X'][0,:],'.',label=r'$t='+str(t/pl.pi)+'\pi$' )
	#pl.title(r'$t='+str(t/pl.pi)+'\pi$')
	pl.xlabel(r'$x$')
	pl.ylabel(r'$y$')
	#pl.legend(loc=0)
	pl.title(r'$\mathbf{u}(t='+str(t)+')$')
	return x,y,u
	
def lodnplot_mumodebug( di='.', i=0, I=1, nf=8, Nt=16 ):
	x,y,u = lod_vfield( di, i )
	ts = pl.linspace(0,2*pi,Nt+1)
	up = pl.zeros([len(x),len(ts)])
	for i in range(len(ts)):
	  up[:,i] = u['X'][0,:].T
	print('0 mode:  \tnorm:\t'+str( pl.norm(pl.norm(u['X'])+pl.norm(u['Y'])+pl.norm(u['Z'])) ) )
	for m in range(nf):
	  x,y,uc = lod_vfield( di, 2*m+1+i )
	  x,y,us = lod_vfield( di, 2*m+2+i )
	  norc = 0 
	  nors = 0
	  norc += pl.norm(uc['X'])
	  nors += pl.norm(us['X'])
	  for i in range(len(t)):
	      up[:,i] += uc['X'][:,0]*cos(m*t)+us['X'][:,0]*sin(m*t)
	  print('c mode:  '+str(m)+'\tnorm:\t'+str(norc) )
	  print('s mode:  '+str(m)+'\tnorm:\t'+str(nors) )
	#plot_vfield(x,y,u,I)
	pl.figure()
	pl.plot( x, u['X'][0,:],'.-',label=r'$t='+str(t/pl.pi)+'\pi$' )
	#pl.title(r'$t='+str(t/pl.pi)+'\pi$')
	pl.xlabel(r'$x$')
	pl.ylabel(r'$u$')
	pl.legend(loc=0)
	return x,y,u


def plot_stream(x,y,u):
	pl.figure()
	pl.gca().set_aspect('equal')
	M = pl.sqrt( u['X'][:,:]**2+u['Y'][:,:]**2 )
	lw = 5*M/M.max()
	streamplot(x,y,u['X'],u['Y'],color=M,linewidth=lw)
	pl.xlabel('x')
	pl.ylabel('y')
	#pl.colorbar()
	pl.show()

def plot_sfield(x,y,p,I=1):
	pl.figure()
	pl.gca().set_aspect('equal')
	pl.pcolor(x[::I],y[::I],p[::I,::I])
	pl.contour(x,y,p,20,colors='k')
	pl.xlabel('x')
	pl.ylabel('y')
	pl.colorbar()
	pl.show()

def lod_vdif(di1='.',di2='.',i1=0,i2=0):
	e = {'X':0,'Y':0,'Z':0}
	x,y,u1 = lod_vfield(di1,i1)
	x,y,u2 = lod_vfield(di2,i2)
	e['X'] = u1['X']-u2['X']
	e['Y'] = u1['Y']-u2['Y']
	e['Z'] = pl.sqrt(e['X']**2 + e['Y']**2)
	return x,y,e

def plot_vdif(x,y,e):
	#e['Z'] = pl.sqrt(e['X']**2 + e['Y']**2)
	#plot_vfield(x,y,e)
	pl.figure()
	pl.gca().set_aspect('equal')
	#pl.pcolor(y,x,e['Z'].T, norm=LogNorm(vmin=e['Z'].min(), vmax=e['Z'].max()) )
	pl.pcolor(x,y,e['Z'])
	pl.colorbar()
	pl.xlabel(r'$x$')
	pl.ylabel(r'$y$')
	print( '||e||_2 =', pl.norm(e['Z']) )
	pl.show()

def lodnplot_vdif(di1='.',di2='.',i1=0,i2=0):
	x,y,e = lod_vdif(di1,di2,i1,i2)
	plot_vdif( x,y,e )

def verify_para(x,y,u,fd='X'):
	nx = len(x)
	ny = len(y)
	nx1 = int(nx/4)
	ny1 = int(ny/4)
	nx2 = int(nx/2)
	ny2 = int(ny/2)
	nx3 = int(3*nx/4)
	ny3 = int(3*ny/4)
	
	yf = pl.linspace(0,y[-1],len(y)*100)
	xf = pl.linspace(0,x[-1],len(x)*100)
	pl.subplot(221)
	pl.plot(x,u[fd][nx2,:],'.')
	if fd=='X':
		pl.plot(xf, vp.parabola(y)[nx2]*pl.ones(len(xf)) )
	else:
		pl.plot(xf, vp.parabola(yf) )
	pl.xlabel(r'$x$')
	if fd =='X':
		pl.ylabel(r'$u(x)$')
	else:
		pl.ylabel(r'$v(x)$')
	#
	pl.subplot(222)
	pl.plot(y,u[fd][:,ny2],'.')
	if fd=='X':
		pl.plot(yf, vp.parabola(yf) )
	else:
		pl.plot(yf, vp.parabola(y)[nx2]*pl.ones(len(yf)) )
	pl.xlabel(r'$y$')
	if fd =='X':
		pl.ylabel(r'$u(y)$')
	else:
		pl.ylabel(r'$v(y)$')
	#
	pl.subplot(223)
	if fd=='X':
		pl.plot(y, abs(u[fd][nx2,:]-vp.parabola(y)[nx2])/abs(vp.parabola(y)[nx2]) )
	else:
		pl.plot(y, abs(u[fd][nx2,:]-vp.parabola(y))/abs(vp.parabola(y)) )
	pl.xlabel(r'$x$')
	if fd =='X':
		pl.ylabel(r'$\frac{|u(x)-u^\star(x)|}{|u^\star(x)|}$')
	else:
		pl.ylabel(r'$\frac{|v(x)-v^\star(x)|}{|v^\star(x)|}$')
	#
	pl.subplot(224)
	if fd=='X':
		pl.plot(y, abs(u[fd][:,ny2]-vp.parabola(y))/abs(vp.parabola(y)) )
	else:
		pl.plot(y, abs(u[fd][:,ny2]-vp.parabola(y)[ny2])/abs(vp.parabola(y)[ny2]) )
	pl.xlabel(r'$y$')
	if fd =='X':
		pl.ylabel(r'$\frac{|u(y)-u^\star(y)|}{|u^\star(y)|}$')
	else:
		pl.ylabel(r'$\frac{|v(y)-v^\star(y)|}{|v^\star(y)|}$')
	#subplot(224)
	#if(fd=='X'):
		#plot( y, norm(u[fd][nx/2,y]-vp.parabola(y))/abs( vp.parabola(y) ) )
	#elif:
		#plot( y, norm(u[fd][nx/2,y]-vp.parabola(x)) )


def verify_pulse(x,y,u,fd='X',mode='c',re=1.,om=1.,px=1.):
	nx = len(x)
	ny = len(y)
	nx1 = int(nx/4)
	ny1 = int(ny/4)
	nx2 = int(nx/2)
	ny2 = int(ny/2)
	nx3 = int(3*nx/4)
	ny3 = int(3*ny/4)
	
	yf = pl.linspace(0,y[-1],len(y)*100)
	xf = pl.linspace(0,x[-1],len(x)*100)
	pl.subplot(221)
	pl.plot(x,u[fd][nx2,:],'.')
	if fd=='X':
		if mode=='c':
			pl.plot(xf, vp.pulseC(y,re,om,px)[nx2]*pl.ones(len(xf)) )
		else:
			pl.plot(xf, vp.pulseS(y,re,om,px)[nx2]*pl.ones(len(xf)) )
	else:
		if mode=='c':
			pl.plot(xf, vp.pulseC(yf,re,om,px) )
		else:
			pl.plot(xf, vp.pulseS(yf,re,om,px) )
	pl.xlabel(r'$x$')
	if fd =='X':
		pl.ylabel(r'$u^{'+mode+'}(x)$')
	else:
		pl.ylabel(r'$v^{'+mode+'}(x)$')
	
	pl.subplot(222)
	pl.plot(y,u[fd][:,ny2],'.')
	if fd=='X':
		if mode=='c':
			pl.plot(yf, vp.pulseC(yf,re,om,px) )
		else:
			pl.plot(yf, vp.pulseS(yf,re,om,px) )
	else:
		if mode=='c':
			pl.plot(yf, vp.pulseC(y,re,om,px)[nx2]*pl.ones(len(yf)) )
		else:
			pl.plot(yf, vp.pulseS(y,re,om,px)[nx2]*pl.ones(len(yf)) )
	pl.xlabel(r'$y$')
	if fd =='X':
		pl.ylabel(r'$u^{'+mode+'}(y)$')
	else:
		pl.ylabel(r'$v^{'+mode+'}(y)$')
	
	pl.subplot(223)
	if fd=='X':
		if mode=='c':
			pl.plot(y[1:-1], abs(u[fd][nx2,1:-1]-vp.pulseC(y,re,om,px)[nx2])/abs(vp.pulseC(y,re,om,px)[nx2]) )
		else:
			pl.plot(y[1:-1], abs(u[fd][nx2,1:-1]-vp.pulseS(y,re,om,px)[nx2])/abs(vp.pulseS(y,re,om,px)[nx2]) )
	else:
		if mode=='c' :
			pl.plot(y[1:-1], abs(u[fd][nx2,1:-1]-vp.pulseC(y,re,om,px)[1:-1])/abs(vp.pulseC(y,re,om,px)[1:-1]) )
		else:
			pl.plot(y[1:-1], abs(u[fd][nx2,1:-1]-vp.pulseS(y,re,om,px)[1:-1])/abs(vp.pulseS(y,re,om,px)[1:-1]) )
	pl.xlabel(r'$x$')
	if fd =='X':
		pl.ylabel(r'$\frac{|u^{'+mode+'}(x)-u^\star(x)|}{|u^\star(x)|}$')
	else:
		pl.ylabel(r'$\frac{|v^{'+mode+'}(x)-v^\star(x)|}{|v^\star(x)|}$')
	
	pl.subplot(224)
	if fd=='X':
		if mode=='c' :
			pl.plot(y[1:-1], abs(u[fd][1:-1,ny2]-vp.pulseC(y,re,om,px)[1:-1])/abs(vp.pulseC(y,re,om,px)[1:-1]) )
		else:
			pl.plot(y[1:-1], abs(u[fd][1:-1,ny2]-vp.pulseS(y,re,om,px)[1:-1])/abs(vp.pulseS(y,re,om,px)[1:-1]) )
	else:
		if mode=='c' :
			pl.plot(y[1:-1], abs(u[fd][1:-1,ny2]-vp.pulseC(y,re,om,px)[ny2])/abs(vp.pulseC(y,re,om,px)[ny2]) )
		else:
			pl.plot(y[1:-1], abs(u[fd][1:-1,ny2]-vp.pulseS(y,re,om,px)[ny2])/abs(vp.pulseS(y,re,om,px)[ny2]) )

	pl.xlabel(r'$y$')
	if fd =='X':
		pl.ylabel(r'$\frac{|u^{'+mode+'}(y)-u^\star(y)|}{|u^\star(y)|}$')
	else:
		pl.ylabel(r'$\frac{|v^{'+mode+'}(y)-v^\star(y)|}{|v^\star(y)|}$')
	#subplot(224)
	#if(fd=='X'):
		#plot( y, norm(u[fd][nx/2,y]-vp.parabola(y))/abs( vp.parabola(y) ) )
	#elif:
		#plot( y, norm(u[fd][nx/2,y]-vp.parabola(x)) )


if __name__ == "__main__":
	i = '00001'
	if( len(sys.argv) > 1 ):
		i = sys.argv[1]
	print( i )
	
	di = '.'
	if( len(sys.argv) > 2 ):
		di = sys.argv[2]
	print( di )
	
	x,y,u = lod_vfield(di,i)
	plot_vfield(x,y,u)

