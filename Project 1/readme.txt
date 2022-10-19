To run program, you must have the following dependencies installed:
  matplotlib.pyplot
  numpy
  cv2
  os
  sys
  glob

You must also have whatever images you wish to run the program with in the same directory as the main.py file.
The directory with the main.py file should also have a directory called 'Results' and in the 'Results' directory, their should be a directory called 'Frames'
This is important because the program writes all the results into that directory.
The Frames directory holds the intermediate frames used to generate the video outputs, so it should be cleared after every few runs to save space on your system.

To run the program, use the following command:
  python main.py <image1/left> <image2/right> <ratio>

on MAC:
  python3 main.py <image1/left> <image2/right> <ratio>

<image1/left> : the image that would be used for the left side of the image recombination
<image2/right> : the image that would be used for the right side of the image recombination
<ratio> : the ratio represent what percentage of the width both images should be reduced by using seam carving. i.e.
            if <ratio> = 0.25, the output images will have a width that is 25% less than the input images.