import cv2


class Game:    
    def __init__(self):
        pass
    
class ImageWorker:    
    def __init__(self):
        pass

image_1 = cv2.imread('data/no_money 1366 768.png')
image_2 = cv2.imread('data/marketplace 1366 768.png')

img = image_1[1:500, 1:500]


image_2[101:600, 101:600] = img

replicate = cv2.copyMakeBorder(img,50,10,10,10,cv2.BORDER_REPLICATE)
# image_2 = cv2.resize(image_2, (720, 480))
cv2.imshow("result", replicate)
cv2.waitKey(0)
cv2.destroyAllWindows()