""" usefull to generate plot about performance scaling/ iterations """
import copy
import pylab as pl
import extractor as ex
from plotting_constants import COLORS, MARKERC, LINES, LINEC


def plot_nonlinears(paths=None, filename='nonlinear', refs=0, labels=None,
                    save=False):
    """ plots residual ... over iterations """
    legend_yes = True
    if labels is None:
        labels = paths
        legend_yes = False
    if paths is None:
        paths = ['./']
        labels = paths
        if len(paths) == 1:
            LINES[0] = '-'
        legend_yes = False
    if refs == 0:
        ref_strs = ['']
    else:
        ref_strs = []
        for ref in range(refs):
            ref_strs.append(str(ref))
    for i, path in enumerate(paths):
        offset = 0
        for ref_str in ref_strs:
            file_str = path+filename+ref_str+'.txt'
            iter_count = pl.array(
                ex.extract(file_str, ex.NOXIterPattern))+offset
            offset = iter_count[-1]
            res = ex.extract(file_str, ex.NOXResPattern)
            print(iter_count)
            print(res)
            pl.figure(1)
            pl.semilogy(iter_count, res[:, 0], marker='.', color=COLORS[i],
                        ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.ylabel(r'$\|\mathbf{r}\|$')
            if refs == 0:
                pl.semilogy(iter_count, res[:, 0], marker='.', color=COLORS[i],
                            ls=LINES[i], label=labels[i])
            else:
                pl.semilogy(iter_count, res[:, 0], marker='.', color=COLORS[i],
                            ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.semilogy(iter_count, res[:, 0], marker='.', color=COLORS[i],
                        linestyle=LINES[i], label=labels[i])
            if legend_yes:
                # pl.legend(loc=0)
                pl.legend(loc=0, handletextpad=0.1)
                pl.xlabel('Picard step')
            pl.ylabel(r'$\|\mathbf{r}\|$', ha='right', va='bottom', rotation=0)
            pl.gca().yaxis.set_label_coords(0.0, 1.02)
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            # pl.gca().yaxis.set_label_coords(-0.09, 1.075)
            # pl.savefig('F.pdf', bbox_inches='tight')
            pl.figure(2)
            pl.semilogy(iter_count[1:], res[1:, 1], basey=2, marker='.',
                        color=COLORS[i], ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.ylabel(r'step width')
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            # pl.savefig('lam.pdf', bbox_inches='tight')
            #
            pl.figure(3)
            pl.semilogy(iter_count[1:], res[1:, 2], marker='.',
                        color=COLORS[i], ls=LINES[i])
            pl.xlabel('Picard iteration')
            pl.ylabel(r'$||\delta\mathbf{q}||$')
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            # pl.savefig('du.pdf', bbox_inches='tight')
            if save:
                pl.savefig('F.pdf', bbox_inches='tight')
            pl.figure(2)
            pl.semilogy(iter_count[1:], res[1:, 1], basey=2, marker='.',
                        color=COLORS[i], linestyle=LINES[i],
                        label=labels[i])
            if legend_yes:
                # pl.legend(loc=0)
                pl.legend(loc=0, handletextpad=0.1)
            pl.xlabel('Picard step')
            pl.ylabel(r'step width', ha='right', va='bottom', rotation=0)
            pl.gca().yaxis.set_label_coords(0.0, 1.02)
            pl.gca().get_xaxis().set_major_locator(
                pl.MaxNLocator(integer=True))
            if save:
                pl.savefig('lam.pdf', bbox_inches='tight')
            #
            pl.figure(3)
            pl.semilogy(iter_count[1:], res[1:, 2], marker='.',
                        color=COLORS[i], linestyle=LINES[i],
                        label=labels[i])
            if legend_yes:
                # pl.legend(loc=0)
                pl.legend(loc=0, handletextpad=0.1)
            pl.xlabel('Picard step')
            pl.ylabel(r'$||\delta\mathbf{q}||$', ha='right', va='bottom',
                      rotation=0)
            pl.gca().yaxis.set_label_coords(0.0, 1.03)
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
            print(linatol)
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


def plotNOX(paths=None, filename='output', run='', newton=False, save=False):
    """ plots residual ... over iterations (deprecated) """
    if paths is None:
        paths = ['./']
    for path in paths:
        iter_count = ex.extract(path+filename+str(run), ex.NOXIterPattern)
        res = ex.extract(path+filename+str(run), ex.NOXResPattern)
        # dof = ex.extract(path+filename+str(run), ex.PimpDofPattern)[0][0]
        # print('dof: ', dof)
        print(iter_count)
        print(res)
        pl.figure(1)
        # pl.semilogy(iter_count, res[:, 0]/pl.sqrt(dof))
        # pl.semilogy(res[:, 0]/pl.sqrt(dof), marker='.')
        pl.semilogy(res[:, 0], marker='.')
        if newton:
            pl.xlabel('Newton step')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'$||\mathbf{r}||_2/\sqrt{N}$')
        # pl.ylabel(r'$||\mathbf{r}||_2/\sqrt{N}$', ha='left', va='bottom',
                  # rotation=0)
        # pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        if save:
            pl.savefig('F.pdf', bbox_inches='tight')
        pl.figure(2)
        pl.semilogy(iter_count[1:], res[1:, 1], basey=2, marker='.')
        if newton:
            pl.xlabel('Newton step')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'step width')
        # pl.ylabel(r'step width', ha='left', va='bottom', rotation=0)
        # pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        if save:
            pl.savefig('lam.pdf', bbox_inches='tight')
        #
        pl.figure(3)
        # pl.semilogy(iter_count[1:], res[1:, 2]/pl.sqrt(dof), marker='.')
        pl.semilogy(iter_count[1:], res[1:, 2], marker='.')
        if newton:
            pl.xlabel('Newton step')
        else:
            pl.xlabel('Picard step')
        pl.ylabel(r'$||\delta\mathbf{q}||_2/\sqrt{N}$')
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        if save:
            pl.savefig('du.pdf', bbox_inches='tight')


def plotNOX2(paths=['./'], leg=[], run='', newton=False, save=False):
    for path in paths:
        iters = ex.extract(path+'output'+str(run), ex.NOXIterPattern)
        res = ex.extract(path+'output'+str(run), ex.NOXResPattern)
        dof = ex.extract(path+'output'+str(run), ex.PimpDofPattern)
        print('dof: ', dof)
        # if isinstance(dof,float) :
        # dof=[dof]
        #
        cumsum = 0
        iterres = [0]
        iter_belos = []
        for j, iter_temp in enumerate(iters):
            if j > 0 and iter_temp == 0:
                cumsum = iters[j-1]
                iterres.append(j)
            else:
                iter_belos.append(iter_temp+cumsum)
            iters[j] = iter_temp+cumsum
        #
        if len(iterres) > 1:
            for j in range(max(len(iterres)-1, 1)):
                # print(iterres[j],iterres[j+1])
                res[iterres[j]:iterres[j+1], [0, 2]] = \
                    res[iterres[j]:iterres[j+1], [0, 2]]/pl.sqrt(dof[j])
            res[iterres[j+1]:, [0, 2]] = res[iterres[j+1]:,
                                             [0, 2]]/pl.sqrt(dof[j])
        else:
            res[:, [0, 2]] = res[:, [0, 2]]/pl.sqrt(dof)
        #
        linestyle = LINEC.next()
        m = MARKERC.next()
        pl.figure(1)
        # pl.semilogy(iters[:],res[:,0], label=lab,linestyle=linestyle)
        pl.semilogy(iters, res[:, 0], linestyle=linestyle)
        if newton:
            pl.xlabel('Newton step')
        else:
            pl.xlabel('Picard step')
        pl.ylabel(r'$||\mathbf{r}||_2/\sqrt{N}$', ha='left', va='bottom',
                  rotation=0)
        pl.gca().yaxis.set_label_coords(-0.09, 1.075)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #xlim((0,9))
        # legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        # xlim((0,9))
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        if save:
            pl.savefig('F.pdf', bbox_inches='tight')
        #
        pl.figure(2)
        # semilogy(iters[:],res[:,1],basey=2,
        # label=lab,linestyle=linestyle,marker=m)
        pl.semilogy(iters[1:], res[1:, 1], basey=2, linestyle=linestyle,
                    marker=m)
        if newton:
            pl.xlabel('Newton step')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'step width')
        pl.ylabel(r'step width', ha='left', va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.ylabel(r'step width', ha='left', va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        # legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        if save:
            pl.savefig('lam.pdf', bbox_inches='tight')
        #
        pl.figure(3)
        # semilogy(iters[:],res[:,2],label=lab,linestyle=linestyle ,marker=m)
        pl.semilogy(iters[1:], res[1:, 2], linestyle=linestyle, marker=m)
        if newton:
            pl.xlabel('Newton step')
        else:
            pl.xlabel('Picard iteration')
        pl.ylabel(r'$||\delta\mathbf{q}||_2/\sqrt{N}$')
        pl.ylabel(r'$||\delta\mathbf{q}||_2/\sqrt{N}$', ha='left', va='bottom',
                  rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.xlabel('Picard step')
        pl.ylabel(r'$||\delta\mathbf{q}||_2/\sqrt{N}$', ha='left', va='bottom',
                  rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        # legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
        if save:
            pl.savefig('du.pdf', bbox_inches='tight')
        #
        # figure(4)
        # #if(len(iter_belos)==len(lin_iter)):
            # #plot(itersBelos[:],lin_iter[:],label=lab,linestyle=linestyle)
        # #elif(len(iter_belos)-1==len(lin_iter)):
        # #plot(iter_belos[1:],lin_iter[:],marker=m,
        # lw=0.5,label=lab,linestyle=linestyle) #else:
        # if isinstance(lin_iter,float) :
        # lin_iter=[lin_iter]
        # plot(range(1,len(lin_iter)+1),lin_iter,marker=m,lw=0.5,linestyle=linestyle)
        # xlabel('Newton iteration')
        # ylabel(r'linear iterations')
        # #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        # gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
        # savefig('liniter.pdf',bbox_inches='tight')
        # #
        # figure(5)
        # #semilogy(iter_belos[1:],linatol[:],marker=m,lw=0.5,label=lab,linestyle=linestyle)
        # semilogy(range(1,len(linatol)+1),linatol[:],marker=m,lw=0.5,linestyle=linestyle)
        # xlabel('Newton iteration')
        # ylabel(r'archieved tolerance of the linear solver')
        # #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        # gca().get_xaxis().set_major_locator(MaxNLocator(integer=True))
        # savefig('lintol.pdf',bbox_inches='tight')
        # i += 1
    # show()


def plotBelos(files=None, leg=None):
    if files is None:
        files = ['./Picard.txt']
    i = 0
    for file_str in files:
        lin_iter = ex.extract(file_str, ex.BelosMaxItPattern)
        linatol = ex.extract(file_str, ex.BelosArTolPattern)
        print(linatol)
        pl.figure(4)
        if isinstance(lin_iter, float):  # wtf
            lin_iter = [lin_iter]
        pl.plot(range(1, len(lin_iter)+1), lin_iter, marker='.')
        pl.xlabel('Picard iteration')
        pl.ylabel(r'linear iterations')
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
        pl.ylabel(r'archieved tolerance of the linear solver')
        pl.ylabel(r'archieved tolerance of the linear solver', ha='left',
                  va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        # legend(leg,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        if leg is not None:
            pl.legend(leg, loc=0)
        pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))


def plot_linear(file_str='./Picard.txt', label=None, save=False, fig=1,
                offset=0, linestyle='-'):
    """ plots the linear iteration and achieved tolerance """
    lin_iter = ex.extract(file_str, ex.BelosMaxItPattern)
    linatol = ex.extract(file_str, ex.BelosArTolPattern)
    print(linatol)
    pl.figure(fig)
    if isinstance(lin_iter, float):  # wtf
        lin_iter = [lin_iter]
    pl.plot(pl.arange(1, len(lin_iter)+1)+offset, lin_iter, marker='.',
            label=label, linestyle=linestyle)
    pl.xlabel('Picard step')
    pl.ylabel(r'linear iterations', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)
    pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
    pl.gca().get_yaxis().set_major_locator(pl.MaxNLocator(integer=True))
    if save:
        pl.savefig('liniter.pdf', bbox_inches='tight')
    #
    pl.figure(fig+1)
    pl.semilogy(pl.arange(1, len(linatol)+1)+offset, linatol, marker='.',
                label=label, linestyle=linestyle)
    pl.xlabel('Picard step')
    # pl.ylabel(r'achieved tolerance of the linear solver', ha='left',
              # va='bottom', rotation=0)
    # pl.gca().yaxis.set_label_coords(-0.08, 1.02)
    pl.ylabel(r'achieved tolerance of the linear solver')
    pl.gca().get_xaxis().set_major_locator(pl.MaxNLocator(integer=True))
    if save:
        pl.savefig('lintol.pdf', bbox_inches='tight')
    offset += len(linatol)
    return offset


def plot_linears(path='./', filenames=None, leg=None, refs=0, save=False):
    """ plots linear iteration and tolerance """
    if filenames is None:
        filenames = [r'Picard', r'ConvectionDiffusionVOp',
                     r'ModeNonlinearOp_ConvectionDiffusionVOp', r'DivGrad']
    if refs == 0:
        refs_str = ['']
    else:
        refs_str = []
        for i in range(refs):
            refs_str.append(str(i))
    for i, file_pre in enumerate(filenames):
        offset = 0
        for ref in refs_str:
            file_str = path + file_pre + ref + '.txt'
            if file_pre == r'Picard':
                linestyle = '-'
            else:
                linestyle = ''
            offset = plot_linear(file_str=file_str, fig=2*i, offset=offset,
                                 linestyle=linestyle, save=False)
            pl.figure(2*i)
            if file_pre == r'Picard':
                pl.title('Picard problem')
                pl.xlabel('Picard step')
            elif file_pre == r'ConvectionDiffusionVOp':
                pl.title(r'Convection-diffusion problem')
                pl.xlabel('')
            elif file_pre == r'ModeNonlinearOp_ConvectionDiffusionVOp':
                pl.title(r'Harmonic convection-diffusion problem')
                pl.xlabel('')
            elif file_pre == r'DivGrad':
                pl.title(r'Poisson problem')
                pl.xlabel('')
            pl.figure(2*i+1)
            if file_pre == r'Picard':
                pl.title('Picard problem')
                pl.xlabel('Picard step')
            elif file_pre == r'ConvectionDiffusionVOp':
                pl.title(r'Convection-diffusion problem')
                pl.xlabel('')
            elif file_pre == r'ModeNonlinearOp_ConvectionDiffusionVOp':
                pl.title(r'Harmonic convection-diffusion problem')
                pl.xlabel('')
            elif file_pre == r'DivGrad':
                pl.title(r'Poisson problem')
                pl.xlabel('')
            if save:
                pl.figure(2*i)
                pl.savefig(file_pre+'_liniter.pdf', bbox_inches='tight')
                pl.figure(2*i+1)
                pl.savefig(file_pre+'_lintol.pdf', bbox_inches='tight')


def __my_cumsum(iters):
    cumsum = 0
    iterres = pl.copy(iters)
    for j, iter_temp in enumerate(iters):
        if j > 0 and iter_temp == 0:
            cumsum = iterres[j-1]
            iterres[j-1] -= 0.00
            iterres[j] += cumsum + 0.00
        else:
            iterres[j] += cumsum
    return iterres


def plot_refinement(path='./', save=False):
    """ plots residual refinement ... over iterations """
    file_str = path+'refinementTest.txt'
    res = pl.loadtxt(file_str)
    print(res)
    pl.figure(1)
    ax1 = pl.subplot(211)
    pl.subplots_adjust(hspace=0)
    iters = __my_cumsum(res[:,0])
    pl.semilogy(iters, res[:, 2]/(2.*res[:, 1] + 1), marker='.', color=COLORS[0],
                linestyle=LINES[0], label=r'$\|\mathbf{r}\|$')
    pl.semilogy(iters, res[:, 3]/res[:, 4]/2., marker='.', color=COLORS[1],
                linestyle=LINES[1],
                label=r'$\|\Delta r\|$')
    pl.ylabel(r'$\|\mathbf{r}\|$')
    pl.legend(loc=0)
    pl.subplot(212, sharex=ax1)
    for i in range(len(res[:, 1])):
        if res[i, 3] == 0.:
            res[i, 4] = 0
    pl.plot(iters, res[:, 1], marker='.', color=COLORS[0],
                linestyle=LINES[0], label=r'$N_f$')
    pl.plot(iters, res[:, 4], marker='.', color=COLORS[1],
                linestyle=LINES[1], label=r'$N_f^{\mathrm{inc}}$')
    pl.legend(loc=0)
    pl.ylabel(r'$N_f$')
    pl.xlabel('Picard step')
    pl.gca().get_xaxis().set_major_locator(
        pl.MaxNLocator(integer=True))
    pl.gca().get_yaxis().set_major_locator(
        pl.MaxNLocator(integer=True))
    if save:
        pl.savefig('refF.pdf', bbox_inches='tight')


def polt_speedup(paths, nps, lab=None, runs=None):
    """ plots speedup """
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
            print('tempnew: ', tempnew)
            tempnew = tempnew
            temptime = min(temptime, tempnew)
        time.append(temptime)
    #
    print('nps: ', nps)
    print('time: ', time)
    if not lab:
        pl.plot(nps, time[0]/pl.array(time), '.-', ms=5)
    else:
        pl.plot(nps, time[0]/pl.array(time), '.-', ms=5, label=lab)
    pl.plot(nps, pl.array(nps)/pl.array(nps[0]), ':', lw=2)
    pl.ylim(ymin=1)
    pl.gca().xaxis.set_ticks(nps)
    pl.xlabel('number of cores')
    pl.ylabel('speed-up', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.05, 1.075)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)


def plot_strongscaling(paths, nps, lab=None, runs=None):
    """ plots strong scaling """
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
            print('tempnew: ', tempnew)
            tempnew = tempnew
            temptime = min(temptime, tempnew)
        time.append(temptime)
    #
    print('nps: ', nps)
    print('time: ', time)
    if not lab:
        pl.loglog(nps, time, '.-', ms=5, basex=2)
    else:
        pl.loglog(nps, time, '.-', ms=5, label=lab, basex=2, basey=2)
    pl.loglog(nps, time[0]*1./pl.array(nps), '--', color='k', ms=5, label=lab,
              basex=2, basey=2)
    # loglog(nps,array(nps)/array(nps[0]),':',lw=2)
    # ylim(ymin=1)
    pl.gca().xaxis.set_ticks(nps)
    pl.xlabel('number of cores')
    pl.ylabel('time[s]', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.05, 1.075)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)


def plot_weakscaling(paths, nps, lab=None, runs=None):
    """ plots weak scaling """
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
            print('tempnew: ', tempnew)
            tempnew = tempnew
            temptime = min(temptime, tempnew)
        # print(temptime)
        time.append(temptime)
    #
    print('nps: ', nps)
    print('time: ', time)
    if not lab:
        pl.loglog(nps, time, '.-', ms=5, basex=2)
    else:
        pl.loglog(nps, time, '.-', ms=5, label=lab, basex=2, basey=2)
    pl.loglog(nps, time[0]*pl.ones(len(nps)), '--', color='k', ms=5,
              label=lab, basex=2, basey=2)
    pl.gca().xaxis.set_ticks(nps)
    pl.xlabel('number of cores')
    pl.ylabel('time[s]', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.05, 1.075)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)


def get_times(paths, runs, pattern):
    """ extracts times """
    time_min = []
    time_mean = []
    time_std = []
    fails = []
    for path in paths:
        temptime = []
        fails.append(0.)
        for run in runs:
            tempnew = ex.extract(path+'output'+str(run), pattern,
                                 isarray=False)
            if isinstance(tempnew, pl.ndarray):
                if tempnew:
                    temptime.append(tempnew[0])
                else:
                    fails[-1] += 1.
            else:
                temptime.append(tempnew)
        time_min.append(min(temptime))
        time_mean.append(pl.mean(temptime))
        time_std.append(pl.std(temptime))
        fails[-1] /= len(runs)
    return time_min, fails, time_mean, time_std


def plot_efficiency(paths, nps, label=None, runs=None,
                    pattern=ex.PimpSolveTimePattern,
                    marker='', linestyle='-', color='b'):
    """ plots efficiency """
    if runs is None:
        runs = ['']
    times, fails, times_mean, times_std = get_times(paths, runs, pattern)
    print('')
    print(label)
    print('nps: ', nps)
    print('times: ', times)
    print('fails: ', fails)
    efficency = copy.deepcopy(nps)
    for i, time in enumerate(times):
        efficency[i] = times[0]/time/nps[i]
    if label is None:
        pl.plot(nps, efficency, '.-', linestyle=linestyle, color=color)
    else:
        pl.semilogx(nps, efficency, '.-', label=label, marker=marker,
                    linestyle=linestyle, color=color)
    return time


def add_time(paths, nps, label='', runs=None, pattern=ex.PimpSolveTimePattern,
             scale=1, basex=10, basey=10, marker='', linestyle='-', color='',
             legend=True):
    """ adds time """
    if runs is None:
        runs = ['']
    time, fails, time_mean, time_std = get_times(paths, runs, pattern)
    print('')
    print(label)
    print('nps: ', nps)
    print('time: ', time)
    print('time_mean: ', time_mean)
    print('time_std: ', time_std)
    print('fails: ', fails)
    # errorbar(log(nps), log(time_mean), log(time_std))
    # errorbar(log(nps), log(time), log(time_std))
    if color:
        pl.loglog(nps, pl.array(time)*scale, label=label, basex=basex,
                  basey=basey, marker=marker, linestyle=linestyle,
                  color=color)
    else:
        pl.loglog(nps, pl.array(time)*scale, label=label, basex=basex,
                  basey=basey, marker=marker, linestyle=linestyle)
    if legend:
        pl.legend(loc=0)
    return time
