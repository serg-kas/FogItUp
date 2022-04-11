"""
При запуске обрабатывает все файлы из папки source_files.
Результат помещает в папку out_files добавляя к имени файла "out_".
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
        # print(f, filename, file_extension)
        if not (('out_'+f) in out_files) or REDO:
            if file_extension in doc_type_list:
                files_to_process.append(f)

    # Обрабатываем файлы
    for f in files_to_process:
        # Полные пути к файлам
        doc_file_name = os.path.join(doc_PATH, f)
        out_file_name = os.path.join(out_PATH, 'out_' + f)
        # Вызов функции обработки
        # _ = run.replace_in_pdf(doc_file_name, out_file_name)
        _ = run.pdf_to_jpg(doc_file_name, out_file_name)

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
