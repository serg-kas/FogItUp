from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, IndirectObject, NameObject

from pdf2image import convert_from_path

# Словарь замен
replace_dict = {'0': '!!!!!',
                '1': '?????',
                '2': '*',
                '3': '*',
                '4': '*',
                '5': '*',
                '6': '*',
                '7': '*',
                '8': '*',
                '9': '*',
                'PDF': 'DOC',
                'This': 'Этот'
                }


#  Функция замены текста по словарю
def replace_text(content, replace_dict=dict()):
    #
    lines = content.splitlines()  # разбиваем на строки
    result = ""  # результат обработки
    is_text = False
    # Цикл по строкам
    for line in lines:
        # print(line)
        if line == "BT":
            is_text = True

        elif line == "ET":
            is_text = False

        elif is_text:
            # cmd = line[-2:]
            if line[-2:].lower() == 'tj':
                replaced_line = line
                # print(replaced_line.encode('utf-8'))
                print(replaced_line)
                #
                for k, v in replace_dict.items():
                    replaced_line = replaced_line.replace(k, v)
                result += replaced_line + "\n"
            else:
                result += line + "\n"
            continue

        result += line + "\n"
    # Возвращаем результат
    return result


# Функция обработки данных внутри файла (замена по словарю)
def process_data(object, replace_dict):

    data = object.getData()
    # print(data)
    decoded_data = data.decode('utf-8')
    # decoded_data = data.decode('utf-8', errors='ignore')
    # decoded_data = data.decode('windows_1251')
    # decoded_data = data.decode('ISO-8859-5')
    # print(decoded_data)
    #
    replaced_data = replace_text(decoded_data, replace_dict)

    encoded_data = replaced_data.encode('utf-8')
    # encoded_data = replaced_data.encode('windows_1251')

    if object.decodedSelf is not None:
        object.decodedSelf.setData(encoded_data)
    else:
        object.setData(encoded_data)


# Функция обработки документа PDF
# https://localcoder.org/search-and-replace-for-text-within-a-pdf-in-python
def replace_in_pdf(doc_file_name, out_file_name):
    #
    pdf = PdfFileReader(doc_file_name)
    #
    writer = PdfFileWriter()
    # Цикл по страницам в документе
    for page_number in range(0, pdf.getNumPages()):
        print('page_number={}'.format(page_number))
        page = pdf.getPage(page_number)
        print(page.extractText())
        contents = page.getContents()
        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            # print('1. len(contents)={}, type(contents)={}, '.format(len(contents), type(contents)))
            process_data(contents, replace_dict)
        elif len(contents) > 0:
            for obj in contents:
                # print('2. len(contents)={}, type(obj)={}'.format(len(contents), type(obj)))
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    streamObj = obj.getObject()
                    # print('3. streamObj={}'.format(streamObj))
                    process_data(streamObj, replace_dict)

        # Force content replacement
        page[NameObject("/Contents")] = contents.decodedSelf

        writer.addPage(page)
    # Сохраняем результат в выходной файл
    with open(out_file_name, 'wb') as out_file:
        writer.write(out_file)


# Функция преобразования pdf в изображение
# sudo apt get poppler-utils если необходимо
# https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/
def pdf_to_jpg(doc_file_name, out_file_name):
    #
    images = convert_from_path(doc_file_name)
    for i in range(len(images)):
        images[i].save(out_file_name[:-4] + '_page' + str(i) + '.jpg', 'JPEG')






