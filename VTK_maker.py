# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:27:17 2019

@author: fkurtog
"""


import scipy.io as sio
import glob


def me_loader(mat,cnt):
    me = sio.loadmat(mat)
    me = me['multiscale_microenvironment']
    xdim= me[0][:]
    ydim= me[1][:]
    zdim= me[2][:]
    oxygen = me[4][:]
    glucose = me[5][:]
    lactate = me[6][:]
    glutamine = me[7][:]
    name="PhysiCell3D_mesh_" + str(cnt)+".csv"
    with open(name, 'w') as f:
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
            
output_list = glob.glob("output*0.mat")
cnt=1
for mat in output_list:
    sphere_actor = me_loader(mat,cnt)
    cnt += 1