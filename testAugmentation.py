#!/usr/bin/env python3

from augment import *

# Open files
fname = choice(listdir(FINGERPRINTS))
I = Image.open(FINGERPRINTS + fname)
fp = np.array(I, np.uint8)

# Open corresponding mask
I = Image.open(MASKS + fname[:-3] + "jpg")
ms = np.array(I, np.uint8)

if TEST == "all":
    fp,ms = augment(fp, ms)
elif TEST == "smudge":
    fp = addSmudge(fp, ms) 
elif TEST == "background":
    if random() < FP_BG:
        mxR = fp.mean()
        fp = fpBackground(fp, 0, mxR)
    else:
        fp = changeBackground(fp)
elif TEST == "transform":
    fill = int(fp[0,0])
    fp,ms,mnDist = transform(fp, ms, fill)

fp = fp.astype(np.uint8)
ms = ms.astype(np.uint8)

I = Image.fromarray(fp)
I.save("aug.jpg")

I = Image.fromarray(ms)
I.save("mask.jpg")
