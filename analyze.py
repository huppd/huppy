""" prints mean of iter and tol and std """
import numpy as np
import extractor as ex


def analyze(step=''):
    """ analyze """
    #
<<<<<<< HEAD
    files = ['Picard'+step+'.txt', 'MHDtConvectionDiffusion'+step+'.txt',
=======
    files = ['Picard'+step+'.txt',
             'MHDtConvectionDiffusion'+step+'.txt',
>>>>>>> 6c94314f05726235beb6f13bb16d69dc7daa217d
             'DivGrad'+step+'.txt',
             'ModeNonlinearOp_ConvectionDiffusionVOp'+step+'.txt',
             'ConvectionDiffusionVOp'+step+'.txt']
    #
    for fil in files:
        stats = ex.extract(fil, ex.BelosIterPattern)
        count = len(stats[:, 0])
        print fil, ' (', count, ')'
        if count != 0:
            print 'total: ', sum(stats[:, 0])
            print 'iter: ', np.mean(stats[:, 0]), '+- ', np.std(stats[:, 0])
            print 'tol: ', np.mean(stats[:, 1]), '+- ', np.std(stats[:, 1])
        print


def compares(paths=None, step=''):
    """ compares different folders """
    if paths is None:
        paths = ['./']
    #
    files = ['Picard'+step+'.txt', 'MHDtConvectionDiffusion'+step+'.txt',
             'DivGrad'+step+'.txt',
             'ModeNonlinearOp_ConvectionDiffusionVOp'+step+'.txt',
             'ConvectionDiffusionVOp'+step+'.txt']
    #
    npath = len(paths)
    for fil in files:
        iter_tot = np.zeros(npath)
        iter_means = np.zeros(npath)
        tol_means = np.zeros(npath)
        iter_stds = np.zeros(npath)
        tol_stds = np.zeros(npath)
        counts = np.zeros(npath)
        print fil, ': ', paths
        for i, path in enumerate(paths):
            stats = ex.extract(path+fil, ex.BelosIterPattern)
            counts[i] = len(stats[:, 0])
            if counts[i] != 0:
                iter_tot[i] = np.sum(stats[:, 0])
                iter_means[i] = np.mean(stats[:, 0])
                tol_means[i] = np.mean(stats[:, 1])
                iter_stds[i] = np.std(stats[:, 0])
                tol_stds[i] = np.std(stats[:, 1])
        print 'counts: ', counts
        print 'total:  ', iter_tot
        print 'iter:   ', iter_means
        print '+-      ', iter_stds
        print 'tol:    ', tol_means
        print '+-      ', tol_stds
        print
    print


if __name__ == "__main__":
    analyze()
