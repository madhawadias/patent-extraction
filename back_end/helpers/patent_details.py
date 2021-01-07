from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from back_end.app import get_base_path
import csv
from selenium.webdriver.chrome.options import Options
import datetime



class PatentExtract:

    def __init__(self):
        self.list_of_titles = []
        self.list_of_links = []
        self.chrome_driver_path = "{}/utils/chromedriver".format(get_base_path())
        hi = "hello"
        self.csv_location = "{}/temp_data/".format(get_base_path())
        self.options = Options()
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--headless")

    # open csv for all titles
    # def write_to_csv(self):
    #     with open(self.csv_location, 'w', newline='') as file:
    #         writer1 = csv.writer(file)
    #         writer1.writerow(["patent-titles"])

    # for i in range(2, 6):

    def search_by_examiner(self, text):
        print(text)
        # text1 = self.text
        # print(text1)

        # current_date = datetime.datetime.now()
        # date_str =str(current_date.hour)+str(current_date.minute)+str(current_date.second)+str(current_date.day)+str(current_date.month)+str(current_date.year)
        # filename = str(self.csv_location + text + date_str)
        # with open(filename+".csv", 'w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(["patent-title", "patent-number", "patent-issue-date"])

        driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=self.options)
        driver.get("https://www.freepatentsonline.com/search.html")
        print(driver.title)
        # search the author
        search = driver.find_element_by_id("query_txt")
        # search.send_keys('PEX/"ROTARU, OCTAVIAN"')
        search.send_keys(text)
        submit_btn = driver.find_element_by_name("search")
        submit_btn.click()

        try:
            # getting all titles
            print("Getting titles")
            titles = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@id="results"]/div[2]/div/div/table/tbody/tr/td[3]/a'))
            )
            for value in titles:
                print(value.text)
                self.list_of_titles.append(value.text + "\n")
                self.list_of_links.append(value.get_attribute('href'))
            print(self.list_of_titles)
            print(self.list_of_links)

        finally:
            driver.quit()

    def extract_patent_details(self, text):

        # list_of_links = self.list_of_links
        patent_results = []

        # disabling notifications
        # options = Options()
        # options.add_argument("--disable-notifications")

        # setting up the chrome driver
        driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=self.options)
        #
        # with open(date, 'w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(["patent-title", "patent-number", "patent-issue-date"])

        for link in self.list_of_links:
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

            patent_application_number = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div[11]/div[2]"))
            )
            patent_application_number = patent_application_number.text

            patent_result = [patent_title, patent_number, patent_issue_date, patent_application_number]
            print(patent_result)
            patent_results.append(patent_result)

        print(patent_results)

        # write it to the csv
        current_date = datetime.datetime.now()
        date_str = " " + str(current_date.hour) + str(current_date.minute) + str(current_date.second) + " " + str(
            current_date.day) + str(current_date.month) + str(current_date.year)
        filename = text + date_str
        filepath = str(self.csv_location + filename)
        print(filepath)
        with open(filepath + ".csv", 'w', newline='', encoding= "utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["patent-title", "patent-number", "patent-issue-date", "patent-application-number"])
            for patent_result in patent_results:
                writer.writerow(patent_result)
        filenamecsv = filename+".csv"

        patent_resutls_string = str(patent_results)
        return filenamecsv

        driver.quit()
