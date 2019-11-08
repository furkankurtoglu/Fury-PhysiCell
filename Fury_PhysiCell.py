# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:29:24 2019

@author: fkurtog
"""
import numpy as np
from pyMCDS import pyMCDS
from fury import window, actor, ui
import itertools
import vtk
import glob

#%% Parsin Time-Series Data

#mcdslist=[]
#for fin in glob.glob("output*.xml"):
#    mcdslist.append(pyMCDS(fin, load_microenv=False))


#DF=mcdslist[0].get_cell_df()

    
#%% Gathering Data for only one-time step
mcds1 = pyMCDS('initial.xml',load_microenv=False)
Df= mcds1.get_cell_df()

Types = np.array([mcds1.data['discrete_cells']['cell_type']])
Fibro = np.where(Types == 2)
Organoid = np.where(Types == 1)

# Total Cell
C_xpos = np.array([mcds1.data['discrete_cells']['position_x']])
C_ypos = np.array([mcds1.data['discrete_cells']['position_y']])
C_zpos = np.array([mcds1.data['discrete_cells']['position_z']])
C_xyz1 = np.concatenate((C_xpos,C_ypos,C_zpos),axis=0)
C_xyz=C_xyz1.transpose()

# Cell Radius Calculation
C_volume = np.array([mcds1.data['discrete_cells']['total_volume']])
C_volume = C_volume/4/np.pi*3
C_radii = np.power(C_volume,1/3).transpose()

# Cell Colors & Opacity

C_R = np.array([np.ones(len(C_radii))]).transpose()
C_G = np.array([np.ones(len(C_radii))]).transpose()
C_B = np.array([np.ones(len(C_radii))]).transpose()
C_O = np.array([np.ones(len(C_radii))]).transpose()*0.2

# Type 1 (Organoid)
C_R[Fibro[1]] = 0
C_G[Fibro[1]] = 0.353
C_B[Fibro[1]] = 1

# Type 2 (Fibroblast)
C_R[Organoid[1]] = 1
C_G[Organoid[1]] = 1
C_B[Organoid[1]] = 0



# Color Matrix
C_colors = np.concatenate((C_R,C_G,C_B,C_O),axis=1)


# Nucleus Calculations
N_xyz=C_xyz
# Nucleus Radii
N_volume = np.array([mcds1.data['discrete_cells']['nuclear_volume']])
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
sphere_actor = actor.sphere(centers=xyz,
                            colors=colors,
                            radii=radii)

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

scene.set_camera(position=(-146.17, 982.29, -3440.16), focal_point=(0, 0, 0),
                 view_up=(0.03, 0.96, 0.27))

#scene.add(plane_actor)
scene.add(sphere_actor)
#scene.add(actor.axes())

showm = window.ShowManager(scene,
                           size=(1080, 720), reset_camera=True,
                           order_transparent=True)

showm.initialize()

tb = ui.TextBlock2D(bold=True)

# use itertools to avoid global variables
counter = itertools.count()



#%% Drawing Axis
#lines = [np.array([[-500.,-800.,-500.],[500.,-800.,-500.],[500.,800.,-500.],[-500.,800.,-500.],[-500.,-800.,-500.],[-500.,-800.,500.],[-500.,800.,500.],[-500.,800.,-500.],[-500.,800.,500.],[500.,800.,500.],[500.,-800.,500.],[500.,-800.,-500.],[500.,800.,-500.]])]
#lines = [np.random.rand(10, 3), np.random.rand(20, 3)]
#colors = np.random.rand(1,3)
#c = actor.line(lines, colors)
#scene.add(c)


def timer_callback(_obj, _event):
    cnt = next(counter)
    maxcnt = 400
    tb.message = "Let's count up to "+ str(maxcnt) + " and exit :" + str(cnt)
    #showm.scene.azimuth(0.05 * cnt)
    showm.render()
    #scene.camera_info()
    if cnt == maxcnt:
        showm.exit()


scene.add(tb)

# Run every 200 milliseconds
showm.add_timer_callback(True, 200, timer_callback)

showm.start()