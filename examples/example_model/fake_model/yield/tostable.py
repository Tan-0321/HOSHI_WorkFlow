import numpy as np

tau_lim = 0. # minimum lifetime for stable isotopes

### import lifetime ###
file_st = open('/data/home/ktakahashi/HOSHI_210703/data/solar/stable.txt','r')
data_st = file_st.readlines()

# number of isotopes
nctl_st = len(data_st) - 1
#print (nctl_st)
#print (data_st)

nuc_A_st=[]
nuc_Z_st=[]
nuc_N_st=[]
name_st =[]
tau_st  =[]
for k in range(0,nctl_st):
    line = data_st[k].rstrip('\n').split()
    nuc_A_st.append( int(line[0]) )
    nuc_Z_st.append( int(line[1]) )
    nuc_N_st.append( int(line[0])-int(line[1]) )
    name_st.append( line[2] )
    tau_st.append( float(line[3].replace('d','e')) )
#    print (k, nuc_A_st[k], nuc_Z_st[k], nuc_N_st[k], tau_st[k])

file_st.close()
########################

def get_nctl_st():
    return nctl_st

def get_nuc_A_st():
    return nuc_A_st

def get_nuc_Z_st():
    return nuc_Z_st

def get_name_st():
    return name_st

def tostable(nctl, nuc_A, nuc_Z, data):
    data_st = np.zeros(nctl_st)
    for k in range(0,nctl):
        finding_stable = True
        nuc_A_decay = nuc_A[k]
        nuc_Z_decay = nuc_Z[k]

        while finding_stable :
            for kst in range(0,nctl_st) :
                if nuc_A_decay==nuc_A_st[kst] and nuc_Z_decay==nuc_Z_st[kst] :
                    finding_stable = False
                    data_st[kst] += data[k]
#                    print (k,nuc_A_decay,nuc_Z[k],nuc_Z_decay)
            nuc_Z_decay -= 1
            if nuc_Z_decay < 0 :
                break

#    for kst in range(0,nctl_st) :
#        print (kst, nuc_Z_st[kst], nuc_A_st[kst], data_st[kst])

    return data_st





