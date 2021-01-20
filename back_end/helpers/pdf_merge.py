import os
from PyPDF2 import PdfFileMerger, PdfFileReader
from back_end.app import get_base_path
from back_end.helpers.s3_upload_patents import AmazolnS3


def merge(file_name, folder_name):
    amazon_S3 = AmazolnS3("patents-jerry")
    file_name = str(file_name)[:-4]
    path = "{}/temp_data/pdf/" + file_name + "/" + str(folder_name)
    read_dir = path.format(get_base_path())
    write_path = "{}/temp_data/pdf/" + file_name + "/result"
    write_dir = write_path.format(get_base_path())
    pdfs = [a for a in os.listdir(read_dir) if a.endswith(".pdf")]

    print(pdfs)
    merger = PdfFileMerger()

    if pdfs:
        for pdf in pdfs:
            print(pdf)
            merger.append(PdfFileReader(str(read_dir) + "/" + str(pdf), 'rb'))
        print("start merging pdfs in {} folder".format(folder_name))
        merger.write(str(write_dir) + "/" + folder_name + ".pdf")
        merger.close()
        print("merge complete")

        if folder_name == "result":
            print("uploading to S3")
            if os.path.isfile("{}/temp_data/pdf/{}/result.pdf".format(get_base_path(), file_name)):
                print("file is available")
                with open("{}/temp_data/pdf/{}/result.pdf".format(get_base_path(), file_name), 'rb') as datafile:
                    print("file opened")
                    _result = amazon_S3.upload_pdf(datafile, "{}.pdf".format(file_name))


class PdfMerge:
    async def runner(self, file_name, folder_name):
        await merge(file_name=file_name, folder_name=folder_name)
