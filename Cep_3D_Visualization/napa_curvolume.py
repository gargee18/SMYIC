import vedo
from vedo import utils
import vtk
from vtkmodules.util import numpy_support
import numpy as np
import scipy
from scipy.interpolate import splprep, splev
# Load the TIFF volume data
#dirpath="/home/phukon/Desktop/RealDataTest/1193/Raw_data"
#volume_path=dirpath+"/1193_2022.tif"




""" Compute the direction cosines from a list of points
    The direction cosines are the vectors between each point
    and the next point in the list. The other two vectors are
    computed by cross product in a tricky way.
"""
def create_direction_cosines_from_point_list(polyline):
    normals = []
    axiss0 = []
    axiss1 = []
    axiss2 = []
    N=len(polyline)
    for i in range(N - 1):
        p0 = polyline[i]
        p1 = polyline[i + 1]
        #Weird, but for radiological convention, the direction cosines are inverted
        normals.append([-p1[0] + p0[0], - p1[1] + p0[1], -p1[2] + p0[2]])

    #Compute the first orthogonal axis by choosing the axis that is the far away from normal
    normal=normals[0]
    axis2 = utils.versor(normal)
    if(np.abs(normal[1])<0.999):
        axisTemp=[0,-1,0]#In order to get X to the right and Y to the bottom
    else:
        axisTemp=[-1,0,0]

    axis0 = np.cross(axisTemp, axis2)
    axis1 = np.cross(axis2, axis0)
    axiss0.append(axis0)
    axiss1.append(axis1)
    axiss2.append(axis2)

    #Compute iteratively the following orthogonal axis
    for i in range(1,N-1):
        normal=normals[i]
        axis2 = utils.versor(normal)
        axis0Prev = axiss0[i-1]
        axis1 = np.cross(axis2, axis0Prev)
        axis0 = np.cross(axis1, axis2)
        axiss0.append(axis0)
        axiss1.append(axis1)
        axiss2.append(axis2)

    return axiss0,axiss1,axiss2    



def compute_slices_of_vtkImageData_along_curve(vtkImageData,curve,output_size = [300, 300],output_spacing=[1,1,1],debug=True):
    #Compute the direction cosines from the curve
    axiss0,axiss1,axiss2=create_direction_cosines_from_point_list(curve)

    #Compute the slices
    slices=[]
    for i in range(len(axiss0)):
        slice=vtk.vtkImageReslice()
        slice.SetInputData(vtkImageData)
        slice.SetResliceAxesDirectionCosines(axiss0[i][0],axiss0[i][1],axiss0[i][2],axiss1[i][0],axiss1[i][1],axiss1[i][2],axiss2[i][0],axiss2[i][1],axiss2[i][2])
        slice.SetResliceAxesOrigin(curve[i])
        slice.SetOutputDimensionality(2)
        slice.SetInterpolationModeToLinear()
        slice.SetOutputSpacing(output_spacing)
        slice.SetOutputExtent(0, output_size[0] - 1, 0, output_size[1] - 1, 0, 1)
        slice.SetOutputOrigin(
            -(output_size[0] * 0.5 - 0.5) * output_spacing[0],
            -(output_size[1] * 0.5 - 0.5) * output_spacing[1],
            0,
        )
        slice.Update()
        slices.append(slice)
        if(debug):
            print("Slice "+str(i)+" Origin="+str(curve[i])+" DirectionCosines="+str(axiss0[i])+" | "+str(axiss1[i])+" | "+str(axiss2[i]))
    return slices

def get_curve(num_curve=1):
    if(num_curve==0):
        curve_points = [
        [94,190,164],
        [94,190,165],
        [94,190,166],
        [94,190,167],
        [94,190,168],
        [94,190,169]
        ]

    if(num_curve==-1 or num_curve==-2):
        curve_points=[
  [252.8333, 339.1667, 1200],
  [251.8333, 338.8333, 1192],
  [246.8333, 340.1667, 1134],
  [242.5, 340.1667, 1088],
  [233.8333, 341.1667, 1011],
  [229.5, 343.1667, 948],
  [218.1667, 334.1667, 930],
  [213.5, 332.5, 917],
  [197.8333, 329.1667, 894],
  [189.1667, 331.5, 865],
  [192.5, 331.5, 834],
  [204.5, 331.5, 794],
  [210.5, 322.8333, 760],
  [221.1667, 319.1667, 728],
  [230.5, 313.8333, 699],
  [233.5, 310.1667, 670],
  [238.8333, 301.8333, 679],
  [252.8333, 286.5, 646],
  [266.1667, 276.5, 595],
  [273.5, 276.8333, 564],
  [275.1667, 276.8333, 531],
  [280.1667, 276.5, 497],
  [279.5, 277.5, 463],
  [278.1667, 278.5, 435],
  [279.8333, 277.8333, 407],
]



    if(num_curve==1 or num_curve==2):
        curve_points = [
        [66.5, 49, 38],
        [118.5, 113.5, 47],
        [125, 122.5, 49],
        [143, 148.5, 59],
        [156.1667, 167.5, 70],
        [164.1667, 182.8333, 81],
        [174.5, 200.1667, 93],
        [185.5, 225.5, 111],
        [192.8333, 244.1667, 127],
        [204.1667, 268.1667, 152],
        [213.5, 286.5, 173],
        [223.8333, 304.5, 192],
        [232.1667, 318.8333, 208],
        [239.1667, 333.5, 222],
        [247.5, 349.8333, 238],
        [261.1667, 367.8333, 258],
        [281.8333, 389.5, 283],
        [298.5, 403.8333, 300],
        [308.1667, 403.1667, 309],
        [315.1667, 400.1667, 315],
        [320.5, 394.8333, 322],
        [327.8333, 390.5, 330],
        [335.5, 385.8333, 338],
        [346.8333, 375.1667, 351],
        [359.1667, 367.1667, 363],
        [369.1667, 360.5, 371],
        [376.5, 355.8333, 378],
        [389.5, 346.1667, 388],
        [397.1667, 339.8333, 395],
        [408.8333, 328.5, 408],
        [421.1667, 318.1667, 422],
        [425.1667, 314.8333, 428],
        [430.1667, 310.8333, 435],
        [431.8333, 306.8333, 441],
        [431.8333, 305.1667, 445],
        [429.1667, 306.5, 452],
        [425.8333, 313.1667, 458],
        [420.1667, 318.8333, 464],
        [418.5, 317.1667, 465]
        ]
    if(num_curve==2 or num_curve==-2):
        #Resample the curve with a spline to get one point every 1mm
        curve_points=resampleCurve(curve_points,1)

    return curve_points

def resampleCurve(curve, spacing):
    # Convert the curve to a numpy array
    curve = np.array(curve)

    # Calculate the total length of the curve
    curve_length = np.sum(np.sqrt(np.sum(np.diff(curve, axis=0) ** 2, axis=1)))

    # Calculate the number of points needed to achieve the desired spacing
    num_points = int(np.ceil(curve_length / spacing))

    # Resample the curve using splines
    tck, u = splprep(curve.T, s=0, per=False)
    u_new = np.linspace(0, 1, num_points)
    curve_resampled = np.column_stack(splev(u_new, tck, der=0))

    return curve_resampled.tolist()


#Open volume_path as a vtkImageData object
dirpath="/home/phukon/Desktop/RealDataTest/1193/Raw_data"
outputdirpath=dirpath+"/output_test"
input_path=dirpath+"/1193_2022.tif"

#dirpath="/home/phukon/Desktop/RealDataTest/1193/Raw_data"  
volume_path=dirpath+"/1193_2022.tif"
#Open volume_path as a vtkImageData object
reader=vtk.vtkTIFFReader()
reader.SetFileName(volume_path)
reader.Update()
vtkImageData=reader.GetOutput()

#output_path=dirpath+"/output_02.tif"
reader=vtk.vtkTIFFReader()
reader.SetFileName(input_path)
reader.Update()
vtkImageData=reader.GetOutput()

#Get the curve
curve_points=get_curve(-2)

#Compute the slices
slices=compute_slices_of_vtkImageData_along_curve(vtkImageData,curve_points)

#write the slices
for i in range(len(slices)):
    slice_output=vtk.vtkTIFFWriter()
    slice_output.SetFileName(outputdirpath+"/"+str(i)+".tif")
    slice_output.SetInputData(slices[i].GetOutput())
    slice_output.Write()

