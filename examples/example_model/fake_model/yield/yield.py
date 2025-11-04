import sys

import numpy as np

args = sys.argv

E_exp     = float(args[1])
t_bomb    = float(args[2])
nstg      = int(args[3])
ye_masscut= 0.48
masscut   = float(args[4])
massout   = float(args[5])
file_str  = '../writestr/str'+args[3]+'.txt'
file_cx   = '../cxdata/cxdat'+args[3]+'.txt'


data_str = np.loadtxt(file_str)
# get mesh_tot
mesh_tot = data_str.shape[0]





with open(file_cx, 'r') as f:
    cx_line = f.readlines()
# get nctl
with open(file_cx, 'r') as f:
    line_tot= sum(1 for line in f)
line_nctl = int( ((line_tot-1)/mesh_tot-1)/3 )
line_tot  = line_nctl*3 + 1
jmesh     = 1
line_base = (jmesh-1)*line_tot
subline2  = cx_line[line_base+ 2:line_base+(2+line_nctl)]
concent_mesh = []
for elem_list in subline2:
    elem_list = elem_list.rstrip('\n').split()
    for elem in elem_list:
        concent_mesh.append( float(elem) )
concent_mesh = np.array( concent_mesh )
nctl  = concent_mesh.shape[0]

# mass resolution
dmass = []
for jmesh in range(1,mesh_tot+1):
    dmass.append( data_str[jmesh-1,7] )
dmass = np.array(dmass)
#print(dmass)

###
if( masscut==1.0 ):
    for jmesh in range(1,mesh_tot+1):
        ye_mesh = data_str[jmesh-1,19]
        if( ye_mesh > ye_masscut ):
            masscut = data_str[jmesh-1,6]
            break

#print(ye_mesh)
#print(ye_masscut)
#print(masscut)
###

i_masscut = np.argmin( abs(data_str[:,6]-masscut) )
mass_cut  = data_str[i_masscut,6]
if( mass_cut > masscut ):
    i_masscut = i_masscut-1
    mass_cut  = data_str[i_masscut,6]

i_massout = np.argmin( abs(data_str[:,6]-massout) )
mass_out  = data_str[i_massout,6]
if( mass_out > massout ):
    i_massout  = i_massout-1
    mass_out   = data_str[i_massout,6]

# concentration.
# firstly 1-mesh concentrations are made as an array [concent].
concent = []
for jmesh in range(1,mesh_tot+1):

    line_base = (jmesh-1)*line_tot
    subline1  = cx_line[line_base+ 1             :line_base+ 2             ]
    subline2  = cx_line[line_base+ 2             :line_base+(2+line_nctl  )]
    subline3  = cx_line[line_base+(2+line_nctl  ):line_base+(2+line_nctl*2)]
    subline4  = cx_line[line_base+(2+line_nctl*2):line_base+(2+line_nctl*3)]

    concent_mesh = []
    for elem_list in subline2:
        elem_list = elem_list.rstrip('\n').split()
        for elem in elem_list:
            concent_mesh.append( float(elem) )

    concent_mesh = np.array(concent_mesh)
    concent.append( concent_mesh )

# secondly full-elemtent concent. dist. are made as an array [concent_all],
# which is made of 1-element conc. dist. [concent_elem].
concent_all = []
for k in range(0,nctl):
    concent_elem = []
    for jmesh in range(1,mesh_tot+1):
        concent_elem.append( concent[jmesh-1][k] )

    concent_elem = np.array(concent_elem)
#    print(concent_elem)
    concent_all.append(concent_elem)

#dot product
prod = []
for k in range(0,nctl):
    prod.append( np.dot(dmass[i_masscut+1:i_massout+1],concent_all[k][i_masscut+1:i_massout+1]) )
prod     = np.array(prod)



# explosion energy
mass= []
rad = []
vel = []
eint= []
for jmesh in range(1,mesh_tot+1):
    mass.append( data_str[jmesh-1, 6] )
    rad .append( data_str[jmesh-1, 8] )
    vel .append( data_str[jmesh-1,10] )
    eint.append( data_str[jmesh-1,17] )

tmp = 6.67384e-8 * 1.989e33 * 0.5
ekin= []
egrv= []
jmesh = 1
ekin.append( vel[jmesh-1]*vel[jmesh-1] )
egrv.append(-tmp*(mass[jmesh-1]/rad[jmesh-1]
                 +mass[jmesh-1]/rad[jmesh-1]) )
for jmesh in range(2,mesh_tot+1):
    ekin.append( 0.5*vel[jmesh-1]*vel[jmesh-1] )
    egrv.append(-tmp*(mass[jmesh-2]/rad[jmesh-2]
                     +mass[jmesh-1]/rad[jmesh-1]) )

eint_tot = np.dot(dmass[i_masscut+1:i_massout+1]
                  ,eint[i_masscut+1:i_massout+1] )*1.989e33
ekin_tot = np.dot(dmass[i_masscut+1:i_massout+1]
                  ,ekin[i_masscut+1:i_massout+1] )*1.989e33
egrv_tot = np.dot(dmass[i_masscut+1:i_massout+1]
                  ,egrv[i_masscut+1:i_massout+1] )*1.989e33
etot_out = eint_tot + ekin_tot + egrv_tot

eint_tot = np.dot(dmass[i_masscut+1:mesh_tot+1]
                  ,eint[i_masscut+1:mesh_tot+1] )*1.989e33
ekin_tot = np.dot(dmass[i_masscut+1:mesh_tot+1]
                  ,ekin[i_masscut+1:mesh_tot+1] )*1.989e33
egrv_tot = np.dot(dmass[i_masscut+1:mesh_tot+1]
                  ,egrv[i_masscut+1:mesh_tot+1] )*1.989e33
etot_tot = eint_tot + ekin_tot + egrv_tot

#print('%12.4e'%eint_tot)
#print('%12.4e'%ekin_tot)
#print('%12.4e'%egrv_tot)
#print('%12.4e'%etot_tot)
#sys.exit()

# output
mass_int = np.sum( dmass[i_masscut+1:i_massout+1] )
mass_sum = np.sum( prod )
mass_eje = mass_out - mass_cut
print ('%14.5e'%E_exp   , end='')
print ('%14.5e'%t_bomb  , end='')
print ('%7i'   %nstg    , end='')
print ('%14.5e'%mass_cut, end='')
print ('%14.5e'%mass_out, end='')
print ('%14.5e'%mass_eje, end='')
#print ('%14.5e'%mass_sum, end='')
#print ('%14.5e'%mass_int, end='')
print ('%14.5e'%etot_out, end='')
print ('%14.5e'%etot_tot, end='')

for k in range(0,nctl):
    prod[k] = prod[k]*(mass_eje/mass_int)
for k in range(0,nctl):
    print ('%14.5e'%prod[k], end='')

print()

