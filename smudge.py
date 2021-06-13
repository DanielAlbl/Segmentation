from header import *

# Global Variables
H = W = X = Y = a = b = t = s = c = rx = ry = 0

# 2D gaussian function given global vars
def gauss2D():
    global a, b, s, c
    def f(x, y):
        global s, c
        return exp(-(((x*c+y*s)/a)**2 + ((x*s-y*c)/b)**2)) / 2
    return f

# moves
def moveOffPrint(mask):
    global H, W, X, Y, a, b, rx, ry

    x = X + rx if X < W//2 else X - rx
    y = Y + ry if Y < H//2 else Y - ry

   # while True:
    if mask[y, x] > 127:
        y = y//2 if Y < H//2 else y+(H-y)//2 

    if mask[y, x] > 127:
        x = x//2 if X < W//2 else x+(W-x)//2
        
    X = x - rx if X < W//2 else X + rx
    Y = y - ry if Y < H//2 else Y + ry

def addSmudge(fp, msk):
    global H, W, X, Y, a, b, t, s, c, rx, ry, R

    H,W = fp.shape

    fname = choice(listdir(BACKGROUNDS))
    I = Image.open(BACKGROUNDS + fname)
    I = ImageOps.grayscale(I)
    I = I.resize((W,H))
    bg = np.asarray(I, dtype=int)
    
    X = randint(0, W-1)
    Y = randint(0, H-1)

    a = randint(5, 50)
    b = randint(5, 50)
    t = uniform(0, pi/2)

    s = sin(t)
    c = cos(t)
 
    rx = int(R * max(abs(a*c), abs(b*s)))
    ry = int(R * max(abs(a*s), abs(b*c)))
   
    moveOffPrint(msk)

    f = gauss2D()

    for i in range(max(X-rx, 0), min(X+rx+1, W)):
        for j in range(max(Y-ry, 0), min(Y+ry+1, H)):
            tmp = bg[j, i] * f(i-X, j-Y)
            fp[j, i] = max(min(fp[j, i] - tmp, 255), 0)

    return fp
