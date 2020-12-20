import pandas as pd
from back_end.helpers.patent_pdf_details import PatentDownload
import time

class ExtractPatentId:

    def runner(file_name):
        path = 'temp_data/' + str(file_name)
        df = pd.read_csv(path, encoding="utf-8")
        patentIds = df["patent-application-number"]
        ids = []
        for patentId in patentIds:
            # print(patentId)
            patent_download_class = PatentDownload()
            patent_download_class.patent_pdf(patentId)

            ids.append(patentId)
        # return ids

    # name of the csv is added below

    runner(file_name="ROTARU, OCTAVIAN 154613 20122020.csv")
