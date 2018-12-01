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