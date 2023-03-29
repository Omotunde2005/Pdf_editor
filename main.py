import time
from flask import Flask, render_template, request, url_for, redirect, flash, send_file
from functions import *


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'my_Secret_key'


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/resize', methods=['GET', 'POST'])
def resize():
    if request.method == 'GET':
        return render_template('edit.html')
    file = request.files['file']
    if verify_file(file, resize_pdf, None):
        try:
            return send_file(f'./results/{secure_filename(file.filename)}_resized.pdf', as_attachment=True)
        except FileNotFoundError:
            return redirect(url_for('resize'))
    else:
        flash('You did not upload any file or you uploaded a wrong file format')
        return redirect(url_for('resize'))


@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'GET':
        return render_template('edit.html', request=request)
    file = request.files['file']
    file_path = f'./results/{file.filename}_encrypted.pdf'
    password = request.form.get('password')

    if verify_file(file, encrypt_pdf, password):
        try:
            return send_file(file_path, as_attachment=True)
        except FileNotFoundError:
            return redirect(url_for('encrypt'))
    else:
        flash('You did not upload any file or you uploaded a wrong file format')
        return redirect(url_for('encrypt'))


@app.after_request
def cleanup(response):
    if request.method == 'POST':
        filename = response.headers.get('Content-Disposition').split('=')[1].strip('"')
        first_file_path = f'./files/{filename.split("_")[0]}'
        time.sleep(10)
        if os.path.exists(first_file_path):
            os.remove(first_file_path)

    return response


if __name__ == "__main__":
    app.run(debug=True)