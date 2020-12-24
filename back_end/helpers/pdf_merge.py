import os
from PyPDF2 import PdfFileMerger, PdfFileReader

from back_end.app import get_base_path


def merge(file_name):
    file_name = str(file_name)[:-4]
    path = "{}\\temp_data\\pdf\\" + file_name
    dir = path.format(get_base_path())
    pdfs = [a for a in os.listdir(dir) if a.endswith(".pdf")]

    print(pdfs)
    merger = PdfFileMerger()

    for pdf in pdfs:
        print(pdf)
        merger.append(PdfFileReader(str(dir) + "/" + str(pdf), 'rb'))

    merger.write(str(dir) + "/" + "result.pdf")
    merger.close()


class PdfMerge:
    async def runner(file_name):
        await merge(file_name=file_name)
