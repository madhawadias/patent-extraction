import pandas as pd
import re


class ExtractPatentId:

    def runner(file_name):
        path = 'temp_data/' + str(file_name)
        df = pd.read_csv(path)
        ids = []
        regex = r"\b\d\d[/]\d\d\d\d\d\d"
        global patentIdCol
        patentIdCol = None

        if df.shape[0] > 0:
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
                return ids
            else:
                return "Please enter a valid CSV file"

        else:
            return "Please enter a non empty CSV file"
