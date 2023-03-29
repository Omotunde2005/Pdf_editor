from werkzeug.utils import secure_filename
import PyPDF2
import asyncio
import os


ALLOWED_EXTENSIONS = {'pdf'}


def verify_file(*args):
    file = args[0]
    function = args[1]
    password = args[2]
    filename = file.filename
    if not os.path.exists('./files'):
        os.mkdir('./files')

    if not os.path.exists('./results'):
        os.mkdir('./results')

    if file and allowed_file(filename):
        filename = secure_filename(filename)
        file.save(os.path.join('./files', filename))
        asyncio.run(function(filename, password))
        return True
    else:
        return False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


async def resize_pdf(*args):
    filename = args[0]
    document = PyPDF2.PdfReader(f'./files/{filename}')
    writer = PyPDF2.PdfWriter()

    for page in document.pages:
        page.compress_content_streams()
        writer.add_page(page)

    with open(f'./results/{filename}_resized.pdf', 'wb') as file:
        writer.write(file)


async def encrypt_pdf(filename, password):
    document = PyPDF2.PdfReader(f'./files/{filename}')
    writer = PyPDF2.PdfWriter()

    for page in document.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(f'./results/{filename}_encrypted.pdf', 'wb') as file:
        writer.write(file)