# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 14:31:36 2019

@author: fkurtog
"""
from fury import window, ui
import numpy as np

line_slider = ui.LineSlider2D(center=(500, 250), initial_value=0,
                              min_value=0, max_value=370,text_template="{value:.0f}")

def line_slider_value(slider):
    print (int(np.round(slider.value)))

line_slider.on_change = line_slider_value


examples = [[line_slider]]


def display_element():
    for element in example:
        element.set_visibility(True)




current_size = (800, 800)
show_manager = window.ShowManager(size=current_size, title="FURY UI Example")

for example in examples:
    for element in example:
        show_manager.scene.add(element)



interactive = True

if interactive:
    show_manager.start()
