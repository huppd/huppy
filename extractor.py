"""@package extractor
uses regular expression to extract results from pimpact resuls and stores them
in numpy array files
TODO: include string variables for recurrin patterns
"""
import re
import numpy
INF = 1e9999

# helper string
FLOAT_STR = r"[\-]{0,1}\d+.{0,1}\d+e{0,1}[-+]{0,1}\d*"
INT_STR = r"\d+"

# lin solver
BelosIterPattern = re.compile(
    r"Iter[ ]+(" + INT_STR + r"), \[ +" + INT_STR + r"\] :    (" + FLOAT_STR +
    r")")
BelosMaxItPattern = re.compile(
    r"\s+[OK,Failed]+[.]+Number of Iterations = (" + INT_STR + r") [<=]+ " +
    INT_STR)
BelosArTolPattern = re.compile(
    r"\s+residual \[ " + INT_STR + r" \] = (" + FLOAT_STR + r") [<>] ")

# nonlin solver
NOXIterPattern = re.compile(r"-- Nonlinear Solver Step (" + INT_STR + r") -- ")
NOXResPattern = re.compile(
    r"\|\|F\|\| = (" + FLOAT_STR + r")  step = " + r"(" + FLOAT_STR +
    r")  dx = ([\-]{0,1}\d+\.\d+[e]{0,1}[-+]\d+)[^\d]*")

PimpOmPattern = re.compile(r" \tomega=(\d+.{0,1}\d*)")
PimpDofPattern = re.compile(r"\t--- Nf: \d+\tdof: (\d+)\t---")
PimpNfPattern = re.compile(r"\t--- Nf: (\d)+\tdof: \d+\t---")

PimpRefPattern = re.compile(
    r"\|\|u\[nf\]\|\|/\|\|u\[1\]\|\| = (\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*)")

# timer
PimpSolveTimePattern = re.compile(
    r"Pimpact:: Solving Time\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \(\d+\)")
PimpSolveTime = re.compile(
    r"Pimpact:: Solving Time\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) " +
    r"\((\d+)\)\s+(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+" +
    r"(\d+.{0,1}\d*e{0,1}[-,+]{0,1}\d*) \((\d+)\)\s+(\d+.{0,1}\d*" +
    r"e{0,1}[-,+]{0,1}\d*) \((\d+)\)")
NOXCompFTime = re.compile(
    r"NOX: compute F\s+(" + FLOAT_STR + r") \((" + INT_STR + r")\)\s+(" +
    FLOAT_STR + r") \((" + INT_STR + r")\)\s+(" + FLOAT_STR + r") \((" +
    INT_STR + r")\)\s+(" + FLOAT_STR + r") \((" + INT_STR + r")\)")
NOXSolveDXTime = re.compile(
    r"NOX: solve dx\s+(" + FLOAT_STR + r") \((" + INT_STR + r")\)\s+(" +
    FLOAT_STR + r") \((" + INT_STR + r")\)\s+(" + FLOAT_STR + r") \((" +
    INT_STR + r")\)\s+(" + FLOAT_STR + r") \((" + INT_STR + r")\)")
NOXUpdateXTime = re.compile(
    r"NOX: update X\s+(" + FLOAT_STR + r") \((" + INT_STR + r")\)\s+(" +
    FLOAT_STR + r" ) \((" + FLOAT_STR + r") \((" + INT_STR + r")\)\s+(" +
    FLOAT_STR + r") \((" + INT_STR + r")\)")
BelosTotTime = re.compile(
    r"Compound\( MHDtConvectionDiffusion\, MH_Grad\, MH_Div \): " +
    r"BlockGmresSolMgr total solve time\s+(" + FLOAT_STR + r") \((" + INT_STR +
    r")\)\s+(" + FLOAT_STR + r") \((" + INT_STR + r")\)\s+(" + FLOAT_STR +
    r") \((" + INT_STR + r")\)\s+(" + FLOAT_STR + r") \((" + INT_STR + r")\)")
FTime = re.compile(
    r"MHDtConvectionDiffusion: BlockGmresSolMgr total solve time\s+" +
    FLOAT_STR + r" \(" + INT_STR + r"\)\s+" + FLOAT_STR + r" \(" + INT_STR +
    r"\)\s+" + FLOAT_STR + r" \(" + INT_STR + r"\)\s+(" + FLOAT_STR + r") \(("
    + INT_STR + r")\)")
DivGradTime = re.compile(
    r"DivGrad: BlockGmresSolMgr total solve time\s+" + FLOAT_STR + r" \(" +
    INT_STR + r"\)\s+" + FLOAT_STR + r" \(" + INT_STR + r"\)\s+" + FLOAT_STR +
    r" \(" + INT_STR + r"\)\s+(" + FLOAT_STR + r") \((" + INT_STR + r")\)")
FZTime = re.compile(
    r"ConvectionDiffusionVOp: BlockGmresSolMgr total solve time\s+" + FLOAT_STR
    + r" \(" + INT_STR + r"\)\s+" + FLOAT_STR + r" \(" + INT_STR + r"\)\s+" +
    FLOAT_STR + r" \(" + INT_STR + r"\)\s+(" + FLOAT_STR + r") \((" + INT_STR +
    r")\)")


def extract(datafile, pattern, isfloat=True, isarray=True, outfile=''):
    """ extractor function """
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
    """ extracts time """
    pattern = re.compile(r'elapsed time \[sec\]  (\d\.\d+E[-,+]\d+)')
    time = extract(path+'/test_wallclocktime_restart000.txt',
                   pattern, isarray=False)
    return time


def extractmint(path, runs):
    """ extract minimum from multiple runs """
    time = INF
    fails = 0
    for run in runs:
        tnew = extracttime(path+'/run'+str(run))
        time = min(time, tnew)
        if tnew == INF:
            fails += 1
            # print '\t', float(run)/(len(runs)-1)*100., '% failed'
        # else:
            # print '\t', float(run)/(len(runs)-1)*100., '% done'
    print(fails, 'fails of', len(runs))
    print()
    return time
