from helpers.patent_details import PatentExtract

patent_extract_class = PatentExtract()
patent_extract_class.search_by_examiner()
patent_extract_class.extract_patent_details()

print("Done")





# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import csv
# from selenium.webdriver.chrome.options import Options
#
#
# class patent_extract:
#
#     def __init__(self):
#         self.list_of_titles = []
#         self.list_of_links = []
#         self.chrome_driver_path = "utils/chromedriver"
#         self.csv_location = "temp_data/patent-details.csv"
#         self.options = Options()
#         self.options.add_argument("--disable-notifications")
#
#     #disabling notifications
#
#
#     #setting up the chrome driver
#     # PATH = "utils/chromedriver"
#     # driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=options)
#     # driver.get("https://www.freepatentsonline.com/search.html")
#     # print(driver.title)
#
#
#     #open csv for all titles
#     def write_to_csv(self):
#         with open(self.csv_location, 'w', newline='') as file:
#             writer1 = csv.writer(file)
#             writer1.writerow(["patent-titles"])
#
#     # for i in range(2, 6):
#
#     def search_by_examiner(self):
#
#         with open(self.csv_location, 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["patent-title", "patent-number", "patent-issue-date"])
#
#         driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=self.options)
#         driver.get("https://www.freepatentsonline.com/search.html")
#         print(driver.title)
#         # search the author
#         search = driver.find_element_by_id("query_txt")
#         search.send_keys('PEX/"ROTARU, OCTAVIAN"')
#         submit_btn = driver.find_element_by_name("search")
#         submit_btn.click()
#
#         try:
#                 #getting all titles
#                 titles = WebDriverWait(driver, 10).until(
#                     EC.presence_of_all_elements_located(
#                         (By.XPATH, '//*[@id="results"]/div[2]/div/div/table/tbody/tr/td[3]/a'))
#                 )
#                 for value in titles:
#                     print(value.text)
#                     self.list_of_titles.append(value.text+"\n")
#                     self.list_of_links.append(value.get_attribute('href'))
#                 print(self.list_of_titles)
#                 print(self.list_of_links)
#                 writer.writerow(self.list_of_titles)
#
#                 link_submit = driver.find_elements_by_xpath('//*[@id="results"]/div[2]/div/div/table/tbody/tr[3]/td[3]/a')[0]
#                 link_submit.click()
#
#
#                 # accessing the details
#
#                 patent_title = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.CLASS_NAME, "disp_elm_text"))
#                 )
#                 patent_title = patent_title.text
#
#                 patent_number = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[3]/div"))
#                 )
#                 patent_number = patent_number.text
#
#                 patent_issue_date = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[12]/div[2]"))
#                 )
#                 patent_issue_date = patent_issue_date.text
#
#                 patent_result = [patent_title,patent_number,patent_issue_date]
#                 print(patent_result)
#
#                 # write it to the csv
#                 with open('patent-results.csv', 'w', newline='') as file:
#                     writer = csv.writer(file)
#                     writer.writerow(["patent-title", "patent-number", "patent-issue-date"])
#                     writer.writerow(patent_result)
#
#
#
#         finally:
#                 driver.quit()
#
#
#
#
#
#
#
#
#
#
#
