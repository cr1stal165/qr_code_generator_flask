from flask import Flask, render_template, request
import qrcode
import os
from barcode.writer import ImageWriter
from barcode import EAN13

app = Flask(__name__)

picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder


def qrGenerate(self):
    qr = qrcode.QRCode()
    qr.add_data(self)
    qr.make()
    img = qr.make_image()
    img.save("static/pics/qrcode.png")


def barcodeGenerate(numbers):
    my_code = EAN13(numbers, writer=ImageWriter())
    my_code.save("static/pics/barcode")


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        if request.form['code'] == 'qrcode':
            qrGenerate(request.form['net'])
            pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'qrcode.png')
            return render_template('qrcode.html', qr=pic1)
        else:
            barcodeGenerate(request.form['net'])
            pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'barcode.png')
            return render_template('barcode.html', bar=pic2)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
