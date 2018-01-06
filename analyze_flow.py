""" analyze flows energy ... """
import pylab as pl

import extractor as ex
from plotting_constants import COLORS, LINES, MARKERS


def _plot_sugar(direc, emin, emax):
    pl.xlim(xmin=emin)
    pl.xlim(xmax=emax)
    pl.xlabel(r'$'+direc.lower()+'$')
<<<<<<< HEAD
    pl.ylabel('energy')
=======
    pl.ylabel('energy', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)
>>>>>>> 6c94314f05726235beb6f13bb16d69dc7daa217d


def load_energy_dir(path='./', direc='Y', refine='0', field='0',
                    iteration='0'):
    """ load energy profile """
    return pl.loadtxt(path + 'energy_' + direc + '_r' + refine + '_i' +
                      iteration + '_' + field + '.txt')


def plot_energy_dir(path='./', direc='Y', field='0', refine='0', iteration='0',
                    ls='-', color='b', label=''):
    """ plot energy profile """
    energy = load_energy_dir(path=path, direc=direc, field=field,
                             iteration=iteration, refine=refine)
    pl.semilogy(energy[:, 0], energy[:, 1], ls=ls, color=color, label=label)
    _plot_sugar(direc, energy[0, 0], energy[-1, 0])


def plot_modeenergy_dir(path='./', direc='Y', field='1', refine='0',
                        iteration='0', ls='-', color='b', label=''):
    """ plot energy profile """
    cenergy = load_energy_dir(path=path, direc=direc, field='C'+field,
                              iteration=iteration, refine=refine)
    senergy = load_energy_dir(path=path, direc=direc, field='S'+field,
                              iteration=iteration, refine=refine)
    pl.semilogy(cenergy[:, 0], cenergy[:, 1]+senergy[:, 1], ls=ls, color=color,
                label=label)
    _plot_sugar(direc, cenergy[0, 0], cenergy[-1, 0])


def plot_energy_dir_all(path='./', direc='Y', fields=None, refine='0',
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
                                color=COLORS[i], refine=refine,
                                label=r'$u_'+field+'^{('+iteration+')}$')
            else:
                plot_modeenergy_dir(path=path, direc=direc, field=field,
                                    iteration=iteration, ls=LINES[j],
                                    color=COLORS[i], refine=refine,
                                    label=r'$u_'+field+'^{('+iteration+')}$')
    pl.legend(loc=0)
<<<<<<< HEAD
    pl.savefig('energyProfile' + fields[0]+str(len(fields)) + '.pdf',
               bbox_inches='tight')
=======
    # pl.savefig('energyProfile' + fields[0]+str(len(fields)) + '.pdf',
               # bbox_inches='tight')
>>>>>>> 6c94314f05726235beb6f13bb16d69dc7daa217d


def digdeep(path='./', prefix='xv', refs=1, color=COLORS[0], ls=LINES[0]):
    """ analyze deep """
    offset = 0
    for ref in range(refs):
        iters = int(ex.extract(path + 'nonlinear' + str(ref) + '.txt',
                               ex.NOXIterPattern)[-1][0]) + 1
        print iters
        n_modes = 0
        bla = pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(0)+'.txt')
        if bla.ndim == 1:
            n_modes = 1
        else:
            n_modes = bla.shape[0]
        print n_modes
        print bla
        norms = pl.zeros([iters, n_modes])
        for i in range(iters):
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
<<<<<<< HEAD
            pl.ylabel(r'$\|\mathbf{q}\|$')
        elif prefix == 'res':
            pl.ylabel(r'$\|\mathbf{r}\|$')
        elif prefix == 'cor':
            pl.ylabel(r'$\|\delta \mathbf{q}\|$')
=======
            pl.ylabel(r'$\|\mathbf{q}\|$', ha='left', va='bottom', rotation=0)
        elif prefix == 'res':
            pl.ylabel(r'$\|\mathbf{r}\|$', ha='left', va='bottom', rotation=0)
        elif prefix == 'cor':
            pl.ylabel(r'$\|\delta \mathbf{q}\|$', ha='left', va='bottom', rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
>>>>>>> 6c94314f05726235beb6f13bb16d69dc7daa217d
        pl.xlabel(r'iteration step')
        pl.gca().get_xaxis().set_major_locator(
            pl.MaxNLocator(integer=True))
        for i, field in enumerate(fields):
            digdeep(path=path, prefix=prefix+field, refs=refs, color=COLORS[i],
                    ls=LINES[i])
<<<<<<< HEAD
=======
        pl.savefig(prefix + '.pdf')


def plot_engergy_spectrum(path='./', ref=0, iters=None, prefix='xv'):
    """ plots development of each norm over Picards iteration, corresponds to
    NOXPrePostSpecturm
    """
    if iters is None:
        iters = [0]
    
    pl.ylabel(r'$\|\mathbf{e}\|$', ha='left', va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)
    pl.xlabel(r'mode')
    pl.gca().get_xaxis().set_major_locator(
        pl.MaxNLocator(integer=True))
    for i in iters:
        spec = pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(i)+'.txt')
        print spec
        pl.semilogy(spec[:, 0], spec[:, 1], marker='.')
>>>>>>> 6c94314f05726235beb6f13bb16d69dc7daa217d


if __name__ == "__main__":
    print 'main'
