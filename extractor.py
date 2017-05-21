"""@package extractor
uses regular expression to extract results from pimpact resuls and stores them
in numpy array files
"""
import re
import numpy
#from pylab import *
inf = 1e9999

# lin solver
BelosIterPattern = re.compile(
    r"Iter[ ]+(\d+), \[ +\d+\] :    (\d+.\d+e[-,+]{0,1}\d+)")
# BelosMaxItPattern = re.compile(
    # r"[ ]+OK...........Number of Iterations = (\d+) [<,==] \d+")
BelosMaxItPattern = re.compile(
    r"[\t, ]+[OK,Failed]+[.]+Number of Iterations = (\d+) [<,=]+ \d+")
BelosArTolPattern = re.compile(
    r"[\t, ]+residual \[ \d+ \] = (\d+.\d+e{0,1}[-,+]{0,1}\d+) [<,>] \d+.\d+e{0,1}[-,+]{0,1}\d+")

# nonlin solver
NOXIterPattern = re.compile(r"-- Nonlinear Solver Step (\d+) -- ")
NOXResPattern = re.compile(
    r"\|\|F\|\| = ([\-]{0,1}\d+\.\d+[e]{0,1}[-+]\d+)  step = ([\-]{0,1}\d+\.\d+[e]{0,1}[-+]\d+)  dx = ([\-]{0,1}\d+\.\d+[e]{0,1}[-+]\d+)[^\d]*")

PimpOmPattern = re.compile(r" \tomega=(\d+.{0,1}\d*)")
PimpDofPattern = re.compile(r"\t--- Nf: \d+\tdof: (\d+)\t---")
PimpNfPattern = re.compile(r"\t--- Nf: (\d)+\tdof: \d+\t---")

PimpRefPattern = re.compile(
    r"\|\|u\[nf\]\|\|/\|\|u\[1\]\|\| = (\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*)")

# timer
PimpSolveTimePattern = re.compile(
    r"Pimpact:: Solving Time\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \(\d+\)")
PimpSolveTime = re.compile(
    r"Pimpact:: Solving Time\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)")
NOXCompFTime = re.compile(
    r"NOX: compute F\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)")
NOXSolveDXTime = re.compile(
    r"NOX: solve dx\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)")
NOXUpdateXTime = re.compile(
    r"NOX: update X\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)")
BelosTotTime = re.compile(
    r"Compound\( MHDtConvectionDiffusion\, MH_Grad\, MH_Div \): BlockGmresSolMgr total solve time\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)")
FTime = re.compile(
    r"MHDtConvectionDiffusion: BlockGmresSolMgr total solve time\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)")
DivGradTime = re.compile(
    r"DivGrad: BlockGmresSolMgr total solve time\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)")
FZTime = re.compile(
    r"ConvectionDiffusionVOp: BlockGmresSolMgr total solve time\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d* \(\d+\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)")


def extract(datafile, pattern, outfile='', isfloat=True, isarray=True):
    m = pattern.groups
    try:
            data = open(datafile).read()
    except:
            print('Error: couldnot open file:', datafile)
            raise
            #return ['*']
    dat = []
    for line in data.split("\n"):
            match = pattern.match(line)
            if match:
                    dat.append(match.groups())
    #print( dat )
    n = len(dat)
    #print( n )
    out = numpy.empty([n, m])
    for i in range(n):
            for j in range(m):
                    if isfloat:
                            out[i][j] = float(dat[i][j])
                    else:
                            out[i][j] = int(dat[i][j])
    if len(outfile) != 0:
            numpy.save(outfile, out)
    #print 'n:',n,'m:',m
    #if( n==1 ):
            #out = out[0]
            #if(m==1):
                    #out = out[0]
    #print 'out:',out
    return out


# what we're gonna do, is search through it line-by-line
# and parse out the numbers, using regular expressions
# what this basically does is, look for any number of characters
# that aren't digits or '-' [^-\d]  ^ means NOT
# then look for 0 or 1 dashes ('-') followed by one or more decimals
# and a dot and decimals again: [\-]{0,1}\d+\.\d+
# and then the same as first..
def extracttime(path):
    pattern = re.compile(r'elapsed time \[sec\]  (\d\.\d+E[-,+]\d+)')
    time = extract(path+'/test_wallclocktime_restart000.txt',
                   pattern, isarray=False)
    return time


def extractmint(path, runs, start_r=0):
    t = 1.e999
    fails = 0
    for r in range(start_r, runs):
            tnew = extracttime(path+'/run'+str(r))
            t = min(t, tnew)
            if tnew == inf:
                    fails += 1
                    print '\t', float(r)/(runs-1)*100., '% failed'
            else:
                    print '\t', float(r)/(runs-1)*100., '% done'
    print fails, 'fails of', runs
    print
    return t
