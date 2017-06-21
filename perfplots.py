""" usefull to generate plot about performance scaling/ iterations """
import copy
import pylab as pl
import extractor as ex
# from plotting_constants import COLORS, MARKERS, LINES
# from plotting_constants import COLORC, MARKERC, LINEC
from plotting_constants import MARKERC, LINEC


def plotNOX(paths=['./'], run='', newton=False):
    """ plots residual ... over iterations """
    for path in paths:
        iter_count = ex.extract(path+'output'+str(run), ex.NOXIterPattern)
        res = ex.extract(path+'output'+str(run), ex.NOXResPattern)
        dof = ex.extract(path+'output'+str(run), ex.PimpDofPattern)[0][0]
        print 'dof: ', dof
        print iter_count
        print res
        pl.figure(1)
        # pl.semilogy(iter_count, res[:, 0]/pl.sqrt(dof))
        pl.semilogy(res[:, 0]/pl.sqrt(dof))
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'$||\mathbf{F}||_2/\sqrt{N}$')
        # pl.gca().yaxis.set_label_coords(-0.09, 1.075)
        pl.grid(True)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        # pl.savefig('F.pdf', bbox_inches='tight')
        pl.figure(2)
        pl.semilogy(iter_count[1:], res[1:, 1], basey=2)
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'step width')
        pl.grid(True)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        # pl.savefig('lam.pdf', bbox_inches='tight')
        #
        pl.figure(3)
        pl.semilogy(iter_count[1:], res[1:, 2]/pl.sqrt(dof))
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'$||\delta\mathbf{u}||_2/\sqrt{N}$')
        pl.grid(True)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        # pl.savefig('du.pdf', bbox_inches='tight')


def plotBelos(files=['./Picard.txt'], leg=[], run=''):
    i = 0
    for file_str in files:
        linIter = ex.extract(file_str, ex.BelosMaxItPattern)
        linatol = ex.extract(file_str, ex.BelosArTolPattern)
        print linatol
        pl.figure(4)
        if isinstance(linIter, float):  # wtf
            linIter = [linIter]
        pl.plot(range(1, len(linIter)+1), linIter)
        pl.xlabel('Picard iteration')
        pl.ylabel(r'linear iterations')
        pl.grid(True)
        pl.legend(leg, loc=0)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('liniter.pdf', bbox_inches='tight')
        #
        pl.figure(5)
        pl.semilogy(range(1, len(linatol)+1), linatol)
        pl.xlabel('Picard iteration')
        pl.ylabel(r'archieved tolerance of the linear solver')
        pl.grid(True)
        # legend(leg,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.legend(leg, loc=0)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('lintol.pdf', bbox_inches='tight')
        i += 1


def plotNOX2(paths=['./'], leg=[], run=''):
    for path in paths:
        iter = ex.extract(path+'output'+str(run), ex.NOXIterPattern)
        res = ex.extract(path+'output'+str(run), ex.NOXResPattern)
        dof = ex.extract(path+'output'+str(run), ex.PimpDofPattern)
        print 'dof: ', dof
        #if isinstance(dof,float) :
        #dof=[dof]
        #
        cumsum = 0
        iterres = [0]
        iterBelos = []
        for j in range(len(iter)):
            if j > 0 and iter[j] == 0:
                cumsum = iter[j-1]
                iterres.append(j)
            else:
                iterBelos.append(iter[j]+cumsum)
            iter[j] = iter[j]+cumsum
        #
        if len(iterres) > 1:
            for j in range(max(len(iterres)-1, 1)):
                #print iterres[j],iterres[j+1]
                res[iterres[j]:iterres[j+1], [0, 2]] = \
                    res[iterres[j]:iterres[j+1], [0, 2]]/pl.sqrt(dof[j])
            res[iterres[j+1]:, [0, 2]] = res[iterres[j+1]:,
                                             [0, 2]]/pl.sqrt(dof[j])
        else:
            res[:, [0, 2]] = res[:, [0, 2]]/pl.sqrt(dof)
        #
        ls = LINEC.next()
        m = MARKERC.next()
        pl.figure(1)
        #pl.semilogy(iter[:],res[:,0],lw=2,label=lab,ls=ls)
        pl.semilogy(iter, res[:, 0], ls=ls)
        pl.xlabel('Newton iteration')
        pl.ylabel(r'$||\mathbf{F}||_2/\sqrt{N}$', ha='left', va='bottom',
                  rotation=0)
        pl.gca().yaxis.set_label_coords(-0.09, 1.075)
        pl.grid(True)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #xlim((0,9))
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        #savefig('F.pdf')
        pl.savefig('F.pdf', bbox_inches='tight')
        #
        pl.figure(2)
        #semilogy(iter[:],res[:,1],basey=2,lw=1,label=lab,ls=ls,marker=m)
        pl.semilogy(iter[1:], res[1:, 1], basey=2, lw=1, ls=ls, marker=m)
        pl.xlabel('Newton iteration')
        pl.ylabel(r'step width')
        pl.grid(True)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('lam.pdf', bbox_inches='tight')
        #
        pl.figure(3)
        #semilogy(iter[:],res[:,2],lw=1,label=lab,ls=ls ,marker=m)
        pl.semilogy(iter[1:], res[1:, 2], lw=1, ls=ls, marker=m)
        pl.xlabel('Newton iteration')
        pl.ylabel(r'$||\delta\mathbf{u}||_2/\sqrt{N}$')
        pl.grid(True)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('du.pdf', bbox_inches='tight')
        #
        #figure(4)
        ##if(len(iterBelos)==len(linIter)):
            ##plot(iterBelos[:],linIter[:],lw=2,label=lab,ls=ls)
        ##elif(len(iterBelos)-1==len(linIter)):
            ##plot(iterBelos[1:],linIter[:],marker=m,lw=0.5,label=lab,ls=ls)
        ##else:
        #if isinstance(linIter,float) :
                #linIter=[linIter]
        #plot(range(1,len(linIter)+1),linIter,marker=m,lw=0.5,ls=ls)
        #xlabel('Newton iteration')
        #ylabel(r'linear iterations')
        #grid(True)
        ##legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
        #savefig('liniter.pdf',bbox_inches='tight')
        ##
        #figure(5)
        ##semilogy(iterBelos[1:],linatol[:],marker=m,lw=0.5,label=lab,ls=ls)
        #semilogy(range(1,len(linatol)+1),linatol[:],marker=m,lw=0.5,ls=ls)
        #xlabel('Newton iteration')
        #ylabel(r'archieved tolerance of the linear solver')
        #grid(True)
        ##legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
        #savefig('lintol.pdf',bbox_inches='tight')
        #i += 1
    #show()


def plotSpeedup(paths, nps, lab=[], runs=[''],):
    time = []
    for path in paths:
        temptime = 1e99
        for run in runs:
            tempnew = ex.extract(path+'output'+str(run),
                                 ex.PimpSolveTimePattern, isarray=False)
            print 'tempnew: ', tempnew
            tempnew = tempnew
            temptime = min(temptime, tempnew)
        time.append(temptime)
    #
    print 'nps: ', nps
    print 'time: ', time
    if len(lab) == 0:
        pl.plot(nps, time[0]/pl.array(time), '.-', ms=5)
    else:
        pl.plot(nps, time[0]/pl.array(time), '.-', ms=5, label=lab)
    pl.plot(nps, pl.array(nps)/pl.array(nps[0]), ':', lw=2)
    pl.ylim(ymin=1)
    pl.gca().xaxis.set_ticks(nps)
    pl.xlabel('number of cores')
    pl.ylabel('speed-up', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.05, 1.075)
    pl.grid(True)


def plotStrongScaling(paths, nps, lab=[], runs=['']):
    time = []
    for path in paths:
        temptime = 1e99
        for run in runs:
            tempnew = ex.extract(path+'output'+str(run),
                                 ex.PimpSolveTimePattern, isarray=False)
            print 'tempnew: ', tempnew
            tempnew = tempnew
            temptime = min(temptime, tempnew)
        time.append(temptime)
    #
    print 'nps: ', nps
    print 'time: ', time
    if len(lab) == 0:
        pl.loglog(nps, time, '.-', ms=5, basex=2)
    else:
        pl.loglog(nps, time, '.-', ms=5, label=lab, basex=2, basey=2)
    pl.loglog(nps, time[0]*1./pl.array(nps), '--', color='k', ms=5, label=lab,
              basex=2, basey=2)
    #loglog(nps,array(nps)/array(nps[0]),':',lw=2)
    #ylim(ymin=1)
    pl.gca().xaxis.set_ticks(nps)
    pl.grid(True)
    pl.xlabel('number of cores')
    pl.ylabel('time[s]', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.05, 1.075)
    pl.grid(True)


def plotWeakScaling(paths, nps, lab=[], runs=['']):
    time = []
    for path in paths:
        temptime = 1e99
        for run in runs:
            tempnew = ex.extract(path+'output'+str(run),
                                 ex.PimpSolveTimePattern, isarray=False)
            print 'tempnew: ', tempnew
            tempnew = tempnew
            temptime = min(temptime, tempnew)
        #print temptime
        time.append(temptime)
    #
    print 'nps: ', nps
    print 'time: ', time
    if len(lab) == 0:
        pl.loglog(nps, time, '.-', ms=5, basex=2)
    else:
        pl.loglog(nps, time, '.-', ms=5, label=lab, basex=2, basey=2)
    pl.loglog(nps, time[0]*pl.ones(len(nps)), '--', color='k', ms=5,
              label=lab, basex=2, basey=2)
    pl.gca().xaxis.set_ticks(nps)
    pl.grid(True)
    pl.xlabel('number of cores')
    pl.ylabel('time[s]', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.05, 1.075)
    pl.grid(True)


def getTimes(paths, runs, pattern):
    timeMin = []
    timeMean = []
    timeSTD = []
    fails = []
    for path in paths:
        temptime = []
        fails.append(0.)
        for run in runs:
            tempnew = ex.extract(path+'output'+str(run), pattern,
                                 isarray=False)
            if isinstance(tempnew, pl.ndarray):
                if len(tempnew) > 0:
                    temptime.append(tempnew[0])
                else:
                    fails[-1] += 1.
            else:
                temptime.append(tempnew)
        timeMin.append(min(temptime))
        timeMean.append(pl.mean(temptime))
        timeSTD.append(pl.std(temptime))
        fails[-1] /= len(runs)
    return timeMin, fails, timeMean, timeSTD


def plotEfficency(paths, nps, label='', runs=[''],
                  pattern=ex.PimpSolveTimePattern, scale=1, basex=10, basey=10,
                  marker='', linestyle='-', color='b', ms=3):
    time, fails, timeMean, timeSTD = getTimes(paths, runs, pattern)
    print ''
    print label
    print 'nps: ', nps
    print 'time: ', time
    print 'fails: ', fails
    efficency = copy.deepcopy(nps)
    for i in range(len(time)):
        efficency[i] = time[0]/time[i]/nps[i]
    if len(label) == 0:
        pl.plot(nps, efficency, '.-', ms=ms, linestyle=linestyle, color=color)
    else:
        pl.semilogx(nps, efficency, '.-', ms=ms, label=label, marker=marker,
                    linestyle=linestyle, linewidth=1., color=color)
    return time


def addTime(paths, nps, label='', runs=[''], pattern=ex.PimpSolveTimePattern,
            scale=1, basex=10, basey=10, marker='', linestyle='-', color='',
            ms=3, lw=1.):
    time, fails, timeMean, timeSTD = getTimes(paths, runs, pattern)
    print ''
    print label
    print 'nps: ', nps
    print 'time: ', time
    print 'timeMean: ', timeMean
    print 'timeSTD: ', timeSTD
    print 'fails: ', fails
    # errorbar(log(nps), log(timeMean), log(timeSTD))
    # errorbar(log(nps), log(time), log(timeSTD))
    if len(color) == 0:
        pl.loglog(nps, pl.array(time)*scale, ms=ms, label=label, basex=basex,
                  basey=basey, marker=marker, linestyle=linestyle, lw=lw)
    else:
        pl.loglog(nps, pl.array(time)*scale, ms=ms, label=label, basex=basex,
                  basey=basey, marker=marker, linestyle=linestyle, lw=lw,
                  color=color)
    pl.legend(loc=0)
    return time
