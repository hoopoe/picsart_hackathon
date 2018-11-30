import os
import argparse
import cv2
from models import UNet1024
import torch
from pathlib import Path
from tqdm import tqdm
import numpy as np
# import pandas as pd
from torchvision import transforms
from albumentations import Compose, Normalize

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
  tr = transforms.ToTensor()
  t_img = tr(img)
  with torch.no_grad():
    inputs = cuda(t_img)
    outputs = model(inputs)
    print(outputs.shape)
            
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  arg = parser.add_argument
  arg('--model_path', type=str, default='runs/unet1024_aug', help='path to model folder')
  arg('--model_type', type=str, default='UNet1024', help='network architecture', choices=['UNet1024'])
  arg('--input_image', type=str, help='input image', default='test.png')
  args = parser.parse_args()

  fold = 0
  model = get_model(str(Path(args.model_path).joinpath('model_{fold}.pt'.format(fold=args.fold))),
    model_type=args.model_type)

  predict(model, args.input_image, img_transform=img_transform(p=1))


