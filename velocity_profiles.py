""" velocity profiles """
from pylab import sin, cos, sinh, cosh, sqrt


def parabola(x):
    return 4*x*(x[-1]-x)/x[-1]**2


def pulseC(x, re=1., om=1., px=1.):
    h = x[-1]/2
    mu = sqrt(om*re/2.)*h
    nu = sqrt(om*re/2.)*(x-h)
    d = px/(om*(cos(mu)**2*cosh(mu)**2 + sin(mu)**2*sinh(mu)**2))
    return(d*(cos(nu)*cosh(nu)*sin(mu)*sinh(mu) -
              sin(nu)*sinh(nu)*cos(mu)*cosh(mu)))


def pulseS(x, re=1., om=1., px=1.):
    h = x[-1]/2
    mu = sqrt(om*re/2.)*h
    nu = sqrt(om*re/2.)*(x-h)
    d = px/(om*(cos(mu)**2*cosh(mu)**2 + sin(mu)**2*sinh(mu)**2))
    return(-d*(+cos(nu)*cosh(nu)*cos(mu)*cosh(mu) +
               sin(nu)*sinh(nu)*sin(mu)*sinh(mu))+px/om)
