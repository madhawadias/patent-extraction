import main
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.webdriver.chrome.options import Options
list_of_links = main.list_of_links

patent_results = []

#disabling notifications
options = Options()
options.add_argument("--disable-notifications")

#setting up the chrome driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)

with open('patent-results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["patent-title", "patent-number", "patent-issue-date"])

for link in list_of_links:
    driver.get(link)
    print(driver.title)

    patent_title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "disp_elm_text"))
    )
    patent_title = patent_title.text

    patent_number = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[3]/div"))
    )
    patent_number = patent_number.text

    patent_issue_date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[12]/div[2]"))
    )
    patent_issue_date = patent_issue_date.text

    patent_result = [patent_title, patent_number, patent_issue_date]
    print(patent_result)
    patent_results.append(patent_result)

print(patent_results)


# write it to the csv
with open('patent-results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["patent-title", "patent-number", "patent-issue-date"])
    writer.writerow(patent_results)



