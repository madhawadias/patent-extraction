from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

PATH = "utils/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.freepatentsonline.com/search.html")
print(driver.title)

search = driver.find_element_by_id("query_txt")
search.send_keys('PEX/"ROTARU, OCTAVIAN"')
submit_btn = driver.find_element_by_name("search")
submit_btn.click()

with open('temp_data/patent-result.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["patent-title", "patent-number", "patent-issue-date"])

# for i in range(2, 6):

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

            writer.writerow(patent_result)



    finally:
            driver.quit()

