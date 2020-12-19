from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from back_end.app import get_base_path
from back_end.helpers.chrome_download import DownloadWait
from selenium.webdriver.chrome.options import Options
# import csv
# from selenium.webdriver.chrome.options import Options
import time


class PatentDownload:

    def __init__(self):

        # options = Options()
        # options.add_argument("--disable-notifications")
        # options.add_argument("--headless")

        #starting execution time


        self.chrome_driver_path = "{}/utils/chromedriver".format(get_base_path())
        # search = driver.find_element_by_id("number_id")
        # search.send_keys("14/688463")
        # submit_btn = driver.find_element_by_id("SubmitPAIR")
        # submit_btn.click()
        # time.sleep(5)
        #


    def patent_pdf(self,patent_id):

        print(patent_id)

        driver = webdriver.Chrome(self.chrome_driver_path)
        driver.get("https://portal.uspto.gov/pair/PublicPair")
        start = time.time()

        try:
            try:
                search = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.ID,"number_id"))
                )
            except:
                print("redo")
                driver.quit()
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id)


            search.send_keys(patent_id)

            try:
                submit = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.ID, "SubmitPAIR"))
                )
            except:
                print("redo")
                driver.quit()
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id)

            submit.click()
            print("searching for PDFs to the relevant application number")


            try:
                image_file_wrapper = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.ID, "imageFileWrapperId"))
                )
            except:
                print("redo")
                driver.quit()
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id)

            image_file_wrapper.click()


            try:
                adminCheckBox = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//td[contains(text(),'AMSB')]/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
                print("AMSB exisit for application number : "+ patent_id)
                AMSB_exist = 1
            except:
                print("AMSB Does not exisit for application number : "+ patent_id)
                AMSB_exist = 0
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id)

            if AMSB_exist == 1:
                adminCheckBox.click();




            try:
                adminCheckBox = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//td[contains(text(),'CLM')]/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
                print("CLM exisit for application number : "+ patent_id)
                CLM_exist = 1
            except:
                print("CLM Does not exisit for application number : "+ patent_id)
                CLM_exist = 0
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id)

            if CLM_exist == 1:
                adminCheckBox.click();

            try:
                adminCheckBox = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//td[contains(text(),'REM')]/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
                print("REM exisit for application number : "+ patent_id)
                REM_exist = 1
            except:
                print("REM Does not exisit for application number : "+ patent_id)
                REM_exist = 0
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id)
            if REM_exist == 1:
                adminCheckBox.click();

            time.sleep(5)

            # try:
            #     select_all_rows = WebDriverWait(driver, 40).until(
            #         EC.presence_of_element_located((By.ID, "selectallrows"))
            #     )
            # except:
            #     print("redo")
            #     patent_pdf()
            #
            # select_all_rows.click()
            # print("selecting all PDFs")


            try:
                download_all_pdf = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="buttonsID"]/a'))
                )

            except:
                print("redo")
                driver.quit()
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id)

            download_all_pdf.click()
            startDownload = time.time()
            print("Downloading PDF")
            paths = WebDriverWait(driver,7500).until(DownloadWait.every_downloads_chrome)
            endDownload = time.time()
            print(paths)
            print("completed downloading pdfs for application number : " + patent_id)
            time.sleep(3)

        finally:
            driver.quit()

        end = time.time()
        print(f"Runtime of the program is {end - start}")
        print(f"Runtime of the download is {endDownload - startDownload}")












