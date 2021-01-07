import pandas as pd
from back_end.helpers.patent_pdf_details import PatentDownload


class ExtractPatentId:

    def download_pdf(self,file_name):
        path = 'temp_data/' + str(file_name)
        df = pd.read_csv(path, encoding="utf-8")
        patentIds = df["patent-application-number"]
        ids = []
        for patentId in patentIds:
            print(patentId)

            patentId_lowercase = patentId.lower()

            contains_letters = patentId_lowercase.islower()

            if contains_letters == True:
                print("contains a letter")
            else:
                print("does not contain  a letter")
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patentId, file_name)
                ids.append(patentId)