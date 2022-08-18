from PIL import Image
import cv2 as cv
import os

# Должен быть  установлен пакет poppler
# Для Ubuntu: sudo apt install poppler-utils
# Для Windows лучший вариант: conda install -c conda-forge poppler
from pdf2image import convert_from_path

# Должен быть установлен сторонний пакет Tesseract-OCR
# Для Ubuntu: sudo apt install tesseract-ocr libtesseract-dev tesseract-ocr-rus
# Для Windows Tesseract-OCR отсюда: https://github.com/UB-Mannheim/tesseract/wiki
import pytesseract
from pytesseract import Output
# При необходимости в Windows поправить путь к исполняемому файлу tesseract.exe
if os.name.lower()[:3] == 'win' or os.name.lower()[:3] == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print('Платформа {}, ищем tesseract здесь: {}'.format(os.name.lower()[:3], pytesseract.pytesseract.tesseract_cmd))


# Список символов, которые покрываем маской.
chars_mask_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


# Функция преобразования pdf в изображение
# https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/
def pdf_to_img(doc_file_name, img_file_name):
    #
    images = convert_from_path(doc_file_name)
    img_file_list = []
    for i in range(len(images)):
        file_name = img_file_name + '_page' + str(i) + '.jpg'
        images[i].save(file_name, 'JPEG')
        img_file_list.append(file_name)
    return img_file_list


# Функция распознавания текста на изображении
# TODO: Сделать предобработку картинки перед распознаванием
def img_to_text(img_file_list):
    text_list = []
    for img_file in img_file_list:
        img = Image.open(img_file)
        img.load()
        text_dict = pytesseract.image_to_boxes(img, output_type=Output.DICT, lang="rus")
        text_list.append(text_dict)
    assert len(img_file_list) == len(text_list)
    return text_list


# Функция нарисовать маски по символам из списка
def draw_boxes(img_file_list, text_list):
    for idx, img_file in enumerate(img_file_list):
        #
        curr_img = cv.imread(img_file)
        h, w, _ = curr_img.shape
        for i in range(len(text_list[idx])):
            curr_file_text = text_list[idx]
            for j in range(len(curr_file_text['char'])):
                char = curr_file_text['char'][j]
                left = curr_file_text["left"][j]
                bottom = curr_file_text["bottom"][j]
                right = curr_file_text["right"][j]
                top = curr_file_text["top"][j]
                # print(char, left, bottom, right, top)

                # Чтобы не маскировать номера строк таблицы
                if idx == 0 and left < w*0.15 and top < h*2/3:
                    continue
                if idx > 0 and left < w*0.15:
                    continue
                #
                if char in chars_mask_list:
                    cv.rectangle(curr_img, (left, h - top), (right, h - bottom), (0, 0, 0), -1)
                # while True:
                #     temp_img = cv.resize(curr_img, (800, 600), interpolation=cv.INTER_LINEAR)
                #     cv.imshow('img', temp_img)
                #     if cv.waitKey(25) & 0xFF == ord('q'):
                #         break

        print('Обрабатываем файл {}'.format(img_file))
        cv.imwrite(img_file, curr_img)


# Функция создания нового pdf из обработанных картинок
def img_to_pdf(img_file_list, out_file_name):
    images = [Image.open(f) for f in img_file_list]
    print('Сохраняем результат: {}'.format(out_file_name))
    images[0].save(out_file_name, "PDF", resolution=100.0, save_all=True, append_images=images[1:])




