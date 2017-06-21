""" anlayze flows energy ... """
import pylab as pl
from plotting_constants import LINES, COLORS


def _plot_sugar(direc, emin, emax):
    pl.xlim(xmin=emin)
    pl.xlim(xmax=emax)
    pl.xlabel(r'$'+direc+'$')
    pl.ylabel('energy')


def load_energy_dir(path='./', direc='Y', field='0', iteration='0'):
    """ load energy profile """
    return pl.loadtxt(path+'energy'+direc+'_'+field+'_'+iteration+'.txt')


def plot_energy_dir(path='./', direc='Y', field='0', iteration='0', ls='-',
                    color='b', label=''):
    """ plot energy profile """
    energy = load_energy_dir(path, direc, field, iteration)
    pl.semilogy(energy[:, 0], energy[:, 1], ls=ls, color=color, label=label)
    _plot_sugar(direc, energy[0, 0], energy[-1, 0])


def plot_modeenergy_dir(path='./', direc='Y', field='1', iteration='0', ls='-',
                        color='b', label=''):
    """ plot energy profile """
    cenergy = load_energy_dir(path, direc, 'C'+field, iteration)
    senergy = load_energy_dir(path, direc, 'S'+field, iteration)
    pl.semilogy(cenergy[:, 0], cenergy[:, 1]+senergy[:, 1], ls=ls, color=color,
                label=label)
    _plot_sugar(direc, cenergy[0, 0], cenergy[-1, 0])


def plot_energy_dir_all(path='./', direc='Y', fields=['0'], iterations=['0']):
    """ plot multipletimes """
    for i, field in enumerate(fields):
        for j, iteration in enumerate(iterations):
            if field == '0':
                plot_energy_dir(path, direc, field, iteration, ls=LINES[j],
                                color=COLORS[i],
                                label=r'$u_'+field+'^{('+iteration+')}$')
            else:
                plot_modeenergy_dir(path, direc, field, iteration, ls=LINES[j],
                                    color=COLORS[i],
                                    label=r'$u_'+field+'^{('+iteration+')}$')
    pl.legend(loc=0)


if __name__ == "__main__":
    print 'main'
