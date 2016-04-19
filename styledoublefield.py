from pylab import *
#presentation
#fig_width_pt = 0.8*340.6956 # Get this from LaTeX using \showthe\columnwidth
#fs=12

#report
fig_width_pt = 0.8*455.24408 # Get this from LaTeX using \showthe\columnwidth
fig_width_pt = 0.49*455.24408 # Get this from LaTeX using \showthe\columnwidth
fs=7

inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (sqrt(5)-1.0)/2.0        # Aesthetic ratio
golden_mean = (sqrt(5)-1.0)        # Aesthetic ratio
#golden_mean = 2./3.        # Aesthetic ratio
golden_mean = 1.        # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
params = {'backend': 'pdf',
          'axes.labelsize': fs,
          #'font.family':'serif',
          #'font.serif':'Computer Modern Roman',
          'font.family':'sans-serif',
          'font.sans-serif':'Helvetica',
          #'font.sans-serif':'Computer Modern Sans serif',
		  'text.fontsize': fs,
		  'axes.linewidth' : 2.0,
		  'lines.linewidth' : 4.0,
		  'legend.fontsize': fs,
		  'axes.titlesize': fs,
		  'axes.labelsize': fs,
		  'xtick.labelsize': fs*8/10,
		  'ytick.labelsize': fs*8/10,
          'text.usetex': True,
          'figure.figsize': fig_size,
          'figure.subplot.bottom' : 0.16,
          'figure.subplot.left' : 0.19
}
rcParams.update(params)

c = ['b','g','r','c','m','y',]
l = [ '--' , '-.' , ':' ,'-' ]
