from vedo import *

# Load the TIFF image
dirpath="/home/phukon/Desktop/RealDataTest/313-B/Raw_data"
input_path=dirpath+"/313-B_2022-_ref.tif"
image = load(input_path)

"""Use sliders to slice volume
Click button to change colormap"""
from vedo import dataurl, Volume, Text2D
from vedo.applications import Slicer3DPlotter

vol = Volume(input_path)

plt = Slicer3DPlotter(
    vol,
    cmaps=("gist_ncar_r", "jet", "Spectral_r", "hot_r", "bone_r"),
    use_slider3d=False,
    bg="blue1",
    bg2="blue9",
)

# Can now add any other vedo object to the Plotter scene:
#plt += Text2D(__doc__)

plt.show(viewup='z')
plt.close()