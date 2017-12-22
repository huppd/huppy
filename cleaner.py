""" small script to remove Pimpact-files """
import os


FIELDS = ['S', 'X', 'Y', 'Z']


def remove_until(i=0, path='./', nf=0):
    """ removes restart files to certain iteration """
    if i<99:
        for j in range(1, i):
            for ftype in FIELDS:
                for f in range(2*nf+1):
                    if ftype == 'S':
                        key = 'pre'
                    else:
                        key = 'vel'+ftype
                    fname = key+'_restart'+str(j*100+f).zfill(5)+'.h5'
                    print('rm '+fname+'\t', end='')
                    try:
                        os.remove(path+fname)
                        print('check')
                    except OSError:
                        print('fail')
    else:
        print('Are you sure? i>=100')


if __name__ == "__main__":
    print('hello')
