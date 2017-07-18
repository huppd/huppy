""" prints mean of iter and tol and std """
import numpy as np
import extractor as ex


def analyze(step=''):
    """ analyze """
    #
    files = ['Picard'+step+'.txt', 'MHDtConvectionDiffusion'+step+'.txt',
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
        means_iter = np.zeros(npath)
        means_tol = np.zeros(npath)
        stds_iter = np.zeros(npath)
        stds_tol = np.zeros(npath)
        counts = np.zeros(npath)
        print fil, ': ', paths
        for i, path in enumerate(paths):
            stats = ex.extract(path+fil, ex.BelosIterPattern)
            counts[i] = len(stats[:, 0])
            if counts[i] != 0:
                means_iter[i] = np.mean(stats[:, 0])
                means_tol[i] = np.mean(stats[:, 1])
                stds_iter[i] = np.std(stats[:, 0])
                stds_tol[i] = np.std(stats[:, 1])
        print 'counts: ', counts
        print 'iter:   ', means_iter
        print '+-      ', stds_iter
        print 'tol:    ', means_tol
        print '+-      ', stds_tol
        print
    print


if __name__ == "__main__":
    analyze()
