from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from io import BytesIO
import base64
from PIL import Image, ImageDraw

import os
import argparse
import cv2
# from models import UNet1024
# import torch
# from pathlib import Path
# from tqdm import tqdm
# import numpy as np
# from torchvision import transforms
# from albumentations import Compose, Normalize
# from torch.nn import functional as F
# from filters import blur_background
# from filters import change_back

# from imageio import imread
# import dlib
# from smart_resize import resize

# set the project root directory as the static folder, you can set others.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
io = SocketIO(app)


@app.route('/')
def index():
    print('Processing: /')
    return render_template('index.html')

@app.route('/background')
def render_background():
    return render_template('back.html')

imgs = {}
@io.on('back_img_upload')
def back_img_acc(data):
    pass

@io.on('main_img_upload')
def main_img_acc(data):
    pass

@io.on('combine')
def combine():
    p = (300, 300)

    # res = change_back(imgs['src'], imgs['back'], imgs['mask'], p)
    # _, buf = cv2.imencode('.jpg', res)
    # img_as_text = base64.b64encode(buf)
    emit('respCombine', {'data': 'clone_test.jpg'})

@io.on('test_img_upload')
def test(data):
    
    emit('resp', {'data': "img_as_text"})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('--model_path', type=str, default='runs/unet1024_aug', help='path to model folder')
    arg('--model_type', type=str, default='UNet1024', help='network architecture', choices=['UNet1024'])
    arg('--input_image', type=str, help='input image', default='test.jpg') #320x240
    arg('--port', type=str, default='8081')
    args = parser.parse_args()


    app.run(host='0.0.0.0', port=args.port)


