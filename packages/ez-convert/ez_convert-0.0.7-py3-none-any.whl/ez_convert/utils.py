import subprocess
import pytesseract
from docx2pdf import convert
from PIL import Image

def make_output_filename(in_path, otype):
    return in_path.rsplit('.', 1)[0] + '.' + otype

def convert_mov_to_mp4(mov_path):
    mp4_path = make_output_filename(mov_path, 'mp4')
    subprocess.run(['ffmpeg', '-i', mov_path, mp4_path])
    return mp4_path

def doc_to_pdf(doc_path):
    pdf_path = make_output_filename(doc_path, 'pdf')
    convert(doc_path, pdf_path)
    return pdf_path

def jpg_to_pdf(input_path):
    # specify output path
    output_path = make_output_filename(input_path, 'pdf')
    # Open the image file
    with Image.open(input_path) as img:
        # Convert and save as PDF
        img.save(output_path, "PDF", resolution=100.0, quality=95)
    return output_path

def jpg_to_txt(input_path):
    # specify output path
    output_path = make_output_filename(input_path, 'txt')
    # open the image file
    with Image.open(input_path) as img:
        text = pytesseract.image_to_string(img)
    # write the text file
    with open(output_path, 'w') as f:
        f.write(text)
    return output_path

def step_to_stl(input_path):
    # specify the output path
    output_path = make_output_filename(input_path, 'stl')
    # open the step file

    # convert the step to stl

    return output_path

def heic_to_jpg(input_path):
    # specify the output path
    output_path = make_output_filename(input_path, 'stl')

    # open the image
    img = Image.open(input_path)

    img.save(output_path, 'jpg', resolution=100.0, quality=95)

