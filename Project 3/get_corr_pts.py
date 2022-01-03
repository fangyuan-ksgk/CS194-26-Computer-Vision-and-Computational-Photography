import math
import numpy as np
import matplotlib.pyplot as plt
import skimage as sk
import skimage.transform as sktr
import skimage.io as skio

if __name__ == "__main__":
    img1 = skio.imread('alimg1.jpg')
    img2 = skio.imread('alimg2.jpg')
    plt.imshow(img1)
    print('Select eyes')
    eyes = plt.ginput(8)
    print('Select eyebrows')
    eyebrow = plt.ginput(6)
    print('Select nose')
    nose = plt.ginput(4)
    print('Select mouth')
    mouth = plt.ginput(6)
    print('Select face')
    face = plt.ginput(9)
    pts1 = {'eyes':eyes,'eyebrows':eyebrow,'nose':nose,'mouth':mouth,'face':face}
    plt.close()
    plt.imshow(img2)
    print('Select eyes')
    eyes = plt.ginput(8)
    print('Select eyebrows')
    eyebrow = plt.ginput(6)
    print('Select nose')
    nose = plt.ginput(4)
    print('Select mouth')
    mouth = plt.ginput(6)
    print('Select face')
    face = plt.ginput(9)
    pts2= {'eyes':eyes,'eyebrows':eyebrow,'nose':nose,'mouth':mouth,'face':face}
    plt.close()
    #np.save('alimg1_pts',pts1)
    np.save('alimg2_pts',pts2)
    