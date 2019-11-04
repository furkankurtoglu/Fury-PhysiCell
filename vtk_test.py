import numpy as np
from fury import window, actor
ren = window.Renderer()
centers = np.random.rand(1, 3)
faces1 = np.random.rand(1, 3)
sphere_actor = actor.sphere(centers, window.colors.coral, faces == faces1)
ren.add(sphere_actor)
window.show(ren)
