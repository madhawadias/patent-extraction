from back_end.helpers.patent_details import PatentExtract

patent_extract_class = PatentExtract()
patent_extract_class.search_by_examiner()
patent_extract_class.extract_patent_details()

print("Done")
