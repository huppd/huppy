#from style import *
from pylab import *
from itertools import cycle
#from style import li,mi
import extractor as ex
import copy

c = ['b','g','r','c','m','y']
ci = cycle(c)
l = [ '-','--' , '-.' , ':'  ]
#l = [ '--' , '-.' , ':'  ]
li = cycle(l)
m = ['.','o','v','^','<','>','1','2','3','4','8','s','p','*','h','H','+','x','D','d','|','_','TICKLEFT','TICKRIGHT','TICKDOWN','CARETLEFT','CARETRIGHT','CARETUP','CARETDOWN']
m = ['o','v','*','x','d','^','2','>','4','p','s','p','8','h','H','+','p','D','3','|','_','TICKLEFT','TICKRIGHT','TICKDOWN','CARETLEFT','CARETRIGHT','CARETUP','CARETDOWN','.']
m = ['o','v','*','x','d','^','2','>','4','p','s','p','8','h','H','+','p','D','3','|','_','.']
mi = cycle(m)

def plotNOX( paths=['./'], leg=[],run='',newton=True ):
    i=0
    for path in paths:
            iter    = ex.extract( path+'output'+str(run), ex.NOXIterPattern )
            res     = ex.extract( path+'output'+str(run), ex.NOXResPattern )
            dof     = ex.extract( path+'output'+str(run), ex.PimpDofPattern )
            print 'dof: ',dof
            ls = li.next()
            m = mi.next()
            figure(1)
            #semilogy(iter[:],res[:,0],lw=2,label=lab,ls=ls )
            semilogy(iter,res[:,0]/sqrt(dof),ls=ls )
            if newton:
                    xlabel('Newton iteration')
            else:
                    xlabel('Picard iteration')
            ylabel(r'$||\mathbf{F}||_2/\sqrt{N}$',ha='left',va='bottom',rotation=0)
            gca().yaxis.set_label_coords(-0.09, 1.075)
            grid(True)
            #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            #xlim((0,9))
            gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            #savefig('F.pdf')
            savefig('F.pdf',bbox_inches='tight')
            figure(2)
            #semilogy(iter[:],res[:,1],basey=2,lw=1,label=lab,ls=ls,marker=m )
            semilogy(iter[1:],res[1:,1],basey=2,lw=1,ls=ls,marker=m )
            if newton:
                    xlabel('Newton iteration')
            else:
                    xlabel('Picard iteration')
            ylabel(r'step width')
            grid(True)
            #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            savefig('lam.pdf',bbox_inches='tight')
            #
            figure(3)
            #semilogy(iter[:],res[:,2],lw=1,label=lab,ls=ls ,marker=m)
            semilogy(iter[1:],res[1:,2]/sqrt(dof),lw=1,ls=ls ,marker=m)
            if newton:
                    xlabel('Newton iteration')
            else:
                    xlabel('Picard iteration')
            ylabel(r'$||\delta\mathbf{u}||_2/\sqrt{N}$')
            grid(True)
            #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            savefig('du.pdf',bbox_inches='tight')

def plotBelos( files=['./Picard.txt'], leg=[],run='' ):
    i=0
    for f in files:
            linIter = ex.extract( f, ex.BelosMaxItPattern )
            linatol = ex.extract( f, ex.BelosArTolPattern )
            figure(4)
            ls = li.next()
            m = mi.next()
            if isinstance(linIter,float) :
                    linIter=[linIter]
            plot(range(1,len(linIter)+1),linIter,marker=m,lw=0.5,ls=ls )
            xlabel('Picard iteration')
            ylabel(r'linear iterations')
            grid(True)
            # legend(leg,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            legend(leg,loc=0)
            gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            savefig('liniter.pdf',bbox_inches='tight')
            #
            figure(5)
            #semilogy(iterBelos[1:],linatol[:],marker=m,lw=0.5,label=lab,ls=ls )
            semilogy(range(1,len(linatol)+1),linatol[:],marker=m,lw=0.5,ls=ls )
            xlabel('Picard iteration')
            ylabel(r'archieved tolerance of the linear solver')
            grid(True)
            # legend(leg,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            legend(leg,loc=0)
            gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            savefig('lintol.pdf',bbox_inches='tight')
            i += 1



def plotNOX2( paths=['./'], leg=[],run='' ):
    i=0
    for path in paths:
            iter    = ex.extract( path+'output'+str(run), ex.NOXIterPattern )
            res     = ex.extract( path+'output'+str(run), ex.NOXResPattern )
            linIter = ex.extract( path+'stats_linSolve.txt', ex.BelosMaxItPattern )
            linatol = ex.extract( path+'stats_linSolve.txt', ex.BelosArTolPattern )
            dof     = ex.extract( path+'output'+str(run), ex.PimpDofPattern )
            print 'dof: ',dof
            #if isinstance(dof,float) :
            #dof=[dof]
            #
            cumsum = 0
            iterres = [0]
            iterBelos = []
            for j in range(len(iter)):
                    if j>0 and iter[j]==0:
                            cumsum = iter[j-1]
                            iterres.append(j)
                    else:
                            iterBelos.append(iter[j]+cumsum)
                    iter[j] = iter[j]+cumsum
            #
            if( len(iterres)>1 ):
                    for j in range(max(len(iterres)-1,1)):
                            #print iterres[j],iterres[j+1]
                            res[iterres[j]:iterres[j+1],[0,2]] = res[iterres[j]:iterres[j+1],[0,2]]/sqrt(dof[j])
                    res[iterres[j+1]:,[0,2]] = res[iterres[j+1]:,[0,2]]/sqrt(dof[j])
            else:
                    res[:,[0,2]] = res[:,[0,2]]/sqrt(dof)
            #
            ls = li.next()
            m = mi.next()
            figure(1)
            #semilogy(iter[:],res[:,0],lw=2,label=lab,ls=ls )
            semilogy(iter,res[:,0],ls=ls )
            xlabel('Newton iteration')
            ylabel(r'$||\mathbf{F}||_2/\sqrt{N}$',ha='left',va='bottom',rotation=0)
            gca().yaxis.set_label_coords(-0.09, 1.075)
            grid(True)
            #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            #xlim((0,9))
            gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            #savefig('F.pdf')
            savefig('F.pdf',bbox_inches='tight')
            #	
            figure(2)
            #semilogy(iter[:],res[:,1],basey=2,lw=1,label=lab,ls=ls,marker=m )
            semilogy(iter[1:],res[1:,1],basey=2,lw=1,ls=ls,marker=m )
            xlabel('Newton iteration')
            ylabel(r'step width')
            grid(True)
            #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            savefig('lam.pdf',bbox_inches='tight')
            #
            figure(3)
            #semilogy(iter[:],res[:,2],lw=1,label=lab,ls=ls ,marker=m)
            semilogy(iter[1:],res[1:,2],lw=1,ls=ls ,marker=m)
            xlabel('Newton iteration')
            ylabel(r'$||\delta\mathbf{u}||_2/\sqrt{N}$')
            grid(True)
            #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            savefig('du.pdf',bbox_inches='tight')
            #
            #figure(4)
            ##if( len(iterBelos)==len(linIter) ):
                    ##plot(iterBelos[:],linIter[:],lw=2,label=lab,ls=ls )
            ##elif( len(iterBelos)-1==len(linIter) ):
                    ##plot(iterBelos[1:],linIter[:],marker=m,lw=0.5,label=lab,ls=ls )
            ##else:
            #if isinstance(linIter,float) :
                    #linIter=[linIter]
            #plot(range(1,len(linIter)+1),linIter,marker=m,lw=0.5,ls=ls )
            #xlabel('Newton iteration')
            #ylabel(r'linear iterations')
            #grid(True)
            ##legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            #gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            #savefig('liniter.pdf',bbox_inches='tight')
            ##
            #figure(5)
            ##semilogy(iterBelos[1:],linatol[:],marker=m,lw=0.5,label=lab,ls=ls )
            #semilogy(range(1,len(linatol)+1),linatol[:],marker=m,lw=0.5,ls=ls )
            #xlabel('Newton iteration')
            #ylabel(r'archieved tolerance of the linear solver')
            #grid(True)
            ##legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            #gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
            #savefig('lintol.pdf',bbox_inches='tight')
            #i += 1
    #show()

def plotSpeedup( paths, nps, lab=[], runs=[''],):
    time = []
    for path in paths:
            temptime = 1e99
            for run in runs:
                    tempnew =  ex.extract( path+'output'+str(run), ex.PimpSolveTimePattern,isarray=False )
                    print 'tempnew: ',tempnew
                    tempnew = tempnew
                    temptime = min(temptime, tempnew )
            #temptime =  ex.extract( path+'output', ex.PimpSolveTimePattern,isarray=False )
            #print temptime
            time.append(temptime)
            #time.append(  ex.extract( path+'output', ex.PimpSolveTimePattern,isarray=False ) )
    #  
    print 'nps: ',nps
    print 'time: ', time
    if len(lab)==0:
            plot(nps,time[0]/array(time),'.-',ms=5)
    else:
            plot(nps,time[0]/array(time),'.-',ms=5,label=lab)
    plot(nps,array(nps)/array(nps[0]),':',lw=2)
    ylim(ymin=1)
    gca().xaxis.set_ticks(nps)
    xlabel('number of cores')
    #gca().yaxis.set_label_position('top') 
    #gca().yaxis.set_label_coords(0., 1.1)
    ylabel('speed-up',ha='left',va='bottom',rotation=0)
    gca().yaxis.set_label_coords(-0.05, 1.075)
    #if( len(leg)!=0 ):
    grid(True)
    #savefig('speedup.pdf')
    #show()

def plotStrongScaling( paths, nps, lab=[], runs=['']):
    time = []
    for path in paths:
            temptime = 1e99
            for run in runs:
                    tempnew =  ex.extract( path+'output'+str(run), ex.PimpSolveTimePattern,isarray=False )
                    print 'tempnew: ',tempnew
                    tempnew = tempnew
                    temptime = min(temptime, tempnew )
            #temptime =  ex.extract( path+'output', ex.PimpSolveTimePattern,isarray=False )
            #print temptime
            time.append(temptime)
            #time.append(  ex.extract( path+'output', ex.PimpSolveTimePattern,isarray=False ) )
    #  
    print 'nps: ',nps
    print 'time: ', time
    if len(lab)==0:
            loglog(nps,time,'.-',ms=5,basex=2)
    else:
            loglog(nps,time,'.-',ms=5,label=lab,basex=2,basey=2)
            #loglog(nps,time,'.-',ms=5,label=lab)
    loglog(nps,time[0]*1./array(nps),'--',color='k',ms=5,label=lab,basex=2,basey=2)
    #loglog(nps,array(nps)/array(nps[0]),':',lw=2)
    #ylim(ymin=1)
    gca().xaxis.set_ticks(nps)
    grid(True)
    xlabel('number of cores')
    #gca().yaxis.set_label_position('top') 
    #gca().yaxis.set_label_coords(0., 1.1)
    ylabel('time[s]',ha='left',va='bottom',rotation=0)
    gca().yaxis.set_label_coords(-0.05, 1.075)
    #if( len(leg)!=0 ):
    grid(True)
    #savefig('speedup.pdf')
    #show()

def plotWeakScaling( paths, nps, lab=[], runs=['']):
    time = []
    for path in paths:
            temptime = 1e99
            for run in runs:
                    tempnew =  ex.extract( path+'output'+str(run), ex.PimpSolveTimePattern,isarray=False )
                    print 'tempnew: ',tempnew
                    tempnew = tempnew
                    temptime = min(temptime, tempnew )
            #temptime =  ex.extract( path+'output', ex.PimpSolveTimePattern,isarray=False )
            #print temptime
            time.append(temptime)
            #time.append(  ex.extract( path+'output', ex.PimpSolveTimePattern,isarray=False ) )
    #  
    print 'nps: ',nps
    print 'time: ', time
    if len(lab)==0:
            loglog(nps,time,'.-',ms=5,basex=2)
    else:
            loglog(nps,time,'.-',ms=5,label=lab,basex=2,basey=2)
            #loglog(nps,time,'.-',ms=5,label=lab)
    loglog(nps,time[0]*ones(len(nps)),'--',color='k',ms=5,label=lab,basex=2,basey=2)
    #loglog(nps,array(nps)/array(nps[0]),':',lw=2)
    #ylim(ymin=1)
    gca().xaxis.set_ticks(nps)
    grid(True)
    xlabel('number of cores')
    #gca().yaxis.set_label_position('top') 
    #gca().yaxis.set_label_coords(0., 1.1)
    ylabel('time[s]',ha='left',va='bottom',rotation=0)
    gca().yaxis.set_label_coords(-0.05, 1.075)
    #if( len(leg)!=0 ):
    grid(True)
    #savefig('speedup.pdf')
    #show()


def getTimes( paths, runs, pattern ):
    timeMin = []
    timeMean = []
    timeSTD = []
    fails = []
    for path in paths:
        temptime = [] 
        fails.append( 0. )
        for run in runs:
            tempnew = ex.extract( path+'output'+str(run), pattern, isarray=False )
            if( isinstance( tempnew, ndarray ) ):
                if( len(tempnew)>0 ):
                    temptime.append( tempnew[0] )
                else:
                    fails[-1] += 1.
            else:
                temptime.append( tempnew )
        timeMin.append( min(temptime) )
        timeMean.append( mean(temptime) )
        timeSTD.append( std(temptime) )
        fails[-1] /= len(runs)
    return timeMin, fails, timeMean, timeSTD


def plotEfficency(  paths, nps, label='', runs=[''], pattern=ex.PimpSolveTimePattern,scale=1, basex=10, basey=10, marker='', linestyle='-', color='b', ms=3 ):
    time, fails, timeMean, timeSTD = getTimes( paths, runs, pattern )
    print ''
    print label
    print 'nps: ',nps
    print 'time: ', time
    print 'fails: ', fails
    efficency = copy.deepcopy( nps )
    for i in range(len(time)):
        efficency[i] = time[0]/time[i]/nps[i]
    if len(label)==0:
        plot(nps,efficency,'.-',ms=ms, linestyle=linestyle, color=color)
    else:
        semilogx(nps,efficency,'.-', ms=ms, label=label, marker=marker, linestyle=linestyle, linewidth=1., color=color )
    return time
  

def addTime( paths, nps, label='', runs=[''], pattern=ex.PimpSolveTimePattern, scale=1, basex=10, basey=10, marker='', linestyle='-', color='', ms=3, lw=1. ):
    time, fails, timeMean, timeSTD = getTimes( paths, runs, pattern )
    print ''
    print label
    print 'nps: ',nps
    print 'time: ', time
    print 'timeMean: ', timeMean
    print 'timeSTD: ', timeSTD
    print 'fails: ', fails
    # errorbar( log(nps), log(timeMean), log(timeSTD) )
    # errorbar( log(nps), log(time), log(timeSTD) )
    if len(color)==0:
        loglog( nps,array(time)*scale, ms=ms, label=label, basex=basex, basey=basey, marker=marker, linestyle=linestyle, lw=lw )
    else:
        loglog( nps,array(time)*scale, ms=ms, label=label, basex=basex, basey=basey, marker=marker, linestyle=linestyle, lw=lw, color=color )
    legend(loc=0)
    return time
