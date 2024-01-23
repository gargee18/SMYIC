
import tifffile
from vedo import Volume


def set_spacing_from_tiff_to_volume(tiffpath,volume):
    vox,unit=read_voxel_size_from_single_tiff(tiffpath)
    volume.spacing(vox)
    

def open_tiff_as_volume(path):
    voxel_size_ref, unit_ref = read_voxel_size_from_single_tiff(path)
    vol_ref = Volume(path)
    vol_ref.spacing(voxel_size_ref)
    return vol_ref

def open_tiffs_as_volumes(pathref,pathmov):
    return open_tiff_as_volume(pathref),open_tiff_as_volume(pathmov)


def read_voxel_size_from_tiff_volumetric_image(ref,mov):
    voxel_size_ref, unit_ref = read_voxel_size_from_single_tiff(ref)
    voxel_size_mov, unit_mov = read_voxel_size_from_single_tiff(mov)

    return (voxel_size_ref, unit_ref), (voxel_size_mov, unit_mov)

def read_voxel_size_from_single_tiff(path):
    with tifffile.TiffFile(path) as tif:
        metadata = tif.pages[0]
        vox_size=[1,1,1]
        unit="mm"
        for tag in metadata.tags.values():
            #print(tag.name, ":", tag.value)
            if tag.name == 'XResolution':
                x_resolution = tag.value
                pix_size_x = (x_resolution[1] / x_resolution[0])
                vox_size[0]=pix_size_x
            elif tag.name == 'YResolution':
                y_resolution = tag.value
                pix_size_y = (y_resolution[1] / y_resolution[0])
                vox_size[1]=pix_size_y
            elif tag.name == 'ImageDescription':
                # Extract spacing information from the 'ImageDescription' tag
                description = tag.value
                # Split the description into key-value pairs
                pairs = description.split('\n') #assuming that each key-value pair is on a new line
                for pair in pairs:
                    key, value = pair.split('=') #the splitting is done at the equal sign
                    if key.strip() == 'spacing':
                            vox_size[2] = float(value.strip())
                    elif key.strip() == 'unit':
                            unit = value.strip()
    return vox_size,unit        

