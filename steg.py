from PIL import Image
import numpy as np
from math import pi
import sys
import os
# from scipy.fftpack import fft, ifft
# import matplotlib.pyplot as plt

class StegMoire:
    def __init__(self, parameter=0.5):
        self.image = None
        self.image_array = np.empty((1,1))
        self.parameter = parameter

    def open(self, filename):
        self.image = Image.open(filename)
        self.image = self.image.convert('RGB')
        self.image_array = np.array(self.image) / 255.0

    def low_contrast(self):
        self.image_array = self.image_array / 255.0 / 8.0 + 0.125

    def phi_1(self):
        # parameter should be from 0.0 to 1.0
        return np.array([[[self.parameter * pi * x + np.cos(y) for c in range(3)] for x in range(self.image.width)] for y in range(self.image.height)])

        # return np.array([[[self.parameter * pi * (x+y) for c in range(3)] for x in range(self.image.width)] for y in range(self.image.height)])
        # return self.profile_inv(np.array(Image.open("example.png").convert('RGB'))/255.0)
        # return np.array([[[self.parameter * pi * x + np.cos(y) for c in range(3)] for x in range(self.image.width)] for y in range(self.image.height)])


    def phi_2(self):
        return self.phi_1() - self.profile_inv(self.image_array)

    def profile(self, phi):
        return 0.5 + 0.5 * np.cos(phi)

    def profile_inv(self, image):
        return np.arccos((image - 0.50) * 2)

    def profile_11(self, phi):
        return 0.25 + 0.125 * np.cos(phi)
  
    def profile_11_inv(self, image):
        return np.arccos((image - 0.25) * 8)

    # L1 is a common image
    def generate_L1(self):
        return self.profile(self.phi_1())

    # L2 is a hidden image
    def generate_L2(self):
        return self.profile(self.phi_2())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 " + sys.argv[0] + " <String:filename> <float:parameter>")
        exit()
    fn = sys.argv[1]
    parameter = sys.argv[2]
    steg = StegMoire(float(parameter))
    steg.open(fn)
    l1 = steg.generate_L1() * 255.0
    Image.fromarray(np.uint8(l1)).save('output/common.png')
    l2 = steg.generate_L2() * 255.0
    Image.fromarray(np.uint8(l2)).save('output/hidden.png')    
    l3 = l1 * l2 / 255.0
    Image.fromarray(np.uint8(l3)).save('output/result.png')    