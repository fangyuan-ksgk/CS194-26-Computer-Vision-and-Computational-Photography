import math
import numpy as np
import matplotlib.pyplot as plt
import skimage
import skimage.transform as sktr
import skimage.io as skio

# User is supposed to pick alignment point before seeing the other image?
def get_points(im1,im2):
    print('Please select 2 points in each image for alignment.')
    plt.imshow(im1)
    p1,p2 = plt.ginput(2)
    #plt.scatter(p1[0],p1[1],c='red',marker='x',linewidths=4.0)
    #plt.scatter(p2[0],p2[1],c='red',marker='x',linewidths=4.0)
    plt.close()
    plt.imshow(im2)
    p3,p4 = plt.ginput(2)
    #plt.scatter(p3[0],p3[1],c='red',marker='x',linewidths=4.0)
    #plt.scatter(p4[0],p4[1],c='red',marker='x',linewidths=4.0)
    plt.close()
    return (p1,p2,p3,p4)

def find_centers(p1, p2):
    cx = np.round(np.mean([p1[0], p2[0]]))
    cy = np.round(np.mean([p1[1], p2[1]]))
    return cx, cy

"This can be verified carefully by studying index & stuff, I have verified it"
def recenter(im,x,y):
    h,w,_ = im.shape
    hpad = int(abs(2*y+1-h))
    wpad = int(abs(2*x+1-w))
    return np.pad(im, [(0 if y>(h-1)/2 else hpad, 0 if y<(h-1)/2 else hpad),
                       (0 if x>(w-1)/2 else wpad, 0 if x<(w-1)/2 else wpad),
                       (0,0)], mode='constant')

def align_image_centers(im1, im2, pts):
    p1, p2, p3, p4 = pts
    h1, w1, b1 = im1.shape
    h2, w2, b2 = im2.shape
    
    cx1, cy1 = find_centers(p1, p2)
    cx2, cy2 = find_centers(p3, p4)

    im1 = recenter(im1, cx1, cy1)
    im2 = recenter(im2, cx2, cy2)
    return im1, im2

# Rescale such that distance between alignment points are the same
def rescale_images(im1,im2,pts):
    p1,p2,p3,p4 = pts
    len1 = np.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
    len2 = np.sqrt((p4[1]-p2[1])**2 + (p4[0]-p3[0])**2)
    dscale = len2/len1
    # rescale to shrink the bigger one to smaller image: Color image / Gray image case
    if len(im1.shape)==3:
        if dscale<1:
            im1 = sktr.rescale(im1,dscale,anti_aliasing=False,channel_axis=2)
        else:
            im2 = sktr.rescale(im2,1./dscale,anti_aliasing=False,channel_axis=2)
    else:
        if dscale<1:
            im1 = sktr.rescale(im1,dscale,anti_aliasing=False)
        else:
            im2 = sktr.rescale(im2,1./dscale,anti_aliasing=False)
    return im1,im2

# we indeed only requires the relative scale and angle of pts remains intact to get smae result for this one
def rotate_im1(im1, im2, pts):
    p1,p2,p3,p4 = pts
    # note that we need to negate on vertical difference because the vertical origin is on TOP
    # thus we negate it to work on the usual xy-axis that we are comportable with
    theta1 = math.atan2(-(p2[1]-p1[1]),p2[0]-p1[0])
    theta2 = math.atan2(-(p4[1]-p3[1]),p4[0]-p3[0])
    dtheta = theta2 - theta1
    im1_rotate = sktr.rotate(im1,dtheta*180/np.pi)
    # or we can choose to rotate on img2 which will be similar
    return im1_rotate

def match_img_size(im1,im2):
    # crop the larger image to fit to smaller image size
    h1,w1,c1 = im1.shape
    h2,w2,c2 = im2.shape
    # one trick here is that when h2-h1 is odd, we use ceil/floor to crop different number of values at start/end
    if h1<h2:
        im2 = im2[int(np.ceil((h2-h1)/2.)):-int(np.floor((h2-h1)/2.)), :, :]
    elif h1>h2:
        im1 = im1[int(np.ceil((h1-h2)/2.)):-int(np.floor((h1-h2)/2.)), :, :]
    if w1<w2:
        im2 = im2[:, int(np.ceil((w2-w1)/2.)):-int(np.floor((w2-w1)/2.)), :]
    elif w2<w1:
        im1 = im1[:, int(np.ceil((w1-w2)/2.)):-int(np.floor((w1-w2)/2.)), :]
    assert im1.shape==im2.shape, 'Shape is not correct'
    return im1,im2


def align_images(im1, im2):
    pts = get_points(im1, im2)
    im1, im2 = align_image_centers(im1, im2, pts)
    # although absolute scale of pts changes, its difference doesn't
    # and the following operation rely only on their difference
    im1, im2 = rescale_images(im1, im2, pts)
    im1  = rotate_im1(im1, im2, pts)
    im1, im2 = match_img_size(im1, im2)
    return im1, im2


if __name__ == "__main__":
    #imname1 = input("Enter image 1: ")
    #imname2 = input("Enter image 2: ")
    imname1 = "11.jpg"
    imname2 = "cx.jpg"
    im1 = skio.imread(imname1)
    im2 = skio.imread(imname2)
    im11,im21 = align_images(im1,im2)
    fig,ax = plt.subplots(nrows=2, ncols=2,figsize=(15,9))
    ax[0,0].imshow(im1)
    ax[0,0].set_title('Original Image 1')
    ax[0,1].imshow(im2)
    ax[0,1].set_title('Original Image 2')
    ax[1,0].imshow(im11)
    ax[1,0].set_title('Aligned Image 1')
    ax[1,1].imshow(im21)
    ax[1,1].set_title('Aligned Image 2')
    fig.tight_layout()
    plt.show()
    skio.imsave('alimg1.jpg',im11)
    skio.imsave('alimg2.jpg',im21)