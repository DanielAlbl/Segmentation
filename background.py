from header import *

# rotates a background image and finds the largest inscribed rectangle of 
# the same aspect ratio of a fingerprint image, given by the width and
# height of the image
def rotateCrop(bg, w, h, theta):
    H,W = bg.shape

    theta = radians(theta)
    
    # angle of vector to the top right corner of finger print image
    a1 = atan(h/w) 
    # angle of vector to the bottom right corner of finger print image
    a2 = -a1

    # rotate opposite direction of background
    a1 -= theta
    a2 -= theta
    
    # this ensures for simplicity that both angles 
    # are < 180 degrees
    a1 = (a1 + 2*pi) % pi
    a2 = (a2 + 2*pi) % pi

    # find min distance from the center of the image to a corner of
    # the incribed rectange that would touch the edge of the background
    hy = abs(W/cos(a1))
    hy = min(hy, abs(W/cos(a2)))
    hy = min(hy, abs(H/sin(a1)))
    hy = min(hy, abs(H/sin(a2)))

    a = atan(h/w)

    # find dimensions of inscribed rectangle
    w = int(round(hy*cos(a)))
    h = int(round(hy*sin(a)))

    x = int(round((W - w)/2))
    y = int(round((H - h)/2))

    # rotate background
    M = cv2.getRotationMatrix2D((W/2, H/2), degrees(theta), 1)
    bg = cv2.warpAffine(bg, M, (W,H), borderValue=255);

    # return inscribed rectangle
    return bg[y:y+h, x:x+w]

# Adds a random background image with a random fade and rotation
# The background is also scaled so the fingerprint image fits within
# the bounds of the background image
def changeBackground(fp):
    h,w = fp.shape

    # Get random background image
    fname = choice(listdir(BACKGROUNDS))
    I = Image.open(BACKGROUNDS + fname)
    I = ImageOps.grayscale(I)
    bg = np.array(I)

    # get random angle of rotation
    t = randint(0, 360)

    # rotate and scale the background image
    bg = rotateCrop(bg, w, h, t)
    bg = cv2.resize(bg, (w,h))

    # randomly fade the background 
    r = np.random.exponential(MEAN_FADE, 1)
    if r > 1: r = 1
    bg = bg*r + 255*(1-r)

    # overlay fingerprint on background and return
    sm = fp.astype(int) + bg - 255
    sm[sm < 0] = 0
    sm[sm > 255] = 255

    return sm

# Adds a faded fingerprint image as a background, with a translation and rotation
def fpBackground(fp, mnDist, mean):
    fname = choice(listdir(FINGERPRINTS))
    I = Image.open(FINGERPRINTS + fname)
    bg = np.array(I)
    
    H,W = bg.shape

    # random rotation
    t = randint(0, 360)

    # fill color for transformations
    fill = int(bg[0,0])
    # max value of R (for random fade)
    mxR = FADE_RATIO * bg.mean() / mean

    M = cv2.getRotationMatrix2D((W/2, H/2), t, 1)
    bg = cv2.warpAffine(bg, M, (W,H), borderValue=fill);
  
    # random translation
    x = normal(0, BG_TRANS_STD * W, 1)
    y = normal(0, BG_TRANS_STD * H, 1)
  
    # make sure background print is not more centered than real print
    dist = sqrt(x*x + y*y)
    if dist < mnDist:
        x *= mnDist/dist
        y *= mnDist/dist

    M = np.float32([[1, 0, x], [0, 1, y]]);
    bg = cv2.warpAffine(bg, M, (W,H), borderValue=fill);

    # randomly fade background
    r = np.random.exponential(MEAN_FADE, 1)
    if r > mxR: r = mxR
    bg = bg*r + 255*(1-r)

    # overlay fingerprint on background fingerprint
    sm = fp.astype(int) + bg - 255
    sm[sm < 0] = 0
    sm[sm > 255] = 255

    return sm




