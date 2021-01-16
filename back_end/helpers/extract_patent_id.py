import pandas as pd
import re
from back_end.helpers.patent_pdf_details import PatentDownload


class ExtractPatentId:
    def __init__(self):
        self.regex = r"\b\d\d[/]\d\d\d\d\d\d"

    async def runner(self, file_name):
        path = 'back_end/temp_data/' + str(file_name)
        df = pd.read_csv(path, encoding="utf-8")
        regex = self.regex
        global patentIdCol
        skiped = []
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
                    else:
                        skiped.append(patentId)

                if skiped:
                    return skiped
                else:
                    S3_BASE_URL = "https://patents-jerry.s3.us-east-2.amazonaws.com/{}.pdf".format(file_name[:-4])
                    return "Download Completed!!" + " Get your file from here: " + S3_BASE_URL
            else:
                return "Please enter a valid CSV file"

        else:
            return "Please enter a non empty CSV file"
