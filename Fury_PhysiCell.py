# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:29:24 2019

@author: fkurtog
"""
import numpy as np
import pandas as pd
from pyMCDS import pyMCDS
from fury import window, actor, ui
import itertools
import vtk
import glob
import time

#%% Parsing Time-Series Data
t= time.time()

SphereActor_list=[]
for fin in glob.glob("output*.xml"):
    mcds=pyMCDS(fin, load_microenv=False)
    data=mcds.get_cell_df()
    Types = np.array([mcds.data['discrete_cells']['cell_type']])
    Fibro = np.where(Types == 2)
    Organoid = np.where(Types == 1)
    #Cells
    C_xpos = np.array([pd.DataFrame.to_numpy(data['position_x'][:])])
    C_ypos = np.array([pd.DataFrame.to_numpy(data['position_y'][:])])
    C_zpos = np.array([pd.DataFrame.to_numpy(data['position_z'][:])])
    C_xyz = np.concatenate((C_xpos,C_ypos,C_zpos),axis=0)
    C_xyz=C_xyz.transpose()
    # Whole Cell
    # Cell Radius Calculation
    C_volume = np.array([pd.DataFrame.to_numpy(data['total_volume'][:])])
    C_volume = C_volume/4/np.pi*3
    C_radii = np.power(C_volume,1/3).transpose()
    # Coloring
    C_R = np.array([np.ones(len(C_radii))]).transpose()
    C_G = np.array([np.ones(len(C_radii))]).transpose()
    C_B = np.array([np.ones(len(C_radii))]).transpose()
    C_O = np.array([np.ones(len(C_radii))]).transpose()*0.6
    # Type 1 (Organoid)
    C_R[Fibro[1]] = 0
    C_G[Fibro[1]] = 0.353
    C_B[Fibro[1]] = 1
    # Type 2 (Fibroblast)
    C_R[Organoid[1]] = 1
    C_G[Organoid[1]] = 1
    C_B[Organoid[1]] = 0
    C_colors = np.concatenate((C_R,C_G,C_B,C_O),axis=1)
    # Nucleus
    N_xyz=C_xyz
    # Nucleus Radii
    N_volume = np.array([pd.DataFrame.to_numpy(data['nuclear_volume'][:])])
    N_volume = N_volume/4/np.pi*3
    N_radii = np.power(N_volume,1/3).transpose()
    N_R = np.array([np.ones(len(N_radii))]).transpose()*0.35
    N_G = np.array([np.ones(len(N_radii))]).transpose()*0.2
    N_B = np.array([np.ones(len(N_radii))]).transpose()*0.1
    N_O = np.array([np.ones(len(N_radii))]).transpose()*0.9
    N_colors = np.concatenate((N_R,N_G,N_B,N_O),axis=1)
    # Concatenations
    xyz = np.concatenate((C_xyz,N_xyz),axis=0)
    colors = np.concatenate((C_colors,N_colors),axis=0)
    radii = np.concatenate((C_radii,N_radii),axis=0)
    # Creating Sphere Actor for one time-point
    sphere_actor = actor.sphere(centers=xyz,colors=colors,radii=radii)
    SphereActor_list.append(sphere_actor)
    
elapsed = time.time() - t

print (elapsed)
#%% Gathering Data for only one-time step
mcds1 = pyMCDS('final.xml',load_microenv=False)
#Df= mcds1.get_cell_df()
#
#Types = np.array([mcds1.data['discrete_cells']['cell_type']])
#Fibro = np.where(Types == 2)
#Organoid = np.where(Types == 1)
#
## Total Cell
C_xpos1 = np.array([mcds1.data['discrete_cells']['position_x']])
C_ypos1 = np.array([mcds1.data['discrete_cells']['position_y']])
C_zpos1 = np.array([mcds1.data['discrete_cells']['position_z']])
C_xyz1 = np.concatenate((C_xpos1,C_ypos1,C_zpos1),axis=0)
C_xyz1=C_xyz1.transpose()
#
## Cell Radius Calculation
#C_volume = np.array([mcds1.data['discrete_cells']['total_volume']])
#C_volume = C_volume/4/np.pi*3
#C_radii = np.power(C_volume,1/3).transpose()
#
## Cell Colors & Opacity
#C_R = np.array([np.ones(len(C_radii))]).transpose()
#C_G = np.array([np.ones(len(C_radii))]).transpose()
#C_B = np.array([np.ones(len(C_radii))]).transpose()
#C_O = np.array([np.ones(len(C_radii))]).transpose()*0.2
#
## Type 1 (Organoid)
#C_R[Fibro[1]] = 0
#C_G[Fibro[1]] = 0.353
#C_B[Fibro[1]] = 1
#
## Type 2 (Fibroblast)
#C_R[Organoid[1]] = 1
#C_G[Organoid[1]] = 1
#C_B[Organoid[1]] = 0
#
#
#
## Color Matrix
#C_colors = np.concatenate((C_R,C_G,C_B,C_O),axis=1)
#
#
## Nucleus Calculations
#N_xyz=C_xyz
## Nucleus Radii
#N_volume = np.array([mcds1.data['discrete_cells']['nuclear_volume']])
#N_volume = N_volume/4/np.pi*3
#N_radii = np.power(N_volume,1/3).transpose()
#
#N_R = np.array([np.ones(len(N_radii))]).transpose()*0.35
#N_G = np.array([np.ones(len(N_radii))]).transpose()*0.2
#N_B = np.array([np.ones(len(N_radii))]).transpose()*0.1
#N_O = np.array([np.ones(len(N_radii))]).transpose()*0.9
#N_colors = np.concatenate((N_R,N_G,N_B,N_O),axis=1)
#
#
## Concatenations
#xyz = np.concatenate((C_xyz,N_xyz),axis=0)
#colors = np.concatenate((C_colors,N_colors),axis=0)
#radii = np.concatenate((C_radii,N_radii),axis=0)
#
## Creating Sphere Actor for one time-point
#sphere_actor = actor.sphere(centers=xyz,
#                            colors=colors,
#                            radii=radii)

# %% Clipping

def plane_source2(scale=50):
    my_vertices = np.array([[0,0,0],[1,1,0],[0,1,0],[1,0,0]])
    my_vertices = my_vertices * scale
    surface=actor.surface(my_vertices)
    return surface

def plane_source(position=[0.0,0.0,0.0],normal=[0.0,0.0,0.0]):
    plane = vtk.vtkPlaneSource()
    plane.SetCenter(position)
    plane.SetNormal(normal)
    x_origin = -1000.0
    y_origin = -1000.0
    plane.SetOrigin(x_origin,y_origin,0.0)
    plane.SetPoint1(1000.0, y_origin, 0.0 )
    plane.SetPoint2(x_origin,1000.0, 0.0 )
    planeMapper=vtk.vtkPolyDataMapper()
    planeMapper.SetInputConnection(plane.GetOutputPort())
    planeActor = vtk.vtkActor()
    planeActor.SetMapper(planeMapper)
    return planeActor


def clipper(inp,clip):
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(inp)
    clipper.SetClipFunction(clip)
    planeMapper=vtk.vtkPolyDataMapper()
    planeMapper.SetInputConnection(clipper.GetOutputPort())
    planeActor = vtk.vtkActor()
    planeActor.SetMapper(planeMapper)
    return planeActor




plane_actor=plane_source()
#sphere_actor.GetMapper().SetClippingPlanes(plane_actor.GetMapper().GetOutputPort())
scene = window.Scene()

scene.set_camera(position=(71.47, 19.45, 3469.03), focal_point=(6.70, -22.29, -18.06),
                 view_up=(0.00, 1.00, -0.01))

scene.add(SphereActor_list[0])
#scene.add(plane_actor)
#scene.add(actor.axes())
#
showm = window.ShowManager(scene,
                           size=(1080, 720), reset_camera=True,
                           order_transparent=True)

showm.initialize()

tb = ui.TextBlock2D(bold=True)

# use itertools to avoid global variables
counter = itertools.count()


#Drawing Axis
lines = [np.array([[-500.,-800.,-500.],[500.,-800.,-500.],[500.,800.,-500.],[-500.,800.,-500.],[-500.,-800.,-500.],[-500.,-800.,500.],[-500.,800.,500.],[-500.,800.,-500.],[-500.,800.,500.],[500.,800.,500.],[500.,800.,-500.],[500.,800.,-500.],[500.,-800.,-500.],[500.,-800.,500.],[500.,800.,500.],[500.,-800.,500.],[-500.,-800.,500.]])]
colors = np.random.rand(1,3)
c = actor.line(lines, colors)
scene.add(c)


def timer_callback(_obj, _event):
    global SphereActor_list
    cnt = next(counter)
    maxcnt = 200
    tb.message = "Time Point : " + str(cnt) + " hrs"
    #showm.scene.azimuth(0.05 * cnt)
    scene.camera_info()
    if (cnt % 1 == 0):
        showm.scene.rm_all()
        #lines = [np.array([[-500.,-800.,-500.],[500.,-800.,-500.],[500.,800.,-500.],[-500.,800.,-500.],[-500.,-800.,-500.],[-500.,-800.,500.],[-500.,800.,500.],[-500.,800.,-500.],[-500.,800.,500.],[500.,800.,500.],[500.,-800.,500.],[500.,-800.,-500.],[500.,800.,-500.]])]
        colors = np.random.rand(1,3)
        c = actor.line(lines, colors)
        scene.add(c)
        scene.add(tb)
        showm.scene.add(SphereActor_list[cnt])
        outname="viz_timer"+str(cnt)+".png"
        x_label = actor.text_3d(text='x axis (micron)',position=(-100,-900,550),font_size=50,justification='left')
        scene.add(x_label)
        y_label = actor.text_3d(text='y axis (micron)',position=(-900,0,550),font_size=50,justification='left')
        scene.add(y_label)
        z_label = actor.text_3d(text='z axis (micron)',position=(600,-900,0),font_size=50,justification='left')
        scene.add(z_label)
#        window.record(showm.scene, size=(1080, 720), out_path=outname)
        

    showm.render()
    if cnt == maxcnt:
        showm.exit()




# Run every 200 milliseconds
showm.add_timer_callback(True, 200, timer_callback)

showm.start()

