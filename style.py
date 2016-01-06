from pylab import *
from itertools import cycle

#presentation
fig_width_pt = 0.8*340.6956 # Get this from LaTeX using \showthe\columnwidth
fs=12

#report
#fig_width_pt = 0.8*455.24408 # Get this from LaTeX using \showthe\columnwidth
#fig_width_pt = 0.49*455.24408 # Get this from LaTeX using \showthe\columnwidth

# ETHbeamer
#fig_width_pt = 0.6*307.28987
#fs=10

inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (sqrt(5)-1.0)/2.0        # Aesthetic ratio
#golden_mean = (sqrt(5)-1.0)        # Aesthetic ratio
#golden_mean = 2./3.        # Aesthetic ratio
#golden_mean = 1.        # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
params = {
    'backend': 'pdf',
    #'font.family':'serif',
    #'font.serif':'Computer Modern Roman',
    'font.family':'sans-serif',
    'font.sans-serif':'Helvetica',
    #'font.sans-serif':'Computer Modern Sans serif',
    'text.fontsize': fs,
    'legend.fontsize': fs,
    'axes.labelsize': fs,
    'xtick.labelsize': fs,
    'ytick.labelsize': fs,
    'text.usetex': True,
    'figure.figsize': fig_size,
    #'figure.subplot.bottom' : 0.16,
    #'figure.subplot.left' : 0.19
}
rcParams.update(params)

c = ['b','g','r','c','m','y']
ci = cycle(c)
l = [ '-','--' , '-.' , ':'  ]
#l = [ '--' , '-.' , ':'  ]
li = cycle(l)
m = ['.','o','v','^','<','>','1','2','3','4','8','s','p','*','h','H','+','x','D','d','|','_','TICKLEFT','TICKRIGHT','TICKDOWN','CARETLEFT','CARETRIGHT','CARETUP','CARETDOWN']
m = ['o','v','*','x','d','^','2','>','4','p','s','p','8','h','H','+','p','D','3','|','_','TICKLEFT','TICKRIGHT','TICKDOWN','CARETLEFT','CARETRIGHT','CARETUP','CARETDOWN','.']
mi = cycle(m)

