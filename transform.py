from header import *

# scalse an image and its mask randomly
# fills with a given pixel value
def scale(fp, ms, fill):
    s = np.exp(normal(0, 0.35, 1))
    
    h,w = fp.shape

    h_ = int(s * h)
    w_ = int(s * w)
    y = abs((h-h_)) // 2
    x = abs((w-w_)) // 2 

    if s < 1:
        tmp1 = np.full_like(fp, fill)
        tmp1[y:y+h_, x:x+w_] = cv2.resize(fp, (w_, h_), interpolation=cv2.INTER_AREA)

        tmp2 = np.full_like(ms, 0)
        tmp2[y:y+h_, x:x+w_] = cv2.resize(ms, (w_, h_), interpolation=cv2.INTER_AREA)

        return tmp1, tmp2
    else:
        fp = cv2.resize(fp, (w_, h_), interpolation=cv2.NEAREST)
        ms = cv2.resize(ms, (w_, h_), interpolation=cv2.NEAREST)

        return fp[y:y+h, x:x+w], ms[y:y+h, x:x+w]

# Adds gaussian noise to image
def noise(im):
    h,w = im.shape 
    ns = normal(0, NOISE_STD, size=(h,w))
    im += np.rint(ns).astype(int)
    im[im<0] = 0
    im[im>255] = 255
    return im

# performs random translation and rotation on a 
# fingerprint together with it's mask
def transform(fp, ms, fill):
    h,w = fp.shape
   
    # get angle of rotation 
    t = int(np.rint(normal(0, ANGLE_STD, 1)))
    M = cv2.getRotationMatrix2D((w/2, h/2), t, 1)
   
    # rotate fingerprint and mask together
    fp = cv2.warpAffine(fp, M, (w,h), borderValue=fill);
    ms = cv2.warpAffine(ms, M, (w,h), borderValue=0);
     
    # get translation matrix
    x = normal(0, FP_TRANS_STD * w, 1)
    y = normal(0, FP_TRANS_STD * h, 1)
    M = np.float32([[1, 0, x], [0, 1, y]]);
    
    # translate fingerprint and mask
    fp = cv2.warpAffine(fp, M, (w,h), borderValue=fill);
    ms = cv2.warpAffine(ms, M, (w,h), borderValue=0);

    # return fingerprint, mask, and distance of translation for later 
    return fp,ms,sqrt(x*x + y*y)
