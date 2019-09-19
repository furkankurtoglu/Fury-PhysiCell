# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:29:24 2019

@author: fkurtog
"""
import numpy as np
from pyMCDS import pyMCDS
from fury import window, actor, ui
import itertools

mcds1 = pyMCDS('final.xml', '.')

xpos = np.array([mcds1.data['discrete_cells']['position_x']])
ypos = np.array([mcds1.data['discrete_cells']['position_y']])
zpos = np.array([mcds1.data['discrete_cells']['position_z']])
xyz1 = np.concatenate((xpos,ypos,zpos),axis=0)
xyz=xyz1.transpose()

# Radius Calculation
volume = np.array([mcds1.data['discrete_cells']['total_volume']])
volume = volume/4/np.pi*3
radius = np.power(volume,1/3)
radii = radius.transpose()

# Oncoprotein
#oncoprotein = np.array([mcds1.data['discrete_cells']['oncoprotein']])
#oncoprotein = oncoprotein.transpose()/np.amax(oncoprotein)

R = np.array([np.ones(len(radii))]).transpose()
G = np.array([np.ones(len(radii))]).transpose()
B = np.array([np.ones(len(radii))]).transpose()
O = np.array([np.ones(len(radii))]).transpose()*0.8
#%%
#xyz= 10 * np.random.rand(100, 3)
colors = np.concatenate((R,G,B,O),axis=1)
# radii = np.random.rand(len(xyz)) + 0.5


scene = window.Scene()

scene.set_camera(position=(194.50, -251.46, 3566.50), focal_point=(0, 0, 0),
                 view_up=(0.08, 0.99, 0.07))

sphere_actor = actor.sphere(centers=xyz,
                            colors=colors,
                            radii=radii)

scene.add(sphere_actor)
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
    tb.message = "Let's count up to 100 and exit :" + str(cnt)
    #showm.scene.azimuth(0.05 * cnt)
    #sphere_actor.GetProperty().SetOpacity(cnt/100.)
    showm.render()
    scene.camera_info()
    if cnt == 100:
        showm.exit()


scene.add(tb)

# Run every 200 milliseconds
showm.add_timer_callback(True, 200, timer_callback)

showm.start()
