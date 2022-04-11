"""
При запуске обрабатывает все файлы из папки source_files.
Результат помещает в папку out_files.
Пути к папкам можно задать в аргументах.
"""
import run
import os
import sys
# Обрабатывать файл повторно (если False, то пропускать)
REDO = True
# Допустимые форматы документов
doc_type_list = ['.pdf']


def process(doc_PATH, out_PATH):
    """
    :param doc_PATH: путь к папке с документами
    :param out_PATH: путь к папке с результатами
    :return: None
    """
    # Создать папки для файлов если отсутствуют
    if not (doc_PATH in os.listdir('.')):
        os.mkdir(doc_PATH)
    if not (out_PATH in os.listdir('.')):
        os.mkdir(out_PATH)

    # Создать список файлов для обработки
    doc_files = sorted(os.listdir(doc_PATH))
    out_files = sorted(os.listdir(out_PATH))
    #
    files_to_process = []
    for f in doc_files:
        filename, file_extension = os.path.splitext(f)
        if not (('out_'+f) in out_files) or REDO:
            if file_extension in doc_type_list:
                files_to_process.append(f)

    # Обрабатываем файлы
    for f in files_to_process:
        # Полные пути к файлам
        doc_file_name = os.path.join(doc_PATH, f)
        img_file_name = os.path.join(out_PATH, f[:-4])
        out_file_name = os.path.join(out_PATH, 'out_' + f)
        # Вызов функции обработки
        img_file_list = run.pdf_to_img(doc_file_name, img_file_name)
        text_list = run.img_to_text(img_file_list)
        _ = run.draw_boxes(img_file_list, text_list)
        _ = run.img_to_pdf(img_file_list, out_file_name)
        # Удалим уже не нужные картинки из папки out_PATH
        for img_file in img_file_list:
            os.remove(img_file)

    # Сообщаем сколько файлов обработали
    if len(files_to_process) == 0:
        print('Нет документов для обработки.')
    else:
        print('Обработали документов: {0}'.format(len(files_to_process)))


if __name__ == '__main__':
    doc_PATH = 'doc_files' if len(sys.argv) <= 1 else sys.argv[1]
    out_PATH = 'out_files' if len(sys.argv) <= 2 else sys.argv[2]
    #
    process(doc_PATH, out_PATH)
