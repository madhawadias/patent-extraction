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

    async def runner(self, patent_id):
        self.patent_pdf(patent_id=patent_id)

    def patent_pdf(self, patent_id):

        print(patent_id)
        print(self.chrome_driver_path)
        driver = webdriver.Chrome(self.chrome_driver_path)
        driver.get("https://portal.uspto.gov/pair/PublicPair")
        start = time.time()

        try:
            try:
                search = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.ID, "number_id"))
                )
            except Exception as e:
                print(e)
                print("redo")
                driver.quit()
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id)

            search.send_keys(patent_id)

            try:
                submit = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.ID, "SubmitPAIR"))
                )
                time.sleep(3)
            except Exception as e:
                print(e)
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
                time.sleep(3)
                image_file_wrapper.click()
            except Exception as e:
                print(e)
                print("redo")
                driver.quit()
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id)

            try:
                adminCheckBox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//td[normalize-space(text())='AMSB']/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
                time.sleep(2)
                print("AMSB exisit for application number : " + patent_id)
                AMSB_exist = 1
            except Exception as e:
                print(e)
                print("AMSB Does not exisit for application number : " + patent_id)
                AMSB_exist = 0
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id)

            if AMSB_exist == 1:
                try:
                    driver.execute_script("arguments[0].click();", adminCheckBox)
                except Exception as e:
                    print(e)
                    pass

            try:
                adminCheckBox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//td[normalize-space(text())='CLM']/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
                time.sleep(2)
                print("CLM exisit for application number : " + patent_id)
                CLM_exist = 1
            except Exception as e:
                print(e)
                print("CLM Does not exisit for application number : " + patent_id)
                CLM_exist = 0
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id)

            if CLM_exist == 1:
                try:
                    driver.execute_script("arguments[0].click();", adminCheckBox)
                except Exception as e:
                    print(e)
                    pass

            try:
                adminCheckBox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//td[normalize-space(text())='REM']/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
                )
                time.sleep(3)
                print("REM exisit for application number : " + patent_id)
                REM_exist = 1
            except Exception as e:
                print(e)
                print("REM Does not exisit for application number : " + patent_id)
                REM_exist = 0
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id)
            if REM_exist == 1:
                try:
                    driver.execute_script("arguments[0].click();", adminCheckBox)
                except Exception as e:
                    print(e)
                    pass

            time.sleep(2)

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
                time.sleep(3)
                download_all_pdf.click()

            except Exception as e:
                print(e)
                print("redo")
                driver.quit()
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id)

            try:
                startDownload = time.time()
                print("Downloading PDF")
                paths = WebDriverWait(driver, 7500).until(DownloadWait.every_downloads_chrome)
                endDownload = time.time()
                print(paths)
                print("completed downloading pdfs for application number : " + patent_id)
                time.sleep(3)
            except Exception as e:
                print(e)


        finally:
            driver.quit()

        end = time.time()
        print(f"Runtime of the program is {end - start}")
        print(f"Runtime of the download is {endDownload - startDownload}")
