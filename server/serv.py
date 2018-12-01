from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from io import BytesIO
import base64
from PIL import Image, ImageDraw
import cv2

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
from filters import blur_background
from filters import change_back

from imageio import imread
import dlib
from smart_resize import resize

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
io = SocketIO(app)

model = 'undefined'


IMG_HEIGHT = 320
IMG_WIDTH = 256
CROP_WIDTH = 8

def img_transform(p=1):
  return Compose([
      Normalize(p=1)
  ], p=p)

def cuda(x):
  return x.cuda(async=True) if torch.cuda.is_available() else x

def get_model(model_path, model_type='UNet1024'):

  input_img_resize = (IMG_HEIGHT, IMG_WIDTH)
  model = UNet1024((3, *input_img_resize))

  if torch.cuda.is_available():
    state = torch.load(str(model_path))
  else:
    state = torch.load(str(model_path), 'cpu')
  state = {key.replace('module.', ''): value for key, value in state['model'].items()}
  model.load_state_dict(state)

  if torch.cuda.is_available():
    return model.cuda()

  model.eval()

  return model

def predict(model, input_image, img_transform):
  orig_img = input_image #cv2.imread(str(input_image)) #320x240
  img = cv2.copyMakeBorder(orig_img,0,0,CROP_WIDTH,CROP_WIDTH,cv2.BORDER_CONSTANT,value=(0,0,0))
  img = np.rollaxis(img, 2, 0) 
  img = torch.tensor(img)
  img = img.float()
  img = img / 255
  img = img.unsqueeze(0)
  with torch.no_grad():
   inputs = cuda(img)
   outputs = model(inputs)
   return outputs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results/{path:filename}')
def send_file(filename):
    print('Processing: /results/' + filename)
    return send_from_directory('results', filename)

@app.route('/background')
def render_background():
    return render_template('back.html')

imgs = {}
@io.on('back_img_upload')
def back_img_acc(data):
    im = cv2.cvtColor(imread(BytesIO(base64.b64decode(data['data'][23:]))), cv2.COLOR_RGB2BGR)
    imgs['back'] = im

@io.on('main_img_upload')
def main_img_acc(data):
    im = cv2.cvtColor(imread(BytesIO(base64.b64decode(data['data'][23:]))), cv2.COLOR_RGB2BGR)

    if np.shape(im) != (320, 240, 3):
        im = resize(im)
    res = predict(model, im, img_transform=img_transform(p=1))
    mask = (F.sigmoid(res[0, 0]).data.cpu().numpy())
    # mask = (mask * 255).astype(np.uint8)
    mask = mask[0:0 + IMG_HEIGHT, CROP_WIDTH: IMG_WIDTH - CROP_WIDTH]
    imgs['src'] = im
    imgs['mask'] = mask

@io.on('combine')
def combine():
    p = (300, 300)

    res = change_back(imgs['src'], imgs['back'], imgs['mask'], p)
    # _, buf = cv2.imencode('.jpg', res)
    # img_as_text = base64.b64encode(buf)
    emit('respCombine', {'data': 'clone_test.jpg'})

@io.on('test_img_upload')
def test(data):
    # print(data['data'][23:])
    im = cv2.cvtColor(imread(BytesIO(base64.b64decode(data['data'][23:]))), cv2.COLOR_RGB2BGR)

    if np.shape(im) != (320, 240, 3):
        im = resize(im)
    res = predict(model, im, img_transform=img_transform(p=1))
    mask = (F.sigmoid(res[0, 0]).data.cpu().numpy())
    # mask = (mask * 255).astype(np.uint8)
    mask = mask[0:0 + IMG_HEIGHT, CROP_WIDTH: IMG_WIDTH - CROP_WIDTH]
    filtered = blur_background(im, mask) #todo: return
    _, buf = cv2.imencode('.jpg', filtered)
    img_as_text = base64.b64encode(buf)
    emit('resp', {'data': img_as_text})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('--model_path', type=str, default='runs/unet1024_aug', help='path to model folder')
    arg('--model_type', type=str, default='UNet1024', help='network architecture', choices=['UNet1024'])
    arg('--input_image', type=str, help='input image', default='test.jpg') #320x240
    arg('--port', type=str, default='8081')
    args = parser.parse_args()

    fold = 0
    model = get_model(str(Path(args.model_path).joinpath('model_{fold}.pt'.format(fold=fold))), model_type=args.model_type)

    app.run(host='0.0.0.0', port=args.port)


