""" usefull to generate plot about performance scaling/ iterations """
import copy
import pylab as pl
import extractor as ex
from plotting_constants import COLORS, MARKERC, LINES, LINEC


def plot_nonlinears(paths=None, filename='nonlinear', refs=1, labels=None):
    """ plots residual ... over iterations """
    legend_yes = True
    if labels is None:
        labels = paths
        legend_yes = False
    if paths is None:
        paths = ['./']
        labels = paths
        legend_yes = False
    for i, path in enumerate(paths):
        offset = 0
        for ref in range(refs):
            file_str = path+filename+str(ref)+'.txt'
            iter_count = pl.array(
                ex.extract(file_str, ex.NOXIterPattern))+offset
            offset = iter_count[-1]
            res = ex.extract(file_str, ex.NOXResPattern)
            print iter_count
            print res
            pl.figure(1)
            if ref == 0:
                pl.semilogy(iter_count, res[:, 0], marker='.', color=COLORS[i],
                            ls=LINES[i], label=labels[i])
                if legend_yes:
                    pl.legend(loc=0)
            else:
                pl.semilogy(iter_count, res[:, 0], marker='.', color=COLORS[i],
                            ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.ylabel(r'$\|\mathbf{r}\|$', ha='left', va='bottom', rotation=0)
            pl.gca().yaxis.set_label_coords(-0.08, 1.02)
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            # pl.gca().yaxis.set_label_coords(-0.09, 1.075)
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            pl.savefig('F.pdf', bbox_inches='tight')
            pl.figure(2)
            if ref == 0:
                pl.semilogy(iter_count[1:], res[1:, 1], basey=2, marker='.',
                            color=COLORS[i], ls=LINES[i], label=labels[i])
                if legend_yes:
                    pl.legend(loc=0)
            else:
                pl.semilogy(iter_count[1:], res[1:, 1], basey=2, marker='.',
                            color=COLORS[i], ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.ylabel(r'step width', ha='left', va='bottom', rotation=0)
            pl.gca().yaxis.set_label_coords(-0.08, 1.02)
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            pl.savefig('lam.pdf', bbox_inches='tight')
            #
            pl.figure(3)
            if ref == 0:
                pl.semilogy(iter_count[1:], res[1:, 2], marker='.',
                            color=COLORS[i], ls=LINES[i], label=labels[i])
                if legend_yes:
                    pl.legend(loc=0)
            else:
                pl.semilogy(iter_count[1:], res[1:, 2], marker='.',
                            color=COLORS[i], ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.ylabel(r'$||\delta\mathbf{q}||$', ha='left', va='bottom', rotation=0)
            pl.gca().yaxis.set_label_coords(-0.08, 1.03)
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            pl.savefig('du.pdf', bbox_inches='tight')


def plot_linears(paths=None, filename='Picard', leg=None, refs=1):
    """ plots linear iteration and tolerance """
    if paths is None:
        paths = ['./']
    for i, pre_str in enumerate(paths):
        offset = 0
        for ref in range(refs):
            file_str = pre_str + filename + str(ref) + '.txt'
            lin_iter = ex.extract(file_str, ex.BelosMaxItPattern)
            linatol = ex.extract(file_str, ex.BelosArTolPattern)
            print linatol
            pl.figure()
            if isinstance(lin_iter, float):  # wtf
                lin_iter = [lin_iter]
            pl.plot(pl.arange(1, len(lin_iter)+1) + offset, lin_iter,
                    marker='.', color=COLORS[i], ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.ylabel(r'linear iterations', ha='left', va='bottom', rotation=0)
            pl.gca().yaxis.set_label_coords(-0.08, 1.02)
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            if leg is not None:
                pl.legend(leg, loc=0)
            pl.savefig('liniter.pdf', bbox_inches='tight')
            #
            pl.figure()
            pl.semilogy(pl.arange(1, len(linatol)+1) + offset, linatol,
                        marker='.', color=COLORS[i], ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.ylabel(r'archieved tolerance of the linear solver', ha='left',
                      va='bottom', rotation=0)
            pl.gca().yaxis.set_label_coords(-0.08, 1.02)
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            if leg is not None:
                # legend(leg,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
                pl.legend(leg, loc=0)
            pl.savefig('lintol.pdf', bbox_inches='tight')
            offset += len(linatol)


def plotNOX(paths=None, filename='output', run='', newton=False):
    """ plots residual ... over iterations (deprecated) """
    if paths is None:
        paths = ['./']
    for path in paths:
        iter_count = ex.extract(path+filename+str(run), ex.NOXIterPattern)
        res = ex.extract(path+filename+str(run), ex.NOXResPattern)
        # dof = ex.extract(path+filename+str(run), ex.PimpDofPattern)[0][0]
        # print 'dof: ', dof
        print iter_count
        print res
        pl.figure(1)
        # pl.semilogy(iter_count, res[:, 0]/pl.sqrt(dof))
        # pl.semilogy(res[:, 0]/pl.sqrt(dof), marker='.')
        pl.semilogy(res[:, 0], marker='.')
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'$||\mathbf{r}||_2/\sqrt{N}$', ha='left', va='bottom',
                  rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        # pl.savefig('F.pdf', bbox_inches='tight')
        pl.figure(2)
        pl.semilogy(iter_count[1:], res[1:, 1], basey=2, marker='.')
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'step width', ha='left', va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        # pl.savefig('lam.pdf', bbox_inches='tight')
        #
        pl.figure(3)
        # pl.semilogy(iter_count[1:], res[1:, 2]/pl.sqrt(dof), marker='.')
        pl.semilogy(iter_count[1:], res[1:, 2], marker='.')
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'$||\delta\mathbf{q}||_2/\sqrt{N}$')
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        # pl.savefig('du.pdf', bbox_inches='tight')


def plotNOX2(paths=['./'], leg=[], run='', newton=False):
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
        #pl.semilogy(iter[:],res[:,0], label=lab,ls=ls)
        pl.semilogy(iter, res[:, 0], ls=ls)
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'$||\mathbf{r}||_2/\sqrt{N}$', ha='left', va='bottom',
                  rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #xlim((0,9))
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('F.pdf', bbox_inches='tight')
        #
        pl.figure(2)
        #semilogy(iter[:],res[:,1],basey=2, label=lab,ls=ls,marker=m)
        pl.semilogy(iter[1:], res[1:, 1], basey=2, ls=ls, marker=m)
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'step width', ha='left', va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('lam.pdf', bbox_inches='tight')
        #
        pl.figure(3)
        #semilogy(iter[:],res[:,2],label=lab,ls=ls ,marker=m)
        pl.semilogy(iter[1:], res[1:, 2], ls=ls, marker=m)
        if newton:
            pl.xlabel('Newton iteration')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'$||\delta\mathbf{q}||_2/\sqrt{N}$', ha='left', va='bottom',
                  rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('du.pdf', bbox_inches='tight')
        #
        #figure(4)
        ##if(len(iterBelos)==len(lin_iter)):
            ##plot(iterBelos[:],lin_iter[:],label=lab,ls=ls)
        ##elif(len(iterBelos)-1==len(lin_iter)):
            ##plot(iterBelos[1:],lin_iter[:],marker=m, lw=0.5,label=lab,ls=ls)
        ##else:
        #if isinstance(lin_iter,float) :
                #lin_iter=[lin_iter]
        #plot(range(1,len(lin_iter)+1),lin_iter,marker=m,lw=0.5,ls=ls)
        #xlabel('Newton iteration')
        #ylabel(r'linear iterations')
        ##legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
        #savefig('liniter.pdf',bbox_inches='tight')
        ##
        #figure(5)
        ##semilogy(iterBelos[1:],linatol[:],marker=m,lw=0.5,label=lab,ls=ls)
        #semilogy(range(1,len(linatol)+1),linatol[:],marker=m,lw=0.5,ls=ls)
        #xlabel('Newton iteration')
        #ylabel(r'archieved tolerance of the linear solver')
        ##legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
        #savefig('lintol.pdf',bbox_inches='tight')
        #i += 1
    #show()


def plotBelos(files=None, leg=None):
    if files is None:
        files = ['./Picard.txt']
    i = 0
    for file_str in files:
        lin_iter = ex.extract(file_str, ex.BelosMaxItPattern)
        linatol = ex.extract(file_str, ex.BelosArTolPattern)
        print linatol
        pl.figure(4)
        if isinstance(lin_iter, float):  # wtf
            lin_iter = [lin_iter]
        pl.plot(range(1, len(lin_iter)+1), lin_iter, marker='.')
        pl.xlabel('Picard iteration')
        pl.ylabel(r'linear iterations', ha='left', va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        if leg is not None:
            pl.legend(leg, loc=0)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('liniter.pdf', bbox_inches='tight')
        #
        pl.figure(5)
        pl.semilogy(range(1, len(linatol)+1), linatol, marker='.')
        pl.xlabel('Picard iteration')
        pl.ylabel(r'archieved tolerance of the linear solver', ha='left',
                  va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        # legend(leg,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        if leg is not None:
            pl.legend(leg, loc=0)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        pl.savefig('lintol.pdf', bbox_inches='tight')
        i += 1


def plotSpeedup(paths, nps, lab=None, runs=None):
    if lab is None:
        lab = []
    if runs is None:
        runs = ['']
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
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)


def plotStrongScaling(paths, nps, lab=None, runs=None):
    if lab is None:
        lab = []
    if runs is None:
        runs = ['']
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
    pl.xlabel('number of cores')
    pl.ylabel('time[s]', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)


def plotWeakScaling(paths, nps, lab=None, runs=None):
    if lab is None:
        lab = []
    if runs is None:
        runs = ['']
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
    pl.xlabel('number of cores')
    pl.ylabel('time[s]', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)


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


def plotEfficency(paths, nps, label='', runs=None,
                  pattern=ex.PimpSolveTimePattern, scale=1, basex=10, basey=10,
                  marker='', linestyle='-', color='b'):
    if runs is None:
        runs = ['']
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
        pl.plot(nps, efficency, '.-', linestyle=linestyle, color=color)
    else:
        pl.semilogx(nps, efficency, '.-', label=label, marker=marker,
                    linestyle=linestyle, color=color)
    return time


def addTime(paths, nps, label='', runs=None, pattern=ex.PimpSolveTimePattern,
            scale=1, basex=10, basey=10, marker='', linestyle='-', color=''):
    if runs is None:
        runs = ['']
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
        pl.loglog(nps, pl.array(time)*scale, label=label, basex=basex,
                  basey=basey, marker=marker, linestyle=linestyle)
    else:
        pl.loglog(nps, pl.array(time)*scale, label=label, basex=basex,
                  basey=basey, marker=marker, linestyle=linestyle,
                  color=color)
    pl.legend(loc=0)
    return time
