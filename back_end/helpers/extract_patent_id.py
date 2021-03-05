import os

import pandas as pd
import re
from back_end.helpers.patent_pdf_details import PatentDownload

global patentIdCol, progress
progress = "-"


def get_progress():
    return progress


class ExtractPatentId:
    def __init__(self):
        self.regex = r"\b\d\d[/]\d\d\d\d\d\d"

    async def runner(self, file_name, count, b_download_path, a_download_path):
        path = 'back_end/temp_data/' + str(file_name)
        df = pd.read_csv(path, encoding="utf-8")
        regex = self.regex
        global patentIdCol, progress
        progress = "-"
        skipped = []
        patentIdCol = None
        patent_download_class = PatentDownload()

        if (df.shape[0] > 0) and (not df.empty):
            if "patent-application-number" in df.columns:
                patentIdCol = "patent-application-number"
            else:
                for column in df:
                    first_val = df[column].iloc[0]
                    first_val = str(first_val)
                    if re.match(regex, first_val):
                        patentIdCol = column

            if patentIdCol:
                patentIds = df[patentIdCol]
                for patentId in patentIds:
                    if re.match(regex, patentId):
                        await patent_download_class.runner(patent_id=patentId, file_name=file_name)
                        a = [a for a in os.listdir(a_download_path) if a.endswith(".pdf")]
                        b = [a for a in os.listdir(b_download_path) if a.endswith(".pdf")]
                        total_pdfs = list(set(a) | set(b))
                        downloaded_count = len(total_pdfs)
                        progress = int((downloaded_count / int(count)) * 100)
                        if downloaded_count == int(count):
                            break
                    else:
                        skipped.append(patentId)

                if skipped:
                    progress = "-"
                    return skipped
                else:
                    progress = "-"
                    S3_BASE_URL = "https://patents-jerry.s3.us-east-2.amazonaws.com/{}.pdf".format(file_name[:-4])
                    return 'Download Completed!! Get your file from here: <br><a href="{}">{}</a>'.format(S3_BASE_URL,S3_BASE_URL)
            else:
                return "Please enter a valid CSV file"

        else:
            return "Please enter a non empty CSV file"
