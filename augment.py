from background import *
from transform import *
from smudge import *

# performs image augmentation 
def augment(x, y):
    fill = int(x[0,0])
    mxR = x.mean()

    x = addSmudge(x, y) 

    x,y,mnDist = transform(x, y, fill)

    if random() < FP_BG:
        x = fpBackground(x, mnDist, mxR)
    else:
        x = changeBackground(x)
    
    x = noise(x)

    return x,y


