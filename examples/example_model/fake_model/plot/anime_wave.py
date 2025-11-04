import math
import sys

import matplotlib.animation as anm
import matplotlib.pyplot as plt
import numpy as np

# file settings
nstg_st =  571
nstg_ed =  571
dnstg   =  10
jevol   = 631
jin = 1
jex = 1024
unit_rsol = 7e10
nstg_max  = 100000

# figure settings
figname = "anime_wave.pdf"
fig, ax = plt.subplots(figsize=(15,8),nrows=2,ncols=4)
plt.subplots_adjust(wspace=0.4, hspace=0.2)
ax[1,0].set_yscale('log')
ax[0,3].set_yscale('log')
ax[1,3].set_yscale('log')
ax[0,0].set_xlabel('time')
ax[0,0].set_ylabel('$\Omega_{\mathrm{surf}}$')
ax[0,1].set_xlabel('mass')
ax[0,2].set_xlabel('mass')
ax[0,3].set_xlabel('mass')
ax[0,1].set_ylabel('Bpol')
ax[0,2].set_ylabel('Btor')
ax[0,3].set_ylabel('omega')
ax[1,0].set_xlabel('radius')
ax[1,1].set_xlabel('radius')
ax[1,2].set_xlabel('radius')
ax[1,3].set_xlabel('radius')
ax[1,0].set_ylabel('1/time')
ax[1,1].set_ylabel('Bpol')
ax[1,2].set_ylabel('Btor')
ax[1,3].set_ylabel('omega')

# animation settings
anmname = "anime_wave.gif"
fig_anm, ax_anm = plt.subplots(figsize=(15,8),nrows=2,ncols=4)
plt.subplots_adjust(wspace=0.4, hspace=0.2)
ax_anm[1,0].set_yscale('log')
ax_anm[0,3].set_yscale('log')
ax_anm[1,3].set_yscale('log')
ax_anm[0,0].set_xlabel('time')
ax_anm[0,0].set_ylabel('Omega')
ax_anm[0,1].set_xlabel('mass')
ax_anm[0,2].set_xlabel('mass')
ax_anm[0,3].set_xlabel('mass')
ax_anm[0,1].set_ylabel('Bpol')
ax_anm[0,2].set_ylabel('Btor')
ax_anm[0,3].set_ylabel('omega')
ax_anm[1,0].set_xlabel('radius')
ax_anm[1,1].set_xlabel('radius')
ax_anm[1,2].set_xlabel('radius')
ax_anm[1,3].set_xlabel('radius')
ax_anm[1,0].set_ylabel('1/time')
ax_anm[1,1].set_ylabel('Bpol')
ax_anm[1,2].set_ylabel('Btor')
ax_anm[1,3].set_ylabel('omega')

class model:
    def __init__(self,nstg):
        snstg_zero = str(nstg).zfill(5)
        self.fname = "../writestr/str"+snstg_zero+".txt"

    def output(self):
        print(self.fname)

    def get_data(self):
        f = open(self.fname, "r")
        data = f.readline()
        line = data.split()
        dtime= float(line[8])
        data = f.readline()
        data = f.readline()
        data = f.readlines()
        f.close()

        jmax = len(data)
        self.jmax = jmax
        mesh = []
        mass = []
        rad  = []
        omg  = []
        omgm = []
        Brad = []
        Bphi = []
        Brad_im = []
        Bphi_im = []
        Brad_abs= []
        Bphi_abs= []
        eta  = []
        alp  = []
        alpn = []
        omgB = []
        omgBn= []
        for j in range(0,jmax):
            line = data[j].split()

            j1 = j+1
            if j1==jevol :
                Ar = float(line[43-1])
                Ai = float(line[49-1])
                Aa = math.sqrt(Ar*Ar+Ai*Ai)
                self.Brad_evol    =Ar
                self.Brad_evol_im =Ai
                self.Brad_evol_abs=Aa
                
                Ar = float(line[44-1])
                Ai = float(line[50-1])
                Aa = math.sqrt(Ar*Ar+Ai*Ai)
                self.Bphi_evol    =Ar
                self.Bphi_evol_im =Ai
                self.Bphi_evol_abs=Aa

            if j1<=jin or j1>=jex :
                continue

            mesh.append( int  (line[ 1-1]))
            mass.append( float(line[ 7-1]))
            rad .append( float(line[ 9-1])/6.96e10)
            omg .append( float(line[32-1])/86400.)
            omgm.append(-float(line[32-1])/86400.)

            Ar = float(line[43-1])
            Ai = float(line[49-1])
            Aa = math.sqrt(Ar*Ar+Ai*Ai)
            Brad.append(Ar)
            Brad_im.append(Ai)
            Brad_abs.append(Aa)

            Ar = float(line[44-1])
            Ai = float(line[50-1])
            Aa = math.sqrt(Ar*Ar+Ai*Ai)
            Bphi.append(Ar)
            Bphi_im.append(Ai)
            Bphi_abs.append(Aa)

            eta0 = float(line[52-1])
            alp0 = float(line[53-1])
            lcv0 = float(line[46-1])

            eta .append( eta0/unit_rsol/unit_rsol )
            alp .append( alp0/unit_rsol )
            alpn.append(-alp0/unit_rsol )

            omgB .append( (float(line[51-1])))
            omgBn.append(-(float(line[51-1])))
        self.jmax = jmax
        self.mesh = mesh
        self.mass = mass
        self.rad  = rad
        self.omg  = omg
        self.omgm = omgm
        self.Brad = Brad
        self.Bphi = Bphi
        self.Brad_im = Brad_im
        self.Bphi_im = Bphi_im
        self.Brad_abs= Brad_abs
        self.Bphi_abs= Bphi_abs
        self.eta  = eta
        self.alp  = alp
        self.alpn = alpn
        self.omgB = omgB
        self.omgBn= omgBn

    def print(self,ims,time):
       
        # time evolution
        x_now = time
        y_now = self.omg[-1]
        ax[0,0].plot(x_time,y_time,c="r")
        ax[0,0].scatter(x_now,y_now,c="r")
        im = ax_anm[0,0].plot(x_time,y_time,c="r")
        im+=[ax_anm[0,0].scatter(x_now,y_now,c="r")]

        # plot circle
        cir1_x=[]
        cir1_y=[]
        cir2_x=[]
        cir2_y=[]
        rad1 = self.Brad_evol_abs
        rad2 = self.Bphi_evol_abs
        for i in range(0,101):
            the= 2.*math.pi*float(i)*0.01

            x1 = rad1 * math.cos( the )
            y1 = rad1 * math.sin( the )
            cir1_x.append(x1)
            cir1_y.append(y1)

            x2 = rad2 * math.cos( the )
            y2 = rad2 * math.sin( the )
            cir2_x.append(x2)
            cir2_y.append(y2)

        # pdf
        #ax[0,0].scatter(self.Brad_evol,self.Brad_evol_im,c="r")
        #ax[0,0].scatter(self.Bphi_evol,self.Bphi_evol_im,c="b")
        #ax[0,0].plot(cir1_x ,cir1_y ,":r")
        #ax[0,0].plot(cir2_x ,cir2_y ,":b")

        ax[1,0].plot(self.rad ,self.eta ,"-r")
        ax[1,0].plot(self.rad ,self.alp ,"-g")
        ax[1,0].plot(self.rad ,self.alpn,"--g")
        ax[1,0].plot(self.rad ,self.omg ,"-c")
        ax[1,0].plot(self.rad ,self.omgm,"--c")
        ax[1,0].plot(self.rad ,self.omgB ,"-b")
        ax[1,0].plot(self.rad ,self.omgBn,"--b")

        ax[0,1].plot(self.mass,self.Brad   ,"-r" )
        ax[0,2].plot(self.mass,self.Bphi   ,"-b" )
        ax[1,1].plot(self.rad ,self.Brad   ,"-r" )
        ax[1,2].plot(self.rad ,self.Bphi   ,"-b" )

        ax[0,1].plot(self.mass,self.Brad_im,"--r")
        ax[0,2].plot(self.mass,self.Bphi_im,"--b")
        ax[1,1].plot(self.rad ,self.Brad_im,"--r")
        ax[1,2].plot(self.rad ,self.Bphi_im,"--b")

        ax[0,3].plot(self.mass,self.omg ,"-g")
        ax[0,3].plot(self.mass,self.omgm,"--g")
        ax[1,3].plot(self.rad ,self.omg ,"-g")
        ax[1,3].plot(self.rad ,self.omgm,"--g")

        # animation
        #im  =[ax_anm[0,0].scatter(self.Brad_evol,self.Brad_evol_im,c="r")]
        #im +=[ax_anm[0,0].scatter(self.Bphi_evol,self.Bphi_evol_im,c="b")]
        #im += ax_anm[0,0].plot(cir1_x ,cir1_y ,":r")
        #im += ax_anm[0,0].plot(cir2_x ,cir2_y ,":b")

        im += ax_anm[1,0].plot(self.rad ,self.eta ,"-r")
        im += ax_anm[1,0].plot(self.rad ,self.alp ,"-g")
        im += ax_anm[1,0].plot(self.rad ,self.alpn,"--g")
        im += ax_anm[1,0].plot(self.rad ,self.omg ,"-c")
        im += ax_anm[1,0].plot(self.rad ,self.omgm,"--c")
        im += ax_anm[1,0].plot(self.rad ,self.omgB ,"-b")
        im += ax_anm[1,0].plot(self.rad ,self.omgBn,"--b")

        im += ax_anm[0,1].plot(self.mass,self.Brad   ,"-r" )
        im += ax_anm[0,2].plot(self.mass,self.Bphi   ,"-b" )
        im += ax_anm[1,1].plot(self.rad ,self.Brad   ,"-r" )
        im += ax_anm[1,2].plot(self.rad ,self.Bphi   ,"-b" )

        im += ax_anm[0,1].plot(self.mass,self.Brad_im,"--r")
        im += ax_anm[0,2].plot(self.mass,self.Bphi_im,"--b")
        im += ax_anm[1,1].plot(self.rad ,self.Brad_im,"--r")
        im += ax_anm[1,2].plot(self.rad ,self.Bphi_im,"--b")

        im += ax_anm[0,3].plot(self.mass,self.omg ,"-g")
        im += ax_anm[0,3].plot(self.mass,self.omgm,"--g")
        im += ax_anm[1,3].plot(self.rad ,self.omg ,"-g")
        im += ax_anm[1,3].plot(self.rad ,self.omgm,"--g")
        ims.append(im)

def get_time(fname):
    f = open(fname,"r")
    lines = f.readlines()

    dt_array = np.zeros(nstg_max-1)
    nstg  = nstg_max
    dtime = 0.
    for l in range(len(lines)-1,-1,-1):
        line = lines[l].split()
        if line[0]=="#" :
            continue
        if int(line[0])<=nstg-1 :
            nstg = int(line[0])
            dtime= float(line[6-1])
            dt_array[nstg-1]=dtime
            #print(l,nstg,dtime)
    f.close()

    t_array = np.zeros(nstg_max-1)
    for l in range(1,len(dt_array)):
        t_array[l]=t_array[l-1] + dt_array[l]
        #print(l,dt_array[l],time)

    return t_array

N_model  = int( (nstg_ed-nstg_st)/dnstg )+1

# get a time array
time = get_time("../summary/summary.txt")
#for l in range(0,len(time)):
#    print(l,time[l])
#sys.exit()

# time sequence
timeb    = 0.
x_time   = np.zeros(N_model)
y_time   = np.zeros(N_model)
for n in range(0,N_model):
    nstg   = nstg_st + n*dnstg
    model1 = model(nstg)
    model1.get_data()
    x_time[n] = time[nstg-1]
    y_time[n] = model1.omg[len(model1.omg)-1]

ims   = []
for n in range(0,N_model):
    nstg   = nstg_st + n*dnstg
    model1 = model(nstg)
    model1.output()
    model1.get_data()
    model1.print(ims,time[nstg-1])

# output data
print("anime_wave.dat output")
f = open("anime_wave.dat","w")
for n in range(0,N_model):
    print(n,x_time[n],y_time[n],file=f)
f.close()
#print("only anime_wave.dat is made")
#sys.exit()

# print out
fig.savefig(figname,transparent=True)
ani = anm.ArtistAnimation(fig_anm,ims,interval=50)
ani.save(anmname,writer="imagemagick")
