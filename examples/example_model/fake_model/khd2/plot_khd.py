import math
import sys

import make_2D_colormap
###
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import read_accretion as ra
import read_summary as rs
import read_writestr as rw
from matplotlib import cm
from matplotlib import colors as mcolors
from matplotlib import pyplot

###

# constants
year = 365*24*3600.
#--
m_stream = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10., 30., 100.]
#--

def plot_khd(fplot,fig,fig_coord
             ,ipanel,T_switch \
             ,ixplot,xlabel,xmin,xmax \
             ,iyplot,ylabel,ymin,ymax \
             ,icplot,clabel,cmin,cmax,cstep \
             ):

    # read summary data
    summ = rs.Summary('../summary/summary.txt')
    summ.read_file()

    # read accretion data
    accr = ra.Accretion('../summary/accretion.txt')
    accr.read_file()

    lmax = min(summ.get_lmax(),accr.get_lmax())

    #--
    # find accretion end
    #--
    l_bound_1 = lmax
    l_bound_2 = lmax
    for l in range(0,lmax):
        nstg = summ.get_nstg (l)
        jcmax= summ.get_jcmax(l)
        if nstg%10==0 :
            if jcmax == 1:
                l_bound_2 = l
                break
            l_bound_1 = l
            
    if ipanel==1 :
        l=l_bound_1
        nstg = summ.get_nstg (l)
        jcmax= summ.get_jcmax(l)
        rtime= summ.get_rtime(l)
        mtot = summ.get_mtot (l)
        rsurf= summ.get_rsurf(l)
        tacc = accr.get_tacc (l)
        if ixplot==1 :
            xvalue = math.log10(mtot)
        elif ixplot==2 :
            xvalue = math.log10(tacc)
        elif ixplot==3 :
            xvalue = math.log10(rtime)
        xmax = xvalue

    elif ipanel==2 :
        l=l_bound_2
        nstg = summ.get_nstg (l)
        jcmax= summ.get_jcmax(l)
        rtime= summ.get_rtime(l)
        mtot = summ.get_mtot (l)
        rsurf= summ.get_rsurf(l)
        tacc = accr.get_tacc (l)
        if ixplot==1 :
            xvalue = math.log10(mtot)
        elif ixplot==2 :
            xvalue = math.log10(tacc)
        elif ixplot==3 :
            xvalue = math.log10(rtime)
        xmin = xvalue


    for l in range(0,lmax):
        nstg = summ.get_nstg (l)
        jcmax= summ.get_jcmax(l)
        rtime= summ.get_rtime(l)
        mtot = summ.get_mtot (l)
        rsurf= summ.get_rsurf(l)
        tacc = accr.get_tacc (l)
        if ixplot==1 :
            xvalue = math.log10(mtot)
        elif ixplot==2 :
            xvalue = math.log10(tacc)
        elif ixplot==3 :
            xvalue = math.log10(rtime)

        menv = accr.get_menv(l)
        if menv<=0. :
            x_acc_end = xvalue
            break

    # curve of the surface
    x_surf = []
    y_surf = []
    # count available data
    lplt = []
    for l in range(0,lmax):
        nstg = summ.get_nstg (l)
        rtime= summ.get_rtime(l)
        mtot = summ.get_mtot (l)
        rsurf= summ.get_rsurf(l)
        tacc = accr.get_tacc (l)

        if ixplot==1 :
            xvalue = math.log10(mtot)
        elif ixplot==2 :
            xvalue = math.log10(tacc)
        elif ixplot==3 :
            xvalue = math.log10(rtime)

        if nstg%10==0 and (xmin-xvalue)*(xmax-xvalue)<=0 :
            lplt.append(l)
        x_surf.append(xvalue)
        y_surf.append(math.log10(rsurf))

    x_stream = []
    y_stream = []
    k_stream_max = len(m_stream)
    for k_stream in range(0,k_stream_max):
        y_stream.append([])
    #--
    for ldum in range(0,len(lplt)):
        l     = lplt[ldum]
        nstg  = summ.get_nstg (l)
        rtime = summ.get_rtime(l)
        mtot  = summ.get_mtot (l)
        tacc  = accr.get_tacc (l)
    
        if ixplot==1 :
            xvalue = math.log10(mtot)
        elif ixplot==2 :
            xvalue = math.log10(tacc)
        elif ixplot==3 :
            xvalue = math.log10(rtime)

        strc = rw.Structure('../writestr/',nstg)
        strc.read_file()
    
        # set x,y,color data
        ndiv = strc.get_ndiv()
        xplt = np.full(ndiv,xvalue)
        yplt = np.empty(ndiv)
        cplt = np.empty(ndiv)
        iplt = np.empty(ndiv)
        for j in range(1,ndiv+1):
            icv  = strc.get_icv(j)
            mass = strc.get_mass(j)
            rad  = strc.get_rad(j)
#        color= math.log10(strc.get_entropy(j)-18.)
            color= strc.get_epn(j)
            yplt[j-1] = np.log10(rad)
            cplt[j-1] = color
            iplt[j-1] = icv
        
        #--
        # stream
        #--
        mtot  = strc.get_mass(ndiv)
        rsurf = strc.get_rad(ndiv)
        lgM   = math.log10(mtot)
        lgR   = math.log10(rsurf)
        # initialization
        x_stream.append( xvalue )
        for k_stream in range(0,k_stream_max):
            y_stream[k_stream].append( lgR )
        # stream search    
        k_stream = 0
        m_stream_search = m_stream[k_stream]
        for j in range(1,ndiv+1):
            mass = strc.get_mass(j)
            if mass >= m_stream_search :
                mass_r = mass*1.0001
                mass_l = strc.get_mass(j-1)
                rad3_r = math.pow(strc.get_rad(j  ),3)
                rad3_l = math.pow(strc.get_rad(j-1),3)
                rad3 = rad3_r*(m_stream_search-mass_l         )/(mass_r-mass_l) \
                    + rad3_l*(mass_r         -m_stream_search)/(mass_r-mass_l)
                y_stream[k_stream][-1] = math.log10(rad3)/3.
                k_stream += 1
                if k_stream >= k_stream_max:
                    break
                m_stream_search = m_stream[k_stream]

        # make grid data
        if ldum==0 :
            xgrid = xplt
            ygrid = yplt
            cgrid = cplt
            igrid = iplt
        else :
            xgrid = np.vstack((xgrid,xplt))
            ygrid = np.vstack((ygrid,yplt))
            cgrid = np.vstack((cgrid,cplt))
            igrid = np.vstack((igrid,iplt))

    ax   = fig.add_axes(fig_coord)
    make_2D_colormap.set_xy_ticks(ipanel,fig,ax\
                                  ,xlabel,xmin,xmax\
                                  ,ylabel,ymin,ymax)
    make_2D_colormap.colormap(ipanel,fig,ax\
                              ,clabel,cmin,cmax,cstep\
                              ,xgrid,ygrid,cgrid,'coolwarm')
    make_2D_colormap.contourmap(ipanel,fig,ax\
                                ,xgrid,ygrid,igrid)
    plt.plot(x_surf,y_surf,linewidth=1,color="black")
    for k_stream in range(0,len(m_stream)):
        plt.plot(x_stream,y_stream[k_stream],"--",linewidth=0.5,color="black")
    plt.vlines(x_acc_end,ymin,ymax,linestyle="dashed",linewidth=0.5,color="red")

    return


