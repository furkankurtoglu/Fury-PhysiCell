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


mcds1 = pyMCDS('final.xml', '.')

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


# %%


def plane_source2(scale=50):
    my_vertices = np.array([[0,0,0],[1,1,0],[0,1,0],[1,0,0]])
    my_vertices = my_vertices * scale
    surface=actor.surface(my_vertices)
    return surface

def plane_source(position=[0,0,0],normal=[1.0,0,1.0]):
    plane = vtk.vtkPlaneSource()
    plane.SetCenter(position)
    plane.SetNormal(normal)
#    plane.SetOrigin([0,0,0])
    plane.SetPoint1([-10,0,0])
    plane.SetPoint2([10,0,0])
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


scene = window.Scene()

scene.set_camera(position=(-146.17, 982.29, -3440.16), focal_point=(0, 0, 0),
                 view_up=(0.03, 0.96, 0.27))

sphere_actor = actor.sphere(centers=xyz,
                            colors=colors,
                            radii=radii)

#plane_actor = plane_source()
plane_actor=plane_source()
#sphere_actor.SetClippingPlanes(plane_actor.GetMapper().GetOutputPort())
# clip_actor=clipper(sphere_actor.GetMapper().GetInput(),
#                   plane_actor.GetMapper().GetInput())
#scene.add(clip_actor)
scene.add(plane_actor)
#scene.add(sphere_actor)
scene.add(actor.axes())

showm = window.ShowManager(scene,
                           size=(1500, 1500), reset_camera=False,
                           order_transparent=True)

showm.initialize()

tb = ui.TextBlock2D(bold=True)

# use itertools to avoid global variables
counter = itertools.count()


def timer_callback(_obj, _event):
    cnt = next(counter)
    maxcnt = 400
    tb.message = "Let's count up to "+ str(maxcnt) + " and exit :" + str(cnt)
    #showm.scene.azimuth(0.05 * cnt)
    #sphere_actor.GetProperty().SetOpacity(cnt/100.)
    showm.render()
    scene.camera_info()
    if cnt == maxcnt:
        showm.exit()


scene.add(tb)

# Run every 200 milliseconds
showm.add_timer_callback(True, 200, timer_callback)

showm.start()
