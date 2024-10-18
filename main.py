import qrcode
from flask import Flask, render_template, request, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/qrcodes'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def index():
    return render_template("index.html", qr_code_url=None)


@app.route("/generate", methods=['POST'])
def generate_qr():
    data = request.form.get('data')
    filename = request.form.get('filename')

    if not filename.endswith('.png'):
        filename += '.png'

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Creating QR code instance
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # Generating the QR code image
    image = qr.make_image(fill_color='black', back_color='white')
    image.save(filepath)

    # Show the generated QR code and provide a download option
    qr_code_url = url_for('static', filename=f'qrcodes/{filename}')

    return render_template('index.html', qr_code_url=qr_code_url, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
