from email.mime import image
import numbers
from tokenize import Double
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

# Read source and mask (if exists) for a given id
def Read(id, path = ""):
    source = plt.imread(path + "image_" + id + ".jpg") / 255
    maskPath = path + "mask_" + id + ".jpg"
    
    if os.path.isfile(maskPath):
        mask = plt.imread(maskPath)
        assert(mask.shape == source.shape), 'size of mask and image does not match'
        mask = (mask > 128)[:, :, 0].astype(int)
    else:
        mask = np.zeros_like(source)[:, :, 0].astype(int)

    return source, mask

def ComputeEngery(input) :
    inSize = input.shape
    energyM = np.zeros((inSize[0], inSize[1]))

    for i in range(inSize[0]) :
        for j in range(inSize[1]) :
            energyM[i][j] = abs(input[i][j] - input[(i - 1) % inSize[0]][j]) + abs(input[i][j] - input[i][(j + 1) % inSize[1]])
    
    return energyM

def ComputeM(energy) :
    inSize = energy.shape
    M = energy.copy()

    for i in range(1, inSize[0]) :
        for j in range(inSize[1]) :

            if ((j - 1) < 0) :
                possible = [M[i - 1][j], M[i - 1][j + 1]]
                M[i][j] = energy[i][j] + min(possible)
                continue

            if ((j + 1) >= inSize[1]) :
                possible = [M[i - 1][j - 1], M[i - 1][j]]
                M[i][j] = energy[i][j] + min(possible)
                continue

            possible = [M[i - 1][j - 1], M[i - 1][j], M[i - 1][j + 1]]
            M[i][j] = energy[i][j] + min(possible)

    return M

def ComputeGradient(input) :
    shiftD = np.roll(input, 1, axis=0)
    shiftL = np.roll(input, -1, axis = 1)

    energy = np.abs(input - shiftD) + np.abs(input - shiftL)
    plt.imsave("Results/test2.jpg", energy)

    return energy

def FindSeam(input) :
    inSize = input.shape
    seam = np.zeros(inSize[0])

    input = input.tolist()
    seam[inSize[0] - 1] = input[inSize[0] - 1].index(min(input[inSize[0] - 1]))

    for i in range(inSize[0] - 1, 0, -1) :
        j = int(seam[i])

        if ((j - 1) < 0) :
            possible = [input[i - 1][j], input[i - 1][j + 1]]
            pIndex = [j, j + 1]
            seam[i - 1] = pIndex[possible.index(min(possible))]
            continue

        if ((j + 1) >= inSize[1]) :
            possible = [input[i - 1][j - 1], input[i - 1][j]]
            pIndex = [j - 1, j]
            seam[i - 1] = pIndex[possible.index(min(possible))]
            continue

        possible = [input[i - 1][j - 1], input[i - 1][j], input[i - 1][j + 1]]
        pIndex = [j - 1, j, j + 1]
        seam[i - 1] = pIndex[possible.index(min(possible))]

    seam = [int(x) for x in seam]
    return seam

def ColorSeem(input, seam) :
    t = input.copy()
    for i in range(input.shape[0]) :
        t[i][seam[i]] = 1
    
    plt.imsave("Results/test.jpg", t)
        
    return t

def SeamCarve(input, ratio):

    original = input.copy()
    # Main seam carving function. This is done in three main parts: 1)
    # computing the energy function, 2) finding optimal seam, and 3) removing
    # the seam. The three parts are repeated until the desired size is reached.

    assert (ratio <= 1), 'Increasing the size is not supported!'

    size = original.shape

    for x in range(int(ratio*size[1])) :
        inSize = input.shape
        
        inputBW = rgb2gray(input)
        energy = ComputeGradient(inputBW)
        M = ComputeM(energy)
        newImage = np.zeros((inSize[0], inSize[1] - 1, 3))
        seam = FindSeam(M) 
        ColorSeem(input, seam)
        for i in range(inSize[0]) :
            newImage[i] = np.concatenate((input[i][:(seam[i])], input[i][(seam[i] + 1):]))

        input = newImage.copy()    

    size = (input.shape[1], input.shape[0])
    return input, size

# print(sys.argv)
# print(len(sys.argv))

if (len(sys.argv) != 4) :
    print("Erorr: Wrong input format")
    print("       Use this format to run the program:")
    print("         main.py <image1> <image2> <ratio>")
    raise SystemExit

# Setting up the input output paths
outputDir = 'Results/'

image_1 = sys.argv[1]
image_2 = sys.argv[2]
ratio = float(sys.argv[3]); # Reduction ratio for height and width

image1 = plt.imread(image_1) / 255
image2 = plt.imread(image_2) / 255

image1_rot = np.rot90(image1)
image2_rot = np.rot90(image2)

# SEAM CARVING/ IMAGE RETARGETING

# WIDTH REDUCTION
output1, size1 = SeamCarve(image1, ratio)
output2, size2 = SeamCarve(image2, ratio)

# Saving the results
plt.imsave(outputDir + "/" + image_1.split('.')[0] + "_result_" + str(size1[0]) + "x" + str(size1[1]) + ".jpg", output1)
plt.imsave(outputDir + "/" + image_2.split('.')[0] + "_result_" + str(size2[0]) + "x" + str(size2[1]) + ".jpg", output2)

# HEIGHT REDUCTION
output1_rot, size1_rot = SeamCarve(image1_rot, ratio)
output2_rot, size2_rot = SeamCarve(image2_rot, ratio)

output1_rev = np.rot90(output1_rot, 3)
output2_rev = np.rot90(output2_rot, 3)

plt.imsave(outputDir + "/" + image_1.split('.')[0] + "_result_" + str(size1_rot[1]) + "x" + str(size1_rot[0]) + ".jpg", output1_rev)
plt.imsave(outputDir + "/" + image_2.split('.')[0] + "_result_" + str(size2_rot[1]) + "x" + str(size2_rot[0]) + ".jpg", output2_rev)