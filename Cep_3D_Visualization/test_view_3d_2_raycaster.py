dirpath="/home/rfernandez/Bureau/A_Test/Aerenchyme/Xrays/Test-02_curve-resampling"
input_path=dirpath+"/test_line_01.tif"
output_path=dirpath+"/output_01.tif"

"""Use sliders to slice volume
Click button to change colormap"""
from vedo import dataurl, Volume, Text2D
from vedo.applications import Slicer3DPlotter

vol = Volume(input_path)


from vedo import Volume, dataurl
from vedo.applications import RayCastPlotter

embryo = Volume(input_path).mode(1).c('jet')  # change properties

plt = RayCastPlotter(embryo, bg='black', bg2='blackboard', axes=7)  # Plotter instance

plt.show(viewup="z").close()