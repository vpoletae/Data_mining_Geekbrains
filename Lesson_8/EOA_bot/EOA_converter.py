import os
import sys
import io

PATH_TO = os.path.dirname(os.path.abspath(__file__))

docs_folder = 'docs'
jpg_folder = 'jpg'
rus_folder = 'RUS'
eng_folder = 'ENG'
archive_folder = 'Archive'

brackets = '\\'

cmd_pdfimages = "\"C:/Program Files/Glyph_Cog/XpdfReader-win64/xpdf-tools-win-4.02/bin64/pdfimages.exe\" -j {} {}"
# cmd_pdfimages = "\"C:/Program Files/ImageMagick-7.0.9-Q16/magick.exe\" convert -density 300 -trim {} -quality 100 {}"
os_pdfimages_start = "cd \"C:/Program Files/Glyph_Cog/XpdfReader-win64/xpdf-tools-win-4.02/bin64\""
cmd_tesseract = "\"C:/Program Files/Tesseract-OCR/tesseract.exe\" {} {} -l {} --psm 1" # adjust lang parameter
os_tesseract_start = "cd \"C:/Program Files/Tesseract-OCR\""

def get_pdf_files():
    '''
    D - takes all files from a given folder, returns a list of pdf files
    I - no
    O - list of filenames with pdf extension
    '''
    files = os.listdir(os.path.join(PATH_TO, docs_folder))
    pdf_files = []
    for file in files:
        if file.endswith('pdf'):
            pdf_files.append(file)
    return pdf_files

def convert_pdf_to_jpg(pdf_files):
    '''
    D - converts pdf-file into several jpg (depends on amount of sheets)
    I - list of filenames with pdf ext.
    O - no. Creates a bunch of jpg-files in initial folder
    '''
    os.system(os_pdfimages_start)
    for file in pdf_files:
        filename, file_ext = os.path.splitext(file)
        cmd_pdfimages_full = cmd_pdfimages.format(os.path.join(PATH_TO, docs_folder, file),
                                                os.path.join(PATH_TO, docs_folder, jpg_folder) + '\\')
        os.system(cmd_pdfimages_full)

def get_jpg_files():
    '''
    D - takes all files from a given folder, returns a list of jpg files
    I - no
    O - list of filenames with jpg extension
    '''
    jpg_files = os.listdir(os.path.join(PATH_TO, docs_folder, jpg_folder))
    return jpg_files

def convert_jpg_to_txt_bilingua(jpg_files):
    '''
    D - converts jpg-file into txt, removes intermediate jpg
    I - list of filenames with jpg ext.
    O - no. Creates a bunch of txt-files in initial folder
    '''
    os.system(os_tesseract_start)
    for file in jpg_files:
        filename, file_ext = os.path.splitext(file)
        lang = 'rus+eng'
        cmd_tesseract_full = cmd_tesseract.format(os.path.join(PATH_TO, docs_folder, jpg_folder, file),
                                        os.path.join(PATH_TO, docs_folder, rus_folder) + '/' + filename + ".txt", lang)
        os.system(cmd_tesseract_full)

def get_txt_files():
    '''
    D - takes all files from a given folder, returns a list of txt files
    I - no
    O - list of filenames with txt extension
    '''
    txt_files = os.listdir(os.path.join(PATH_TO, docs_folder, rus_folder))
    return txt_files

def txt_concatenator(txt_files):
    '''
    D - takes txt files from a given folder, returns concatenated one, removes intermediate
    I - bunch of txt files
    O - concatenated txt file
    '''
    with open(os.path.join(PATH_TO, docs_folder, 'concatenated_file.txt'), 'a', encoding='UTF8') as concat_file:
        for file in txt_files:
            with open(os.path.join(PATH_TO, docs_folder, rus_folder, file), 'r', encoding='UTF8') as read_file:
                data = read_file.read()
                concat_file.write(data)
            # os.remove(os.path.join(PATH, file)) # delete intermediate file

def eoa_convert():
    pdf_files = get_pdf_files()
    convert_pdf_to_jpg(pdf_files)
    jpg_files = get_jpg_files()
    convert_jpg_to_txt_bilingua(jpg_files)
    txt_files = get_txt_files()
    txt_concatenator(txt_files)
