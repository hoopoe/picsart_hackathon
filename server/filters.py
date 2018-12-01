import numpy as np
import cv2

def blur_background(img, mask):
  mask[mask < 0.25] = 0
  mask[mask >= 0.25] = 1
  mask = mask.astype(np.uint8)
  person = img * mask[:,:,np.newaxis]
  kernel = np.ones((5,5), np.float32)/25
  all = cv2.filter2D(img,-1,kernel)
  mask = np.logical_not(mask)
  back = all * mask[:,:,np.newaxis]
  result = back + person
  return result

def change_back(src, dst, mask, p):
  #print('test')
  mask[mask < 0.8] = 0
  mask[mask >= 0.8] = 255
  mask = mask.astype(np.uint8)
  res = cv2.seamlessClone(src, dst, mask, p, cv2.NORMAL_CLONE)
  cv2.imwrite('clone_test.jpg', res)
  print(np.array(res))
  return res#cv2.imread('clone_test.jpg')
  #return new_im + (dst * np.logical_not(new_mask)[:,:,np.newaxis])