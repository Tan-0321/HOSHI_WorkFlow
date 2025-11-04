import sys

import numpy as np

year = 365*24*3600.

class Summary:
    def __init__(self,fname):
        self.fname = fname
        return
        
    def get_lmax(self) :
        return self.lmax

    def get_nstg(self,l) :
        return self.nstg[l]

    def get_jcmax(self,l) :
        return self.jcmax[l]

    def get_time(self,l) :
        return self.time[l]

    def get_rtime(self,l) :
        return self.rtime[l]

    def get_mtot(self,l) :
        return self.mtot[l]

    def get_rsurf(self,l) :
        return self.rsurf[l]

    def get_tempc(self,l) :
        return self.tempc[l]

    def get_densc(self,l) :
        return self.densc[l]

    def get_entrc(self,l) :
        return self.entrc[l]

    def get_lnuc(self,l) :
        return self.lnuc[l]

    def get_lneu(self,l) :
        return self.lneu[l]



    def read_file(self):
        # define necessary data
        self.lmax = 0
        self.nstg = []
        self.jcmax= []
        self.time = []
        self.rtime= []
        self.mtot = []
        self.rsurf= []

        self.tempc = []
        self.densc = []
        self.entrc = []
        self.lnuc  = []
        self.lneu  = []

        # store all summary data
        with open(self.fname,'r') as f:
            line_all = f.readlines()

        # get rid of description
        line_data = []
        for l in range(0,len(line_all)):
            line = line_all[l].split()
            if line[0]!='#' :
                line_data.append(line)

        # reduct unconnected data
        # at the same time, rtime is integrated
        line_red = []
        lmax     = len(line_data)
        rtime    = 0.
        # copy the last line
        ldata    = lmax-1 - 0
        line     = line_data[ldata]
        rtime   += float(line[5])
        line.append(rtime)
        line_red.append(line)
        nstgb    = line[0]
        # copy the 2nd last to first line
        for l in range(1,lmax):
            ldata    = lmax-1 - l
            line     = line_data[ldata]
            nstg     = line[0]
            if int(nstg)==int(nstgb)-1 :
                rtime+= float(line[5])
                line.append(rtime)
                line_red.append(line)
                nstgb = nstg
        # reverse
        line_red.reverse()

        # take out necessary data
        self.lmax = len(line_red)
        for l in range(0,self.lmax):
            line = line_red[l]

            nstg = int  (line[ 1-1])
            jcmax= int  (line[ 2-1])
            time = float(line[ 5-1])
            rtime= float(line[  -1])
            mtot = float(line[ 7-1])
            rsurf= float(line[14-1])

            tempc = float(line[13-1])
            densc = float(line[12-1])
            entrc = 0.0
            lnuc  = float(line[28-1])
            lneu  = float(line[29-1])
            
            self.nstg  .append(nstg )
            self.jcmax .append(jcmax)
            self.time  .append(time /year)
            self.rtime .append(rtime/year)
            self.mtot  .append(mtot )
            self.rsurf .append(rsurf)

            self.tempc .append(tempc )
            self.densc .append(densc )
            self.entrc .append(entrc )
            self.lnuc  .append(lnuc  )
            self.lneu  .append(lneu  )

        print('read summary data: %s' % self.fname)
        return

    def output(self):
        print('summary data: %s' % self.fname)
        for l in range(0,self.lmax):
            nstg = self.get_nstg(l)
            time = self.get_time(l)
            rtime= self.get_rtime(l)

            print (l \
                   ,nstg \
                   ,time,rtime \
            )
        return
