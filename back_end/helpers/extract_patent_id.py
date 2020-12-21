import pandas as pd
import re
from back_end.helpers.patent_pdf_details import PatentDownload


class ExtractPatentId:

    async def runner(file_name):
        path = 'temp_data/' + str(file_name)
        df = pd.read_csv(path, encoding="ISO-8859-1")
        ids = []
        regex = r"\b\d\d[/]\d\d\d\d\d\d"
        global patentIdCol
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
                    ids.append(patentId)
                    await patent_download_class.runner(patent_id=patentId)
                return "Download Completed!!"
            else:
                return "Please enter a valid CSV file"

        else:
            return "Please enter a non empty CSV file"
