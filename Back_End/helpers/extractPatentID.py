import pandas as pd

class ExtractPatentId:

    def runner(file_name):
        path = 'temp_data/' + str(file_name)
        df = pd.read_csv(path)
        patentIds = df["patent-application-number"]
        ids = []
        for patentId in patentIds:
            ids.append(patentId)
        return ids
