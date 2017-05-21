""" manipultes parameterlist xml files"""
import xml.etree.ElementTree as ET


def setParameter(root, name, value):
    for child in root.iter('Parameter'):
        if child.attrib['name'] == name:
            child.attrib['value'] = str(value)


def set(fname, name, value):
    tree = ET.parse(fname)
    #
    root = tree.getroot()
    #
    setParameter(root, name, value)
    #
    tree.write(fname)


def setIDS(fname):
    tree = ET.parse(fname)
    #
    root = tree.getroot()
    #
    i = 0
    for child in root.iter('ParameterList'):
        child.attrib['id'] = str(i)
        i = i+1
    for child in root.iter('Parameter'):
        child.attrib['id'] = str(i)
        i = i+1
    #
    tree.write(fname)


def setOutput(fname):
    tree = ET.parse('parameterOut.xml')
    #
    root = tree.getroot()
    # remove Output Stream
    parents = root.findall('.//Parameter[@name="Output Stream"]...')
    for parent in parents:
        for child in parent.iter():
            if child.attrib['name'] == 'Output Stream':
                parent.remove(child)
    # remove My PID
    parents = root.findall('.//Parameter[@name="MyPID"]...')
    for parent in parents:
        for child in parent.iter():
            if child.attrib['name'] == 'MyPID':
                parent.remove(child)
    #
    tree.write(fname)
    setIDS(fname)
