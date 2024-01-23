"""
-------------------
This script allows to import and visualize images in 3D using vedo library .



-------------------
"""

import numpy as np

import vtk
from vedo import dataurl, Volume, Text2D, Axes, Box, settings, show, Plotter, Mesh
from vedo import *
from vedo.applications import Slicer3DPlotter, IsosurfaceBrowser, RayCastPlotter
from vedo.pyplot import histogram
from vtkmodules.vtkRenderingCore import *
import matplotlib
import matplotlib.pyplot as plt

import volume_utils




#Change this to view another specimen
current_specimen="cep_368B"

#Change this according to your local configuration of data storage
custom_user_path_to_registered_data="/home/phukon/Desktop/registration/"


ref_input_path=custom_user_path_to_registered_data + current_specimen + "/result/Exported_data/img_reference_after_registration_median_f_crop.tif"
mov_input_path=custom_user_path_to_registered_data + current_specimen + "/result/Exported_data/img_moving_after_registration_median_f_crop.tif"

print("Loading volume...")
vol_ref,vol_mov=volume_utils.open_tiffs_as_volumes(ref_input_path,mov_input_path)
print("Volume loaded")

# Convert to numpy, and with arithmetic operations, compute the diff and sum of both volumes
matmov=vol_mov.tonumpy()
matref=vol_ref.tonumpy()
matref=matref.astype(float)
matmov=matmov.astype(float)

# What's new tissues --> Compute the arithmetic operation (2023 - 2022) and keep only positive values (set 0 if negative)
newdiff_2023_2022=np.maximum(0, matmov-matref)
newdiffvol_2023_2022=Volume(newdiff_2023_2022)
volume_utils.set_spacing_from_tiff_to_volume(ref_input_path,newdiffvol_2023_2022)

# What's lost tissues --> Compute the arithmetic operation (2022 - 2023) and keep only positive values (set 0 if negative)
newdiff_2022_2023=np.maximum(0, matref-matmov)
newdiffvol_2022_2023=Volume(newdiff_2022_2023)
volume_utils.set_spacing_from_tiff_to_volume(ref_input_path,newdiffvol_2022_2023)

#Some kind of verification ?
assert np.sum(np.abs(newdiff_2022_2023-newdiff_2023_2022)) != 0 , "Images are zero, or images are identical. Critical fail!"

# concatenate the volumes
concat = newdiff_2023_2022 + newdiff_2022_2023
concat_vol = Volume(concat)
volume_utils.set_spacing_from_tiff_to_volume(ref_input_path,concat_vol)


from vedo import dataurl, show, BoxCutter, Volume

# generate an isosurface the volume for each thresholds
threshold = 100; threshold_22 = 80; threshold_23 = 80
silhouette = vol_ref.isosurface(threshold)
newdiffvol_2022_2023 = newdiffvol_2022_2023.isosurface(threshold_22)
newdiffvol_2023_2022 = newdiffvol_2023_2022.isosurface(threshold_23)
# Display using "plotter"
plt = Plotter(axes=1,N=1)
plt.at(0).show("bla",silhouette.color('white'), bg='black', axes = 0)
plt.at(0).show("dd", newdiffvol_2022_2023.color('red'), bg='black', axes = 0)
plt.at(0).show("dd", newdiffvol_2023_2022.color('green'), bg='black', axes = 0)
# Setting custom properties(Specular, Diffuse, Ambient, Opacity) 


def update_property(widget, event, property_setter):
    value = widget.GetRepresentation().GetValue()
    property_setter(value)


def add_slider(plt, property_setter, title, x1, y1, x2, y2):
    plt.at(0).add_slider(
        lambda widget, event: update_property(widget, event, property_setter),
        0, 1,
        value=0.5,
        pos=[(x1, y1), (x2, y2)],
        title=title,
    )


#define slider for Silhouette 
add_slider(plt, silhouette.properties.SetSpecular, "specular", 0.75, 0.1, 0.75, 0.26)
add_slider(plt, silhouette.properties.SetDiffuse, "diffuse", 0.82, 0.1, 0.82, 0.26)
add_slider(plt, silhouette.properties.SetAmbient, "ambient", 0.89, 0.1, 0.89, 0.26)
add_slider(plt, silhouette.properties.SetOpacity, "opacity", 0.96, 0.1, 0.96, 0.26)


# define slider for red
add_slider(plt, newdiffvol_2022_2023.properties.SetSpecular, "specular", 0.10, 0.1, 0.10, 0.26)
add_slider(plt, newdiffvol_2022_2023.properties.SetDiffuse, "diffuse",  0.17, 0.1, 0.17, 0.26)
add_slider(plt, newdiffvol_2022_2023.properties.SetAmbient, "ambient",  0.24, 0.1, 0.24, 0.26)
add_slider(plt, newdiffvol_2022_2023.properties.SetOpacity, "opacity",  0.31, 0.1, 0.31, 0.26)


# define slider for green
add_slider(plt, newdiffvol_2023_2022.properties.SetSpecular, "specular", 0.10, 0.74, 0.10, 0.9)
add_slider(plt, newdiffvol_2023_2022.properties.SetDiffuse, "diffuse",  0.17, 0.74, 0.17, 0.9)
add_slider(plt, newdiffvol_2023_2022.properties.SetAmbient, "ambient",  0.24, 0.74, 0.24, 0.9)
add_slider(plt, newdiffvol_2023_2022.properties.SetOpacity, "opacity",  0.31, 0.74, 0.31, 0.9)


plt.interactive().close()




