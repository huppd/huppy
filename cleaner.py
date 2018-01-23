""" small script to remove Pimpact-files """
import os
import xml.etree.ElementTree as ET
import numpy as np


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


def remove_auto(path='./'):
    """ reads refine and then cleans """
    refine = np.loadtxt('refinementTest.txt')
    i = int(refine[-1, 0])
    nf = int(refine[-1, 1]) - 1
    remove_until(i=i, path=path, nf=nf)



def update(fname='parameterOut.xml', tol=1.e-6):
    """ reads refine and changer parameter accordingly """
    refine = np.loadtxt('refinementTest.txt')
    nf = int(refine[-1, 1]) - 1
    nf_inc = int(refine[-1, 4])
    nf_new = nf + nf_inc
    tol = 1.0e-6*float(nf_new)
    print( 'nf: ', nf)
    print( 'nf_inc: ', nf_inc)
    print( 'tol: ', tol)
    tree = ET.parse(fname)
    root = tree.getroot()
    # setting nf and npf
    for child in root.iter('Parameter'):
        if child.attrib['name'] == 'nf':
            child.attrib['value'] = str(nf_new)
        if child.attrib['name'] == 'npf':
            child.attrib['value'] = str(nf_new)

    # setting NormF
    for child in root.iter('ParameterList'):
        if child.attrib['name'] == 'Test 0':
            for cchild in child.iter('Parameter'):
                if cchild.attrib['name'] == 'Tolerance':
                    cchild.attrib['value'] = str(tol)

    tree.write(fname)


if __name__ == "__main__":
    print('hello')
