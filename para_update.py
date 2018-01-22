""" updates parameter xml file for refinement """

import xml.etree.ElementTree as ET
import numpy as np


def update(fname='paramterOut.xml', tol=1.e-6):
    """ reads refine and changer parameter accordingly """
    refine = np.loadtxt('refinement.txt')
    nf = refine[-1, 1] - 1
    nf_inc = refine[-1, 4]
    nf_new = nf + nf_inc
    tree = ET.parse(fname)
    root = tree.getroot()
    # setting nf and npf
    for child in root.iter('Parameter'):
        if child.attrib['name'] == 'nf':
            child.attrib['value'] = int(nf_new)
        if child.attrib['name'] == 'npf':
            child.attrib['value'] = int(nf_new)

    # setting NormF
    for child in root.iter('ParameterList'):
        if child.attrib['name'] == 'Test 0':
            for cchild in child.iter('Parameter'):
                if cchild.attrib['name'] == 'Tolerance':
                    cchild.attrib['value'] = float(1.e-6*float(nf_new))
