from flask import Flask, render_template
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

app = Flask(__name__)
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

  state = torch.load(str(model_path))
  state = {key.replace('module.', ''): value for key, value in state['model'].items()}
  model.load_state_dict(state)

  if torch.cuda.is_available():
    return model.cuda()

  model.eval()

  return model

def predict(model, input_image, img_transform):
  orig_img = cv2.imread(str(input_image)) #320x240
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


@io.on('test_img_upload')
def test(data):
    # print(data['data'][23:])
    im = Image.open(BytesIO(base64.b64decode(data['data'][23:])))
    img_name = 'test.jpg'
    im.save(img_name)

    res = predict(model, img_name, img_transform=img_transform(p=1))

    mask = (F.sigmoid(res[0, 0]).data.cpu().numpy())
    mask = (mask * 255).astype(np.uint8)
    mask = mask[0:0 + IMG_WIDTH, CROP_WIDTH: IMG_WIDTH - CROP_WIDTH]
    cv2.imwrite("mask.png", mask)

    draw = ImageDraw.Draw(im)
    draw.line((0, 0) + im.size, fill=128)
    draw.line((0, im.size[1], im.size[0], 0), fill=128)

    del draw
    #buffered = BytesIO()
    im = cv2.imread('mask.png')
    #im.save(buffered, format="jpeg")
    _, buf = cv2.imencode('.png', im)
    png_as_text = base64.b64encode(buf)
    #img_str = base64.b64encode(buffered.getvalue())
    # print(img_str.decode('utf-8'))
    emit('resp', {'data': png_as_text})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('--model_path', type=str, default='runs/unet1024_aug', help='path to model folder')
    arg('--model_type', type=str, default='UNet1024', help='network architecture', choices=['UNet1024'])
    arg('--input_image', type=str, help='input image', default='test.jpg') #320x240
    args = parser.parse_args()

    fold = 0
    model = get_model(str(Path(args.model_path).joinpath('model_{fold}.pt'.format(fold=fold))), model_type=args.model_type)

    app.run(host='0.0.0.0', port='8081')


