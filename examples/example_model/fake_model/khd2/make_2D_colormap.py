import math
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib import colors as mcolors


def colormap(ipanel,fig,ax,clabel,cmin,cmax,cstep,xgrid,ygrid,cgrid,colorref) :

    # color definition
    #icolor     = 6
    #color_list = []
    #for i in range(0,icolor):
        #color = cm.PuOr(float(i)/float(icolor))
        #color_list.append(color)

    # set c coordinate
    qcolor = np.arange(cmin,cmax+  cstep,  cstep)
    qticks = np.arange(cmin,cmax+2*cstep,2*cstep)

    cont = ax.contourf(xgrid,ygrid,cgrid,qcolor,cmap=colorref,alpha=1.0)

    # contour definition
    if ipanel==2:
        cbar = fig.colorbar(cont,ticks=qticks)
        cbar.set_label(clabel)

    return

def contourmap(ipanel,fig,ax,xgrid,ygrid,cgrid) :
    
    # contour definition
    mask    = cgrid > 0.5
    ax.contourf(xgrid,ygrid,cgrid,2,colors=['w','w','orange'],alpha=0.1)
    ax.contour (xgrid,ygrid,mask,colors='orange',linewidths=1.0)
    return

def set_xy_ticks(ipanel,fig,ax,xlabel,xmin,xmax,ylabel,ymin,ymax):

    # set x coordinate
    ax.set_xlabel(xlabel)
    ax.set_xlim(xmin,xmax)
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')

    # set y coordinate

    if ipanel==1:
        ax.set_ylabel(ylabel)
    elif ipanel==2:
        ax.yaxis.set_ticklabels([])
    ax.set_ylim(ymin,ymax)

    ax.tick_params(axis='both',which='minor',direction='in',length=3,width=0.5,labelsize=8)
    ax.tick_params(axis='both',which='major',direction='in',length=5,width=0.5,labelsize=8)
    ax.minorticks_on()

    return

