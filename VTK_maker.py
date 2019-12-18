# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:27:17 2019

@author: fkurtog
"""


import scipy.io as sio
import glob
import numpy as np


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
            
output_list_me = glob.glob("output*0.mat")
cnt=1
#for mat in output_list_me:
#    me = me_loader(mat,cnt)
#    cnt += 1


#%%
cnt=1
def cell_loader(mat,cnt):
    cs = sio.loadmat(mat)
    cs = cs['cells']
    x_pos = cs[1][:]
    y_pos = cs[2][:]
    z_pos = cs[3][:]
    cell_vol = cs[4][:]
    cell_vol = cell_vol/4/np.pi*3
    cell_vol = np.power(cell_vol,1/3)
    cell_type = cs[5][:]
    time_elapsed_in_the_phase = cs[8][:]
    name="PhysiCell3D_cells_" + str(cnt)+".csv"
    with open(name, 'w') as f:
        f.write('xpos,ypos,zpos,cell_radius,cell_type,time_elapse_in_phase')
        f.write('\n')
        for i in range(len(x_pos)):
            f.write(str(x_pos[i]))
            f.write(',')
            f.write(str(y_pos[i]))
            f.write(',')
            f.write(str(z_pos[i]))
            f.write(',')
            f.write(str(cell_vol[i]))
            f.write(',')
            f.write(str(cell_type[i]))
            f.write(',')
            f.write(str(time_elapsed_in_the_phase[i]))
            f.write('\n')
output_list_cs = glob.glob("output*l.mat")
for mat in output_list_cs:
    sphere_actors = cell_loader(mat,cnt)
    cnt += 1