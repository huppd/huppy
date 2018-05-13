""" analyze flows energy ... """
import pylab as pl

import extractor as ex
from plotting_constants import COLORS, LINES, MARKERS


def _plot_sugar(direc, emin, emax):
    pl.xlim(xmin=emin)
    pl.xlim(xmax=emax)
    pl.xlabel(r'$'+direc.lower()+'$')
    # pl.ylabel('energy')
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
                    linestyle='-', color='b', label=''):
    """ plot energy profile """
    energy = load_energy_dir(path=path, direc=direc, field=field,
                             iteration=iteration, ref=ref)
    pl.semilogy(energy[:, 0], energy[:, 1], linestyle=linestyle, color=color,
                label=label)
    _plot_sugar(direc, energy[0, 0], energy[-1, 0])


def plot_modeenergy_dir(path='./', direc='Y', field='1', ref='0',
                        iteration='0', linestyle='-', color='b', label=''):
    """ plot energy profile """
    cenergy = load_energy_dir(path=path, direc=direc, field='C'+field,
                              iteration=iteration, ref=ref)
    senergy = load_energy_dir(path=path, direc=direc, field='S'+field,
                              iteration=iteration, ref=ref)
    pl.semilogy(cenergy[:, 0], cenergy[:, 1]+senergy[:, 1],
                linestyle=linestyle, color=color, label=label)
    _plot_sugar(direc, cenergy[0, 0], cenergy[-1, 0])


def plot_energy_dir_all(path='./', direc='Y', fields=None, ref='0',
                        iterations=None, save=False):
    """ plot multipletimes """
    if fields is None:
        fields = ['0']
    if iterations is None:
        iterations = ['0']
    for i, field in enumerate(fields):
        for j, iteration in enumerate(iterations):
            if field == '0':
                plot_energy_dir(path=path, direc=direc, field=field,
                                iteration=iteration, linestyle=LINES[j],
                                color=COLORS[i], ref=ref,
                                label=r'$u_'+field+'^{('+iteration+')}$')
            else:
                plot_modeenergy_dir(path=path, direc=direc, field=field,
                                    iteration=iteration, linestyle=LINES[j],
                                    color=COLORS[i], ref=ref,
                                    label=r'$u_'+field+'^{('+iteration+')}$')
    pl.legend(loc=0)
    if save:
        pl.savefig(path + 'energyProfile' + fields[0]+str(len(fields)) +
                   '.pdf', bbox_inches='tight')


def he_energy(path='./', fields=None, modes=None, save=False, linestyle='-',
              xmax=600, ymin=1.e-8, loc=0):
    """ plot multipletimes """
    if fields is None:
        fields = ['0']
    if modes is None:
        modes = [2, 4]
    pl.gca().set_color_cycle(None)
    for field in fields:
        if field == '0':
            energy = load_energy_he(path=path, field=field)
            for j in modes:
                label = r'$e_{0' + str(j-1) + '}$'
                pl.semilogy(energy[:-1, 0], (energy[:-1, j])/pl.pi,
                            label=label, linestyle=linestyle)
        else:
            cenergy = load_energy_he(path=path, field='C'+field)
            senergy = load_energy_he(path=path, field='S'+field)
            for j in modes:
                label = r'$e_{' + field + str(j-1) + '}$'
                pl.semilogy(cenergy[:-1, 0],
                            (cenergy[:-1, j]+senergy[:-1, j])/pl.pi,
                            label=label, linestyle=linestyle)
    pl.ylim(ymin=ymin)
    pl.ylim(ymax=1.)
    pl.xlim(xmin=0)
    pl.xlim(xmax=xmax)
    pl.xlabel(r'$y$')
    pl.ylabel(r'$e$')
    pl.legend(loc=loc, fontsize=8, labelspacing=0.1)
    if save:
        pl.savefig(path + 'energyProfile' + fields[0]+str(len(fields)) +
                   '.pdf', bbox_inches='tight')


def digdeep(path='./', prefix='xv', refs=1, color=COLORS[0],
            linestyle=LINES[0]):
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
        print(prefix)
        print('iters:', iters)
        n_modes = 0
        bla = pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(1)+'.txt')
        if bla.ndim == 1:
            n_modes = 1
        else:
            n_modes = bla.shape[0]
        print('#modes:', n_modes)
        print(bla)
        norms = pl.zeros([iters, n_modes])
        for i in range(1, iters):
            print(pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(i)+'.txt'))
            if n_modes == 1:
                norms[i, :] = \
                    pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(i)+'.txt')[-1]
            else:
                norms[i, :] = pl.loadtxt(
                    path+prefix+'_'+str(ref)+'_'+str(i)+'.txt')[:, -1]
        for j in range(n_modes):
            pl.semilogy(pl.arange(1, iters)+offset, norms[1:, j], color=color,
                        linestyle=linestyle, marker=MARKERS[j])
        offset += iters - 1
    print()


def plot_vs(path='./', refs=1, save=False):
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
            pl.ylabel(r'$\|\delta \mathbf{q}\|$', ha='left', va='bottom',
                      rotation=0)
        pl.gca().yaxis.set_label_coords(-0.08, 1.02)
        pl.xlabel(r'iteration step')
        pl.gca().get_xaxis().set_major_locator(
            pl.MaxNLocator(integer=True))
        for i, field in enumerate(fields):
            digdeep(path=path, prefix=prefix+field, refs=refs, color=COLORS[i],
                    linestyle=LINES[i])
        if save:
            pl.savefig(prefix + '.pdf')


def plot_engergy_spectrum(path='./', ref=0, iters=None, prefix='xv',
                          linestyle='-', label=None, scale=1.):
    """ plots development of each norm over Picards iteration, corresponds to
    NOXPrePostSpecturm
    """
    if iters is None:
        iters = [0]
    pl.ylabel(r'$\frac{1}{2}\|\hat{\mathbf{u}}_k\|^2_2$', ha='left',
              va='bottom', rotation=0)
    pl.gca().yaxis.set_label_coords(-0.08, 1.02)
    pl.xlabel(r'$k$')
    pl.gca().get_xaxis().set_major_locator(
        pl.MaxNLocator(integer=True))
    for i in iters:
        spec = pl.loadtxt(path+prefix+'_'+str(ref)+'_'+str(i)+'.txt')
        print(spec)
        pl.semilogy(spec[:, 0], 0.5*scale*spec[:, 1]**2, marker='.',
                    linestyle=linestyle, label=label)


if __name__ == "__main__":
    print('main')
