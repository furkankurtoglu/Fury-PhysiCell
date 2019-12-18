# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:27:17 2019

@author: fkurtog
"""

from pyMCDS import pyMCDS
import scipy.io as sio

mcds = pyMCDS('output00000070.xml')
me = sio.loadmat('output00000070_microenvironment0.mat')
me = me['multiscale_microenvironment']

xdim= me[0][:]
ydim= me[1][:]
zdim= me[2][:]
oxygen = me[4][:]
glucose = me[5][:]
lactate = me[6][:]
glutamine = me[7][:]


#%%
b= mcds.get_mesh()
A=mcds.data['mesh']['voxels']['centers']

with open("PhysiCell3D_mesh.csv", 'w') as f:
#    f.write('# vtk DataFile Version 2.0')
#    f.write('\n')
#    f.write('ASCII')
#    f.write('\n')
#    f.write('DATASET RECTILINEAR_GRID')
#    f.write('\n')
#    f.write('DIMENSIONS 500 800 500')
#    f.write('\n')
#    f.write('X_COORDINATES 500 float')
#    f.write('\n')
#    for x in xx[0][1]:
#        f.write(str(x))
#        f.write(' ')
#    f.write('\n')
#    f.write('Y_COORDINATES 800 float')
#    f.write('\n')
#    for y in yy[0][1]:
#        f.write(str(y))
#        f.write(' ')
#    f.write('\n')
#    f.write('Z_COORDINATES 500 float')
#    f.write('\n')
#    for z in zz[0][1]:
#        f.write(str(z))
#        f.write(' ')
#    f.write('\n')
#    f.write('SCALARS scalar_variable float 1')
    f.write('xdim,ydim,zdim,oxygen,glucose,lactate,glutamine')
    f.write('\n')
    for i in range(len(glucose)):
        f.write(str(xdim[i]))
        f.write(',')
        f.write(str(ydim[i]))
        f.write(',')
        f.write(str(zdim[i]))
        f.write(',')
        f.write(str(oxygen[i]))
        f.write(',')
        f.write(str(glucose[i]))
        f.write(',')
        f.write(str(lactate[i]))
        f.write(',')
        f.write(str(glutamine[i]))
        f.write('\n')