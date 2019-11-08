from fury import actor, window, utils
import numpy as np

centers = np.array([[0, 0, 0],
                    [0, -1, 0],
                    [0, 1, 0.]])

dirs = np.array([[1, 0, 0],
                 [1, 0, 0],
                 [1, 0, 0.]])

colors = np.random.rand(3, 3)

arrows = actor.arrow(centers=centers, colors=colors, directions=dirs)
showm = window.ShowManager(size=(1800, 600))

nb_pts = arrows.GetMapper().GetInput().GetReferenceCount()

pts = utils.numpy_support.vtk_to_numpy(arrows.GetMapper().GetInput().GetPoints().GetData())


def timer_callback(_obj, _event):

    global pts

    centers_update = np.array([[0.01, 0, 0],
                               [0.02, 0, 0],
                               [0.03, 0, 0.]])
    centers_update = np.repeat(centers_update, pts.shape[0]/nb_pts, axis=0)
    pts += centers_update

    arrows.GetMapper().GetInput().SetPoints(utils.numpy_to_vtk_points(pts))
    arrows.GetMapper().GetInput().ComputeBounds()

    showm.render()


showm.scene.add(arrows)
showm.initialize()
showm.add_timer_callback(True, 200, timer_callback)

showm.start()