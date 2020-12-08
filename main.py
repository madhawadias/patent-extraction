from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from selenium.webdriver.chrome.options import Options

#disabling notifications
options = Options()
options.add_argument("--disable-notifications")

#setting up the chrome driver 
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=options)
driver.get("https://www.freepatentsonline.com/search.html")
print(driver.title)

#search the author
search = driver.find_element_by_id("query_txt")
search.send_keys('PEX/"ROTARU, OCTAVIAN"')
submit_btn = driver.find_element_by_name("search")
submit_btn.click()

# open csv
with open('patent-results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["patent-title", "patent-number", "patent-issue-date"])

# for i in range(2, 6):



    # get values
    try:

            element = WebDriverWait(driver, 10).until(
                # EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/div[2]/div/div/table/tbody/tr['+str(i)+']/td[3]/a')),
                EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/div[2]/div/div/table/tbody/tr[3]/td[3]/a'))
            )
            element.click()

            # accessing the details
            
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

            patent_result = [patent_title,patent_number,patent_issue_date]
            print(patent_result)

            # write it to the csv
            writer.writerow(patent_result)



    finally:
            driver.quit()







