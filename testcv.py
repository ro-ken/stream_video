import numpy as np
import cv2

img = cv2.imread('test.png', 0)
print(img)

cv2.imshow('Butterfly', img)
cv2.waitKey(0)
cv2.destroyAllWindows()