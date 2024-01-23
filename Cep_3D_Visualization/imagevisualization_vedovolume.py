""" 
-------------------
This script allows to import and visualize images in 3D using vedo library .




-------------------
"""

import numpy as np

import vtk
from vedo import dataurl, Volume, Text2D, Axes, Box, settings, show, Plotter, Mesh
from vedo.applications import Slicer3DPlotter, IsosurfaceBrowser, RayCastPlotter
from vedo.pyplot import histogram
from vtkmodules.vtkRenderingCore import *
import matplotlib
import matplotlib.pyplot as plt

import volume_utils




#Change this to view another specimen
current_specimen="cep_313B"

#Change this according to your local configuration of data storage
custom_user_path_to_registered_data="/home/phukon/Desktop/registration/"


ref_input_path=custom_user_path_to_registered_data + current_specimen + "/result/Exported_data/img_reference_after_registration.tif"
mov_input_path_equalized=custom_user_path_to_registered_data + current_specimen + "/result/Exported_data/img_moving_after_registration_equalized.tif"
mov_input_path=custom_user_path_to_registered_data + current_specimen + "/result/Exported_data/img_moving_after_registration.tif"

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

    
# Display using "plotter"
plt = Plotter(axes=1,N=4)
plt.at(0).show("lost density", newdiffvol_2022_2023.color('red'), bg='black', axes = 0)
plt.at(1).show("gained density", newdiffvol_2023_2022.color('green'), bg='black', axes = 0)
plt.at(2).show("concatenated volumes", newdiffvol_2022_2023.color('red'),bg='black',axes = 0)
plt.at(2).show("concatenated volumes", newdiffvol_2023_2022.color('green'), bg='black',axes = 0)
plt.at(3).show("2022 and 2023", vol_ref.color('red'), bg='black',axes = 0)
plt.at(3).show("2022 and 2023", vol_mov.color('green'), bg='black',axes = 0)
plt.at(3)._extralight=vtk.vtkLight()

# Setting custom properties(Specular, Diffuse, Ambient, Opacity) 
volumes=plt.get_volumes(at=0)
vol=volumes[0]
custom_properties=vol.properties
custom_properties.SetSpecular(0.9)
custom_properties.SetDiffuse(0.9)
custom_properties.SetAmbient(1)
compositeOpacity = vtk.vtkPiecewiseFunction()
compositeOpacity.AddPoint(50.0,0.0);
compositeOpacity.AddPoint(150.0,0.6);
compositeOpacity.AddPoint(255.0,0.9);
custom_properties.SetScalarOpacity(compositeOpacity)

volumes=plt.get_volumes(at=1)
vol=volumes[0]
custom_properties=vol.properties
custom_properties.SetSpecular(0.9)
custom_properties.SetDiffuse(0.9)
custom_properties.SetAmbient(1)
compositeOpacity = vtk.vtkPiecewiseFunction()
compositeOpacity.AddPoint(50.0,0.0);
compositeOpacity.AddPoint(150.0,0.6);
compositeOpacity.AddPoint(256.0,0.9);
custom_properties.SetScalarOpacity(compositeOpacity)


volumes=plt.get_volumes(at=2)
vol=volumes[0]
custom_properties=vol.properties
custom_properties.SetSpecular(0.9)
custom_properties.SetDiffuse(0.9)
custom_properties.SetAmbient(0.7)
compositeOpacity = vtk.vtkPiecewiseFunction()
compositeOpacity.AddPoint(50.0,0.0);
compositeOpacity.AddPoint(200.0,0.05);
compositeOpacity.AddPoint(256.0,0.02);
custom_properties.SetScalarOpacity(compositeOpacity)

vol=volumes[1]
custom_properties=vol.properties
custom_properties.SetSpecular(0.8)
custom_properties.SetDiffuse(0.8)
custom_properties.SetAmbient(0.7)
compositeOpacity = vtk.vtkPiecewiseFunction()
compositeOpacity.AddPoint(50.0,0.0);
compositeOpacity.AddPoint(200.0,0.05);
compositeOpacity.AddPoint(256.0,0.01);
custom_properties.SetScalarOpacity(compositeOpacity)


volumes=plt.get_volumes(at=3)
vol_0=volumes[0]
custom_properties_0=vol_0.properties
custom_properties_0.SetSpecular(1)
custom_properties_0.SetDiffuse(0.5)
custom_properties_0.SetAmbient(0.5)
compositeOpacity_0 = vtk.vtkPiecewiseFunction()
compositeOpacity_0.AddPoint(0,0);
compositeOpacity_0.AddPoint(30.0,0.0);
compositeOpacity_0.AddPoint(50.0,0.05);
compositeOpacity_0.AddPoint(200.0,0.05);
compositeOpacity_0.AddPoint(256.0,0.05);
funcOpacityGradient_0 = vtk.vtkPiecewiseFunction()
funcOpacityGradient_0.AddPoint(1,   0.01)
funcOpacityGradient_0.AddPoint(5,   0.2)
funcOpacityGradient_0.AddPoint(30,  0.5)
custom_properties_0.SetGradientOpacity(funcOpacityGradient_0)
custom_properties_0.SetScalarOpacity(compositeOpacity_0)

vol_1=volumes[1]
custom_properties_1=vol_1.properties
custom_properties_1.SetSpecular(1)
custom_properties_1.SetDiffuse(0.5)
custom_properties_1.SetAmbient(0.5)
compositeOpacity_1 = vtk.vtkPiecewiseFunction()
compositeOpacity_1.AddPoint(30.0,0.0);
compositeOpacity_1.AddPoint(50.0,0.05);
compositeOpacity_1.AddPoint(200.0,0.05);
compositeOpacity_1.AddPoint(256.0,0.05);
custom_properties_1.SetInterpolationTypeToLinear()    
custom_properties_1.SetSpecularPower(100) 

##compositeOpacity.AddPoint(50.0,0.0);
#compositeOpacity.AddPoint(200.0,0.05);
#compositeOpacity.AddPoint(256.0,0.01);
custom_properties_1.SetScalarOpacity(compositeOpacity_1)

funcOpacityGradient_1 = vtk.vtkPiecewiseFunction()
funcOpacityGradient_1.AddPoint(1,   0.01)
funcOpacityGradient_1.AddPoint(5,   0.2)
funcOpacityGradient_1.AddPoint(30,  0.5)
custom_properties_1.SetGradientOpacity(funcOpacityGradient_1)
custom_properties_1.ShadeOn()
    
plt.interactive().close()





# select vedo visualizer
# vedo_type = "raycasterD"


# if vedo_type == "isobrowser":
#     plt= IsosurfaceBrowser(newdiffvol_2023_2022, use_gpu=True, c='gold')
#     plt.show(axes=7, bg2='lb').close()

    
    

# elif vedo_type == "raycaster":

#     # raycaster
#     # Load Volume data
#     newdiffvol_2022_2023.mode(1).cmap("jet")  # change visual properties

#     # Create a Plotter instance and show
#    plt = RayCastPlotter(vol_ref, bg='black', bg2='blackboard', axes=7)
#     plt.show(viewup="z")


# elif vedo_type == "slicer":


#     plt = Slicer3DPlotter(
#         vol,
#         cmaps=("gist_ncar_r", "jet", "Spectral_r", "hot_r", "bone_r"),
#         use_slider3d=False,
#         bg="white",
#         bg2="blue9",
#     )

#     plt.show(viewup='z')
    

# elif vedo_type == "slab_vol":
    
#     vaxes = Axes(vol, xygrid=False)

#     slab = vol.slab([45,55], axis='z', operation='mean')
#     slab.cmap('Set1_r', vmin=10, vmax=80).add_scalarbar("intensity")
#     # histogram(slab).show().close()  # quickly inspect it

#     bbox = slab.metadata["slab_bounding_box"]
#     slab.z(-bbox[5] + vol.zbounds()[0])  # move slab to the bottom

#     # create a box around the slab for reference
#     slab_box = Box(bbox).wireframe().c("black")

#     show(__doc__, vol, slab, slab_box, vaxes, axes=14, viewup='z')