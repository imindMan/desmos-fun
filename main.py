
import cv2
from PIL import Image 
import sys
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY
from PyDesmos import Graph
# Load the image
image = cv2.imread('random.jpg', cv2.IMREAD_GRAYSCALE) # I havent implemented the input image feature yet

# Check if image loaded successfully
if image is None:
    raise ValueError("Image not found or could not be opened.")

# Apply Canny edge detection
edges = cv2.Canny(image, threshold1=100, threshold2=200)


img = Image.fromarray(edges).transpose(Image.Transpose.ROTATE_180)

bm = Bitmap(img, blacklevel=0.5)
plist = bm.trace(
    turdsize=2,
    turnpolicy=POTRACE_TURNPOLICY_MINORITY,
    alphamax=1,
    opticurve=False,
    opttolerance=0.2,
)
with Graph("my graph") as G:
    for curve in plist:
        fs = curve.start_point
        for segment in curve.segments:
            x0, y0 = fs.x, fs.y
            if segment.is_corner:
                x1, y1 = segment.c.x, segment.c.y
                x2, y2 = segment.end_point.x, segment.end_point.y
                G.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x0, x1, y0, y1))
                G.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x1, x2, y1, y2))
            else:
                x1, y1 = segment.c1.x, segment.c1.y
                x2, y2 = segment.c2.x, segment.c2.y
                x3, y3 = segment.end_point.x, segment.end_point.y
                G.append('((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),\
                (1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))' % \
                (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3))
            fs = segment.end_point
