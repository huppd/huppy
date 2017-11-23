""" analyze flows energy ... """
import pylab as pl

import extractor as ex
from plotting_constants import COLORS, LINES, MARKERS


def _plot_sugar(direc, emin, emax):
    pl.xlim(xmin=emin)
    pl.xlim(xmax=emax)
    pl.xlabel(r'$'+direc.lower()+'$')
    pl.ylabel('energy', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)


def load_energy_dir(path='./', direc='Y', ref='0', field='0',
                    iteration='0'):
    """ load energy profile """
    return pl.loadtxt(path + 'energy_' + direc + '_r' + ref + '_i' +
                      iteration + '_' + field + '.txt')


def load_energy_he(path='./', field='0'):
    """ load energy profile """
    return pl.loadtxt(path + 'energy_' + field + '.txt')


def plot_energy_dir(path='./', direc='Y', field='0', ref='0', iteration='0',
                    ls='-', color='b', label=''):
    """ plot energy profile """
    energy = load_energy_dir(path=path, direc=direc, field=field,
                             iteration=iteration, ref=ref)
    # pl.semilogy(energy[:, 0], energy[:, 1]*pl.sqrt(2.), ls=ls, color=color, label=label)
    pl.semilogy(energy[:, 0], energy[:, 1], ls=ls, color=color, label=label)
    _plot_sugar(direc, energy[0, 0], energy[-1, 0])



def plot_modeenergy_dir(path='./', direc='Y', field='1', ref='0',
                        iteration='0', ls='-', color='b', label=''):
    """ plot energy profile """
    cenergy = load_energy_dir(path=path, direc=direc, field='C'+field,
                              iteration=iteration, ref=ref)
    senergy = load_energy_dir(path=path, direc=direc, field='S'+field,
                              iteration=iteration, ref=ref)
    pl.semilogy(cenergy[:, 0], cenergy[:, 1]+senergy[:, 1], ls=ls, color=color,
                label=label)
    _plot_sugar(direc, cenergy[0, 0], cenergy[-1, 0])


def plot_energy_dir_all(path='./', direc='Y', fields=None, ref='0',
                        iterations=None):
    """ plot multipletimes """
    if fields is None:
        fields = ['0']
    if iterations is None:
        iterations = ['0']
    for i, field in enumerate(fields):
        for j, iteration in enumerate(iterations):
            if field == '0':
                plot_energy_dir(path=path, direc=direc, field=field,
                                iteration=iteration, ls=LINES[j],
                                color=COLORS[i], ref=ref,
                                label=r'$u_'+field+'^{('+iteration+')}$')
            else:
                plot_modeenergy_dir(path=path, direc=direc, field=field,
                                    iteration=iteration, ls=LINES[j],
                                    color=COLORS[i], ref=ref,
                                    label=r'$u_'+field+'^{('+iteration+')}$')
    pl.legend(loc=0)
    # pl.savefig('energyProfile' + fields[0]+str(len(fields)) + '.pdf',
               # bbox_inches='tight')


def he_energy(path='./', fields=None, modes=None):
    """ plot multipletimes """
    if fields is None:
        fields = ['0']
    if modes is None:
        modes = [1, 3]
    for i, field in enumerate(fields):
        if field == '0':
            energy = load_energy_he(path=path, field=field)
            for j in modes:
                label = r'$e_{0' + str(j) + '}$'
                pl.semilogy(energy[:, 0], energy[:, j], label=label)
        else:
            cenergy = load_energy_he(path=path, field='C'+field)
            senergy = load_energy_he(path=path, field='S'+field)
            for j in modes:
                label = r'$e_{' + field + str(j) + '}$'
                pl.semilogy(cenergy[:, 0], cenergy[:, 1]+senergy[:, 1],
                            label=label)
    pl.xlabel(r'$y$')
    pl.ylabel(r'$e$')
    pl.legend(loc=0)
    # pl.savefig('energyProfile' + fields[0]+str(len(fields)) + '.pdf',
               # bbox_inches='tight')


def digdeep(path='./', prefix='xv', refs=1, color=COLORS[0], ls=LINES[0]):
    """ analyze deep """
    offset = 0
    for ref in range(max(refs, 1)):
        if refs == 0:
            ref = 0
            iters = int(ex.extract(path + 'nonlinear.txt',
                                   ex.NOXIterPattern)[-1][0]) + 1
        else:
            iters = int(ex.extract(path + 'nonlinear' + str(ref) + '.txt',
                                   ex.NOXIterPattern)[-1][0]) + 1
        print iters
        n_modes = 0
        bla = pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(1)+'.txt')
        if bla.ndim == 1:
            n_modes = 1
        else:
            n_modes = bla.shape[0]
        print n_modes
        print bla
        norms = pl.zeros([iters, n_modes])
        for i in range(1, iters):
            print pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(i)+'.txt')
            if n_modes == 1:
                norms[i, :] = \
                    pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(i)+'.txt')[-1]
            else:
                norms[i, :] = pl.loadtxt(
                    path+prefix+'_'+str(ref)+'_'+str(i)+'.txt')[:, -1]
        for j in range(n_modes):
            pl.semilogy(pl.arange(iters)+offset, norms[:, j], color=color,
                        ls=ls, marker=MARKERS[j])
        offset += iters - 1


def plot_vs(path='./', refs=1):
    """ plots development of each norm over Picards iteration, corresponds to
    NOXPrePostSpecturm
    """
    prefixes = ['x', 'res', 'cor']
    fields = ['v', 'p']
    for prefix in prefixes:
        pl.figure()
        if prefix == 'x':
            pl.ylabel(r'$\|\mathbf{q}\|$', ha='left', va='bottom', rotation=0)
        elif prefix == 'res':
            pl.ylabel(r'$\|\mathbf{r}\|$', ha='left', va='bottom', rotation=0)
        elif prefix == 'cor':
            pl.ylabel(r'$\|\delta \mathbf{q}\|$', ha='left', va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        pl.xlabel(r'iteration step')
        pl.gca().get_xaxis().set_major_locator(
            pl.MaxNLocator(integer=True))
        for i, field in enumerate(fields):
            digdeep(path=path, prefix=prefix+field, refs=refs, color=COLORS[i],
                    ls=LINES[i])
        pl.savefig(prefix + '.pdf')


def plot_engergy_spectrum(path='./', ref=0, iters=None, prefix='xv', ls='-'):
    """ plots development of each norm over Picards iteration, corresponds to
    NOXPrePostSpecturm
    """
    if iters is None:
        iters = [0]
    pl.ylabel(r'$\|\hat{\mathbf{u}}_k\|$', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)
    pl.xlabel(r'$k$')
    pl.gca().get_xaxis().set_major_locator(
        pl.MaxNLocator(integer=True))
    for i in iters:
        spec = pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(i)+'.txt')
        print spec
        pl.semilogy(spec[:, 0], spec[:, 1], marker='.', ls=ls)


if __name__ == "__main__":
    print 'main'
