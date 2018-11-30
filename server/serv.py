from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from io import BytesIO
import base64
from PIL import Image, ImageDraw

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


@app.route('/')
def index():
    return render_template('index.html')


@io.on('test_img_upload')
def test(data):
    # print(data['data'][23:])
    im = Image.open(BytesIO(base64.b64decode(data['data'][23:])))
    draw = ImageDraw.Draw(im)
    draw.line((0, 0) + im.size, fill=128)
    draw.line((0, im.size[1], im.size[0], 0), fill=128)

    del draw
    buffered = BytesIO()
    im.save(buffered, format="jpeg")
    img_str = base64.b64encode(buffered.getvalue())
    # print(img_str.decode('utf-8'))
    emit('resp', {'data': img_str})


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
