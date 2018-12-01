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
  print('clone_test.jpg - processing')
  mask[mask < 0.75] = 0
  mask[mask >= 0.75] = 255
  mask = mask.astype(np.uint8)
  res = cv2.seamlessClone(src, dst, mask, p, cv2.NORMAL_CLONE)
  print('clone_test.jpg - saving')
  crop_coords = (max(p[0] - 120, 0), max(p[1] - 160, 0))
  im_croped = res[crop_coords[1]:crop_coords[1] + 320, crop_coords[0]:crop_coords[0] + 240]

  cv2.imwrite('static/results/clone_test.jpg', im_croped)
  print('clone_test.jpg - saved')

  print(np.array(res))
  return res#cv2.imread('clone_test.jpg')
  #return new_im + (dst * np.logical_not(new_mask)[:,:,np.newaxis])
