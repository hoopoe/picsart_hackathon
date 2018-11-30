import os
import argparse
import cv2
from models import UNet1024
import torch
from pathlib import Path
from tqdm import tqdm
import numpy as np
from torchvision import transforms
from albumentations import Compose, Normalize
from torch.nn import functional as F

IMG_HEIGHT = 320
IMG_WIDTH = 256

def img_transform(p=1):
  return Compose([
      Normalize(p=1)
  ], p=p)

def cuda(x):
  return x.cuda(async=True) if torch.cuda.is_available() else x

def get_model(model_path, model_type='UNet1024'):

  input_img_resize = (IMG_HEIGHT, IMG_WIDTH)
  model = UNet1024((3, *input_img_resize))

  state = torch.load(str(model_path))
  state = {key.replace('module.', ''): value for key, value in state['model'].items()}
  model.load_state_dict(state)

  if torch.cuda.is_available():
    return model.cuda()

  model.eval()

  return model

def predict(model, input_image, img_transform):
  img = cv2.imread(str(input_image))
  img = np.rollaxis(img, 2, 0) 
  img = torch.tensor(img)
  img = img.float()
  img = img / 255
  img = img.unsqueeze(0)
  with torch.no_grad():
   inputs = cuda(img)
   outputs = model(inputs)
   print(outputs.shape)
   return outputs
            
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  arg = parser.add_argument
  arg('--model_path', type=str, default='runs/unet1024_aug', help='path to model folder')
  arg('--model_type', type=str, default='UNet1024', help='network architecture', choices=['UNet1024'])
  arg('--input_image', type=str, help='input image', default='test.jpg')
  args = parser.parse_args()

  fold = 0
  model = get_model(str(Path(args.model_path).joinpath('model_{fold}.pt'.format(fold=fold))), model_type=args.model_type)

  res = predict(model, args.input_image, img_transform=img_transform(p=1))

  mask = (F.sigmoid(res[0, 0]).data.cpu().numpy())
  mask = (mask * 255).astype(np.uint8)

  cv2.imwrite("mask.png", mask)


