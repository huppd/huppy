from style import *
import extractor as ex


def addNOX2plot( filename='./output', pattern=ex.NOXResPattern, ind=0, it0=0, label='', ls='-',ms='' ):
	bla = ex.extract( filename, pattern )
	dof = ex.extract( filename, ex.PimpDofPattern )
	print 'dof: ',dof
	semilogy(arange(len(bla))+it0,bla[:,ind]/sqrt(dof),lw=2,label=label,ls=ls,ms=ms )

def addBelos2plot( filename='./output', pattern=ex.NOXResPattern, it0=0, label='', ls='-', ms='' ):
	bla = ex.extract( filename, pattern )
	print( 'bla: '+str(bla) )
	semilogy(arange(len(bla))+it0,bla[:],lw=2,label=label,ls=ls,ms=ms )

def addInnerBelos2plot( filename='./output', ifilename='./output', pattern=ex.NOXResPattern, it0=0, label='', ls='-',ms='', times=2 ):
	bla = ex.extract( filename, pattern )
	ibla = ex.extract( ifilename, pattern )
	index = [0]
	for i in range( len(bla) ):
		index.append( int(index[i]+times*bla[i]) )
	print 'len(ibla):', len(ibla)
	print 'index:', index
	y = []
	for i in range(len(index)-1):
		y.append( mean( ibla[ index[i]:index[i+1] ] ) )
	print 'y:',y 
	semilogy(arange(len(y))+it0,y[:],lw=2,label=label,ls=ls,ms=ms )
	return bla, ibla

def accumBelos2plot( filenames=['./output'], pattern=ex.NOXResPattern, x=0, label='', ls='-',ms='' ):
	bla = array([])
	for filename in filenames:
		bla = append( bla, ex.extract( filename, pattern )[-1] )
	loglog(x,bla[:],lw=2,label=label,ls=ls,basex=10 )


