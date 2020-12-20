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

        # starting execution time

        self.chrome_driver_path = "{}/utils/chromedriver".format(get_base_path())
        # search = driver.find_element_by_id("number_id")
        # search.send_keys("14/688463")
        # submit_btn = driver.find_element_by_id("SubmitPAIR")
        # submit_btn.click()
        # time.sleep(5)
        #

    def patent_pdf(self):

        driver = webdriver.Chrome(self.chrome_driver_path)
        driver.get("https://portal.uspto.gov/pair/PublicPair")
        start = time.time()

        try:
            try:
                search = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.ID, "number_id"))
                )
            except:
                print("redo")
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf()

            search.send_keys("14/688463")
            submit_btn = driver.find_element_by_id("SubmitPAIR")
            submit_btn.click()
            print("searching for PDFs to the relevant application number")

            try:
                image_file_wrapper = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.ID, "imageFileWrapperId"))
                )
            except:
                print("redo")
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf()

            image_file_wrapper.click()

            try:
                adminCheckBox = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//td[contains(text(),'AMSB')]/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
            except:
                print("redo")
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf()

            adminCheckBox.click();

            try:
                adminCheckBox = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//td[contains(text(),'CLM')]/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
            except:
                print("redo")
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf()

            adminCheckBox.click();

            try:
                adminCheckBox = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//td[contains(text(),'REM')]/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
            except:
                print("redo")
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf()

            adminCheckBox.click();

            time.sleep(50)

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
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf()

            download_all_pdf.click()
            startDownload = time.time()
            print("Downloading PDF")
            paths = WebDriverWait(driver, 7500).until(DownloadWait.every_downloads_chrome)
            endDownload = time.time()
            print(paths)
            print("complete")
            time.sleep(10)

        finally:
            driver.quit()

        end = time.time()
        print(f"Runtime of the program is {end - start}")
        print(f"Runtime of the download is {endDownload - startDownload}")
