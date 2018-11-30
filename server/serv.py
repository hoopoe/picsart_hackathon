from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from io import BytesIO
import base64
from PIL import Image, ImageDraw

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
io = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@io.on('test_img_upload')
def test(data):
    print(data['data'][23:])
    im = Image.open(BytesIO(base64.b64decode(data['data'][23:])))
    draw = ImageDraw.Draw(im)
    draw.line((0, 0) + im.size, fill=128)
    draw.line((0, im.size[1], im.size[0], 0), fill=128)

    del draw
    buffered = BytesIO()
    im.save(buffered, format="jpeg")
    img_str = base64.b64encode(buffered.getvalue())
    print(img_str.decode('utf-8'))
    emit('resp', {'data': img_str})


if __name__ == '__main__':
    app.run()
