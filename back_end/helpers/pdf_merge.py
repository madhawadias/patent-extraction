import os
from PyPDF2 import PdfFileMerger, PdfFileReader
from back_end.helpers.s3_upload_patents import AmazolnS3
from back_end.app import get_base_path


def merge(file_name):
    amazon_S3 = AmazolnS3("patents-jerry")
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

    if os.path.isfile("{}/temp_data/pdf/{}/result.pdf".format(get_base_path(), file_name)):
        print("file is available")
        with open("{}/temp_data/pdf/{}/result.pdf".format(get_base_path(), file_name), 'rb') as datafile:
            print("file opened")
            _result = amazon_S3.upload_pdf(datafile, "{}.pdf".format(file_name))


class PdfMerge:
    async def runner(file_name):
        await merge(file_name=file_name)
