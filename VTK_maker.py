# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:27:17 2019

@author: fkurtog
"""

from pyMCDS import pyMCDS
import scipy.io as sio

mcds = pyMCDS('output00000070.xml')
me = sio.loadmat('output00000070_microenvironment0.mat')
#%%
xx, yy, zz = mcds.get_mesh()
glu=mcds.data['continuum_variables']['glucose']['data']
xdim= glu[:][0][0].size
ydim= glu[0][:][0].size
zdim= glu[0][0][:].size


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
    counter = 0
    f.write('xdim,ydim,zdim,glu')
    f.write('\n')
    for i in range(0,70):
        for j in range(0,ydim):
            for k in range(0,zdim):
                f.write(str(A[0][counter]))
                f.write(',')
                f.write(str(A[1][counter]))
                f.write(',')
                f.write(str(A[2][counter]))
                f.write(',')
                f.write(str(glu[i][j][k]))
                counter += 1
                print(counter)
                f.write('\n')