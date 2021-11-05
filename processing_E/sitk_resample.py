'''
@Description: 
@Autor: zhangcheng
@Date: 2020-05-08 12:25:02
LastEditors: zhangcheng
LastEditTime: 2021-05-19 06:33:59
@License: (C)Copyright 2020-2021, Aitrox-ZHANG
'''

import SimpleITK as sitk
import numpy as np


# ==============================================================================================
# resampling the sitk images with center aligned
def resample_sitkImage_centerAligned(sitkImage, newSize, newSpacing, vol_default_value='min', interpolator=sitk.sitkNearestNeighbor):
    """
    :param sitkImage:
    :param newSize: tuple (,,)
    :param newSpacing: tuple (,,)
    :param vol_default_value: 'min', or 'zero', or a numerical number
    :return:
        resampled image
    """

    # input checking
    if sitkImage is None:
        return None
    dim = sitkImage.GetDimension()
    if len(newSize) != dim:
        return None
    if len(newSpacing) != dim:
        return None

    # default value
    vol_value = 0.0
    if vol_default_value == 'min':
        vol_value = float(np.ndarray.min(sitk.GetArrayFromImage(sitkImage)))
    elif vol_default_value == 'zero':
        vol_value = 0.0
    elif str(vol_default_value).isnumeric():
        vol_value = float(vol_default_value)

    # original size, spacing, and origin
    np_old_size = np.array(sitkImage.GetSize(), dtype=np.int).reshape(dim, 1)
    np_old_spacing = np.array(sitkImage.GetSpacing(), dtype=np.float).reshape(dim, 1)
    np_old_origin = np.array(sitkImage.GetOrigin(), dtype=np.float).reshape(dim, 1)

    # direction
    np_matrix_direction = np.array(sitkImage.GetDirection()).reshape(dim, dim)

    # to be centered, condier the shift
    np_calibrated_shift = np.dot(np_matrix_direction, np_old_spacing*(np_old_size-1)/2)
    np_center = np_old_origin + np_calibrated_shift

    # new size, spacing, and origin
    np_new_size = np.array(newSize, dtype=np.int).reshape(dim, 1)
    np_new_spacing = np.array(newSpacing, dtype=np.float).reshape(dim, 1)
    np_calibrated_shift = np.dot(np_matrix_direction, np_new_spacing*(np_new_size-1)/2)
    np_new_origin = np_center - np_calibrated_shift

    newOrigin = tuple(np_new_origin[:, 0].tolist())

    transform = sitk.Transform()

    # perform the resample
    centerAlignedResampledsitkImage = sitk.Resample(sitkImage, newSize, transform,
                                                    interpolator, newOrigin, newSpacing,
                                                    sitkImage.GetDirection(), vol_value, sitkImage.GetPixelID())

    return centerAlignedResampledsitkImage


# ==============================================================================================
# resampling the sitkImages with new spacing
def resample_sitkImage_by_spacing(sitkImage, newSpacing, vol_default_value='min', interpolator=sitk.sitkNearestNeighbor):
    """
    :param sitkImage:
    :param newSpacing:
    :return:
    """
    if sitkImage == None:
        return None
    if newSpacing is None:
        return None

    dim = sitkImage.GetDimension()
    if len(newSpacing) != dim:
        return None

    # determine the default value
    vol_value = 0.0
    if vol_default_value == 'min':
        vol_value = float(np.ndarray.min(sitk.GetArrayFromImage(sitkImage)))
    elif vol_default_value == 'zero':
        vol_value = 0.0
    elif str(vol_default_value).isnumeric():
        vol_value = float(vol_default_value)

    # calculate new size
    np_oldSize = np.array(sitkImage.GetSize())
    np_oldSpacing = np.array(sitkImage.GetSpacing())

    np_newSpacing = np.array(newSpacing)
    np_newSize = np.divide(np.multiply(np_oldSize, np_oldSpacing), np_newSpacing)
    newSize = tuple(np_newSize.astype(np.uint).tolist())

    # resample sitkImage into new specs
    transform = sitk.Transform()

    return sitk.Resample(sitkImage, newSize, transform, interpolator, sitkImage.GetOrigin(),
                         newSpacing, sitkImage.GetDirection(), vol_value, sitkImage.GetPixelID())

# ==============================================================================================
# resampling the sitkImages with specified size (new spacing)
def resample_sitkImage_by_size(sitkImage, newSize, vol_default_value='min'):
    """
    :param sitkImage:
    :param newSize:
    :return:
    """
    if sitkImage == None:
        return None
    if newSize is None:
        return None

    dim = sitkImage.GetDimension()
    if len(newSize) != dim:
        return None

    # determine the default value
    vol_value = 0.0
    if vol_default_value == 'min':
        vol_value = float(np.ndarray.min(sitk.GetArrayFromImage(sitkImage)))
    elif vol_default_value == 'zero':
        vol_value = 0.0
    elif str(vol_default_value).isnumeric():
        vol_value = float(vol_default_value)

    # calculate new size
    np_oldSize = np.array(sitkImage.GetSize())
    np_oldSpacing = np.array(sitkImage.GetSpacing())
    np_newSize = np.array(newSize)
    np_newSpacing = np.divide(np.multiply(np_oldSize, np_oldSpacing), np_newSize)
    newSpacing = tuple(np_newSpacing.astype(np.float).tolist())

    # resample sitkImage into new specs
    transform = sitk.Transform()

    return sitk.Resample(sitkImage, newSize, transform, sitk.sitkNearestNeighbor, sitkImage.GetOrigin(),
                         newSpacing, sitkImage.GetDirection(), vol_value, sitkImage.GetPixelID())


# ==============================================================================================
# resampling the sitkImages with specified size and spacing
def resample_sitkImage_by_sizeAndSpacing(sitkImage, newSize, newSpacing, vol_default_value='min', interpolator=sitk.sitkNearestNeighbor):
    """
    :param sitkImage:
    :param newSize:
    :return:
    """
    if sitkImage == None:
        return None
    if newSize is None:
        return None

    dim = sitkImage.GetDimension()
    if len(newSize) != dim:
        return None

    # determine the default value
    vol_value = 0.0
    if vol_default_value == 'min':
        vol_value = float(np.ndarray.min(sitk.GetArrayFromImage(sitkImage)))
    elif vol_default_value == 'zero':
        vol_value = 0.0
    elif str(vol_default_value).isnumeric():
        vol_value = float(vol_default_value)

    # resample sitkImage into new specs
    transform = sitk.Transform()

    return sitk.Resample(sitkImage, newSize, transform, interpolator, sitkImage.GetOrigin(),
                         newSpacing, sitkImage.GetDirection(), vol_value, sitkImage.GetPixelID())

if __name__ == "__main__":
    mask_file = "/hdd/zc_data/1.2.392.200036.9116.2.2417506549.1597042476.5.1014200002.1/mask.nii.gz"
    sitkImage = sitk.ReadImage(mask_file)
    np_oldSize = np.array(sitkImage.GetSize())
    np_oldSpacing = np.array(sitkImage.GetSpacing())
    newSpacing = [0.3,0.3,0.5]
    np_newSpacing = np.array(newSpacing)
    np_newSize = np.divide(np.multiply(np_oldSize, np_oldSpacing), np_newSpacing)
    newSize = tuple(np_newSize.astype(np.uint).tolist())
    img = resample_sitkImage_by_sizeAndSpacing(sitkImage, newSize, newSpacing)
    sitk.WriteImage(img, mask_file.replace('mask.nii.gz', 'Cmask.nii.gz'))
    img = resample_sitkImage_by_sizeAndSpacing(img, sitkImage.GetSize(), sitkImage.GetSpacing())
    sitk.WriteImage(img, mask_file.replace('mask.nii.gz', 'Bmask.nii.gz'))

    arr1 = sitk.GetArrayFromImage(sitkImage)
    arr2 = sitk.GetArrayFromImage(img)
    arr = arr1+arr2
    arr = arr.astype(np.uint8)
    img = sitk.GetImageFromArray(arr)
    img.CopyInformation(sitkImage)
    sitk.WriteImage(img, mask_file.replace('mask.nii.gz', 'combine.nii.gz'))
    x = 1
    