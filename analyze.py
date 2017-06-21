""" prints mean of iter and tol and std """
import pylab as py
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
            print 'iter: ', py.mean(stats[:, 0]), '+- ', py.std(stats[:, 0])
            print 'tol: ', py.mean(stats[:, 1]), '+- ', py.std(stats[:, 1])
        print


if __name__ == "__main__":
    analyze()
