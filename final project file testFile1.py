import pydicom
import os
import numpy as np
from matplotlib import pyplot
from PIL import Image
import nibabel as nib

def read_file():

    givenFileName = input('Enter file name : ')
    givenFileName += '.dcm'
    dcmdir = input('Enter file location : ')

    if os.path.isdir(dcmdir):
        for files in os.listdir(dcmdir):
            if givenFileName in files.lower() or givenFileName in files.upper() or givenFileName in files:
                ds = pydicom.read_file(dcmdir + givenFileName)
                return ds

        print('\n\t\tFile Not Found!\n\n')
        return None
    else:
        print('\n\t\tDirectory Not Found!\n\n')


def get_xy_dicomarray(ds):
    ConstPixelDims = (int(ds.Rows), int(ds.Columns))
    ConstPixelSpacing = (float(ds.PixelSpacing[0]), float(ds.PixelSpacing[1]), float(ds.SliceThickness))

    x = np.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0], ConstPixelSpacing[0])
    y = np.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])

    ArrayDicom = np.zeros(ConstPixelDims, dtype=ds.pixel_array.dtype)
    ArrayDicom[:, :] = ds.pixel_array

    return x, y, ArrayDicom


def show_file(x, y, ArrayDicom):

    pyplot.figure(dpi=150)
    pyplot.axes().set_aspect('equal')
    pyplot.set_cmap(pyplot.gray())
    pyplot.pcolormesh(x, y, np.flipud(ArrayDicom[:, :]))
    pyplot.show()


def convert_to_other_format(dcmFile):

    x, y, ArrayDicom = get_xy_dicomarray(dcmFile)

    img = Image.new('RGB', (len(x) - 1, len(y) - 1), (1, 1, 1))

    pixel = img.load()
    for i in range(len(x) - 1):
        for j in range(len(y) - 1):
            hv = ArrayDicom[i, j]
            pixel[i, j] = hv, hv, hv

    fname = input('Enter Image Name : ')
    imgFormat = input('Enter Image Format : ')

    dirpath = input('Enter folder location with name : ')

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    img.save('{}/{}.{}'.format(dirpath, fname, imgFormat))
    img.show()
    print('\n\tCheck Converted Image in the Folder!\n')

#--------------------------------------------------------
def imageLoad():
    img = nib.load("./nifti/image.nii")
    header = img.header
    print(header)
    img_data = img.get_fdata()
    print(img_data.shape)
    return img_data

def show_slices(slices):
    fig, axes = pyplot.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="none", aspect="equal")

def createSlices():
    imag_data = imageLoad()
    slice_0 = imag_data[1, :, :]
    slice_1 = imag_data[:, 1, :]
    slice_2 = imag_data[:, :, 1]
    show_slices([slice_0, slice_1, slice_2])
    pyplot.suptitle("----: SLICES OF IMAGE :----")

    print(slice_0.shape)
    print(slice_1.shape)
    print(slice_2.shape)
#--------------------------------------------------------
def menu2():
    print('\n 0.Nifti \n 1.Dicom File\n 2.EXIT')
    num = input('\t Enter : ')
    num = int(num)
    return num

def menu():
    print('\n 1. Open File \n 2. Convert to Other Format ')
    print(' 3. Exit ')
    num = input('\t Enter : ')
    num = int(num)
    return num


dcmFile = []
choice = 0
while 1:

    choicee = menu2()


    if choicee == 1:
        choice = menu()
        if choice == 1:
            dcmFile = read_file()

            if dcmFile != None:
                x, y, arr = get_xy_dicomarray(dcmFile)
                show_file(x, y, arr)

        elif choice == 2:
            dcmFile = read_file()

            if dcmFile != None:
                convert_to_other_format(dcmFile)

        elif choice == 3:
            print('\n\t\t GOOD BYE! \n\n')
            break

    elif choicee == 0:
        createSlices()
        print('\n\t\t GOOD BYE!\n\n')
    elif choicee==2:
        print('\n\t\t GOOD BYE!\n\n')
        break
    else:
        print('Error')
    print('\n')
