import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import sys
import glob

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

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

def ColorSeem(input, seam, name, count) :
    t = input.copy()
    for i in range(input.shape[0]) :
        t[i][seam[i]] = 1
    
    padded = np.pad(t, pad_width=((0, 0), (0, count), (0, 0)))
    plt.imsave(outputDir + 'Frames/' + name + '/frame_' + str(count).zfill(4) + '.jpg', padded)

    return padded

def createVideo(name, size) :
    video = cv2.VideoWriter(outputDir + name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, (size[1], size[0]))

    frames = glob.glob(outputDir + 'Frames/' + name + '/*.jpg')
    frames.sort()
    
    for frame in frames :
        img = cv2.imread(frame)
        video.write(img)
    
    video.release()

def SeamCarve(input, ratio, name):

    original = input.copy()

    assert (ratio <= 1)

    size = original.shape

    for x in range(int(ratio*(size[1]))) :
        inSize = input.shape
        
        inputBW = rgb2gray(input)
        energy = ComputeGradient(inputBW)
        M = ComputeM(energy)
        newImage = np.zeros((inSize[0], inSize[1] - 1, 3))
        seam = FindSeam(M) 
        ColorSeem(input, seam, name, x)

        for i in range(inSize[0]) :
            newImage[i] = np.concatenate((input[i][:(seam[i])], input[i][(seam[i] + 1):]))

        input = newImage.copy()
    
    createVideo(name, size)
    size = (input.shape[1], input.shape[0])
    return input, size

def ImageRecombination( img1, img2) :
    energy = np.abs(rgb2gray(img1) - rgb2gray(img2))
    
    M = ComputeM(energy)
    seam = FindSeam(M)
    
    img1_seam = img1.copy()
    img2_seam = img2.copy()
    
    newImage = np.zeros((img1.shape[0], img1.shape[1], 3))
    imageSeam = newImage.copy()
    
    for i in range(img1_seam.shape[0]) :
        img1_seam[i][seam[i]] = 1
        img2_seam[i][seam[i]] = 1
        newImage[i] = np.concatenate((img1[i][:(seam[i])], img2[i][(seam[i]):]))
        imageSeam[i] = newImage[i]
        imageSeam[i][seam[i]] = 1
        
    plt.imsave(outputDir + "left_seam.jpg", img1_seam)
    plt.imsave(outputDir + "right_seam.jpg", img2_seam)
    plt.imsave(outputDir + "Combined_Result_Seam.jpg", imageSeam)
    
    return newImage

if (len(sys.argv) != 4) :
    print("Erorr: Wrong input format")
    print("       Use this format to run the program:")
    print("         main.py <image1/left> <image2/right> <ratio>")
    raise SystemExit

# Setting up the input output paths
outputDir = 'Results/'

image_1 = sys.argv[1]
image_2 = sys.argv[2]
ratio = float(sys.argv[3]); # Reduction ratio for height and width

img1_path = outputDir + 'Frames/' + image_1.split('.')[0]
img2_path = outputDir + 'Frames/' + image_2.split('.')[0]
img1_h_path = outputDir + 'Frames/' + image_1.split('.')[0] + '_height'
img2_h_path = outputDir + 'Frames/' + image_2.split('.')[0] + '_height'

if not os.path.exists(img1_path) :
    os.mkdir(img1_path)
else :
    files = glob.glob(img1_path + '/*')
    for f in files:
        os.remove(f)

if not os.path.exists(img2_path) :
    os.mkdir(img2_path)
else :
    files = glob.glob(img2_path + '/*')
    for f in files:
        os.remove(f)

# if not os.path.exists(img1_h_path) :
#     os.mkdir(img1_h_path)
# else :
#     files = glob.glob(img1_h_path + '/*')
#     for f in files:
#         os.remove(f)

# if not os.path.exists(img2_h_path) :
#     os.mkdir(img2_h_path)
# else :
#     files = glob.glob(img2_h_path + '/*')
#     for f in files:
#         os.remove(f)

image1 = plt.imread(image_1) / 255
image2 = plt.imread(image_2) / 255

image1_rot = np.rot90(image1)
image2_rot = np.rot90(image2)

# SEAM CARVING/ IMAGE RETARGETING

# WIDTH REDUCTION
output1, size1 = SeamCarve(image1, ratio, image_1.split('.')[0])
output2, size2 = SeamCarve(image2, ratio, image_2.split('.')[0])

# Saving the results
plt.imsave(outputDir + image_1.split('.')[0] + "_result_" + str(size1[0]) + "x" + str(size1[1]) + ".jpg", output1)
plt.imsave(outputDir + image_2.split('.')[0] + "_result_" + str(size2[0]) + "x" + str(size2[1]) + ".jpg", output2)

# # HEIGHT REDUCTION
# output1_rot, size1_rot = SeamCarve(image1_rot, ratio, image_1.split('.')[0] + '_height')
# output2_rot, size2_rot = SeamCarve(image2_rot, ratio, image_2.split('.')[0] + '_height')

# output1_rev = np.rot90(output1_rot, 3)
# output2_rev = np.rot90(output2_rot, 3)

# plt.imsave(outputDir + image_1.split('.')[0] + "_result_" + str(size1_rot[1]) + "x" + str(size1_rot[0]) + ".jpg", output1_rev)
# plt.imsave(outputDir + image_2.split('.')[0] + "_result_" + str(size2_rot[1]) + "x" + str(size2_rot[0]) + ".jpg", output2_rev)

if image1.shape == image2.shape :
    combined = ImageRecombination(image1, image2)
    plt.imsave(outputDir + "Combined_Result.jpg", combined)
else:
    print("Warning: Images cannot be combined because they have different dimensions")