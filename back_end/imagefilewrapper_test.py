

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


import os
from dotenv import load_dotenv

load_dotenv()





global retry
retry = 0


def get_base_path():
    return os.path.dirname(os.path.realpath(__file__))


print(get_base_path())

options = Options()
options.add_argument("--disable-notifications")

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')

options.add_argument("--headless")
options.add_argument('--no-sandbox')

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
PATH = "{}".format(get_base_path())+os.getenv("CHROME_DRIVER_PATH")
print(PATH)



driver = webdriver.Chrome(options=options, executable_path=PATH)



print("Opening Browser")
driver.get("https://portal.uspto.gov/pair/PublicPair")

## enter the application patent number ###
try:
    search = ''
    submit = ''
    patent_id = "09/621925"
    file_name = "test.csv"
    try:
        search = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.ID, "number_id"))
        )
    except Exception as e:
        print(e)
        print("redo 1")
        driver.quit()
        # patent_download_class = PatentDownload()
        # patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)


    search.send_keys(patent_id)

    try:
        submit = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.ID, "SubmitPAIR"))
        )
        time.sleep(3)
    except Exception as e:
        print(e)
        print("redo 2")
        driver.quit()
        # patent_download_class = PatentDownload()
        # patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

    submit.click()
    print("searching for PDFs to the relevant application number")
    time.sleep(5)

    try:
        print("inside first try")
        # time.sleep(5)
        # driver.find_element_by_id("imageFileWrapperId")
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "imageFileWrapperId")))
        # image_file_wrapper = WebDriverWait(driver, 40).until(
        #     EC.presence_of_element_located((By.ID, "imageFileWrapperId"))
        # )
        print("inside first try")
        print(element)
        adminCheckBox = ''
        print("leaving first try")

        try:
            print("inside second try")
            image_file_wrapper = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.ID, "imageFileWrapperId"))
            )
            print("found image file wrapper")
            print(image_file_wrapper)
            time.sleep(10)
            image_file_wrapper.click()

        except Exception as e:
            print(e)
            print("redo 3")
            driver.quit()
            # patent_download_class = PatentDownload()
            # patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

        try:
            adminCheckBox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//td[normalize-space(text())='REM']/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
            )
            time.sleep(2)
            print("REM exist for application number : " + patent_id)
            REM_exist = 1
        except Exception as e:
            print(e)
            print("REM Does not exist for application number : " + patent_id)
            REM_exist = 0
            # patent_download_class = PatentDownload()
            # patent_download_class.patent_pdf(patent_id=patent_id,file_name=file_name)

        if REM_exist == 1:
            try:
                driver.execute_script("arguments[0].click();", adminCheckBox)
            except Exception as e:
                print(e)
                pass

            try:
                download_all_pdf = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="buttonsID"]/a'))
                )
                time.sleep(3)
                path_a = "\\" + file_name[0:-4]
                params = {'behavior': 'allow',
                          'downloadPath': r"{}\temp_data\pdf".format(get_base_path()) + path_a + r"\1"}
                driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
                download_all_pdf.click()
            except Exception as e:
                print(e)
                print("redo 4")
                driver.quit()
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

            try:
                print("Downloading REM PDF")
                driver.get("chrome://downloads/")
                time.sleep(10)
                print("completed downloading pdf REM for application number : " + patent_id)
                driver.back()
                time.sleep(10)
            except Exception as e:
                print(e)
                print("redo 5")
                driver.quit()
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

        try:
            adminCheckBox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//td[normalize-space(text())='AMSB']/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
            )
            time.sleep(2)
            print("AMSB exist for application number : " + patent_id)
            AMSB_exist = 1
        except Exception as e:
            print(e)
            print("AMSB Does not exist for application number : " + patent_id)
            AMSB_exist = 0
            # patent_download_class = PatentDownload()
            # patent_download_class.patent_pdf(patent_id=patent_id,file_name=file_name)

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
            print("CLM exist for application number : " + patent_id)
            CLM_exist = 1
        except Exception as e:
            print(e)
            print("CLM Does not exist for application number : " + patent_id)
            CLM_exist = 0
            # patent_download_class = PatentDownload()
            # patent_download_class.patent_pdf(patent_id=patent_id,file_name=file_name)

        if CLM_exist == 1:
            try:
                driver.execute_script("arguments[0].click();", adminCheckBox)
            except Exception as e:
                print(e)
                pass

        try:
            adminCheckBox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//td[normalize-space(text())='A.NE']/following-sibling::td/following-sibling::td/following-sibling::td/following-sibling::td/descendant::input"))
            )
            time.sleep(3)
            print("A.. exist for application number : " + patent_id)
            A_exist = 1
        except Exception as e:
            print(e)
            print("A.. Does not exist for application number : " + patent_id)
            A_exist = 0
            # patent_download_class = PatentDownload()
            # patent_download_class.patent_pdf(patent_id=patent_id,file_name=file_name)
        if A_exist == 1:
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

        if (A_exist + CLM_exist + AMSB_exist) != 0:
            try:
                download_all_pdf = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="buttonsID"]/a'))
                )
                time.sleep(3)
                path_b = "\\" + file_name[0:-4]
                # params = {'behavior': 'allow', 'downloadPath': r"C:\Users\ASUS\Documents\patent-extract\patent-extraction\back_end\temp_data\pdf"+path_b+r"\2"}
                params = {'behavior': 'allow',
                          'downloadPath': r"{}\temp_data\pdf".format(get_base_path()) + path_b + r"\2"}
                driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
                download_all_pdf.click()
            except Exception as e:
                print(e)
                print("redo 6")
                driver.quit()
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

            try:
                # startDownload = time.time()
                print("Downloading PDF")
                driver.get("chrome://downloads/")
                time.sleep(10)
                # endDownload = time.time()
                print("completed downloading pdfs for application number : " + patent_id)
            except Exception as e:
                print(e)
                print("redo 7")
                driver.quit()
                # patent_download_class = PatentDownload()
                # patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)
        else:
            print("No pdfs to download")
        # try:
        #     startDownload = time.time()
        #     print("Downloading PDF")
        #     paths = WebDriverWait(driver, 7500).until(DownloadWait.every_downloads_chrome)
        #     endDownload = time.time()
        #     print(paths)
        #     print("completed downloading pdfs for application number : " + patent_id)
        #     time.sleep(3)
        # except Exception as e:
        #     print(e)
        #     driver.quit()
        #     patent_download_class = PatentDownload()
        #     patent_download_class.patent_pdf(patent_id=patent_id,file_name=file_name)

    except NoSuchElementException as e:
        print(e)
        print("image file wrapper doesn't exist for the id")
        if retry == 2:
            print("moving to the next id")
            retry = 0
            driver.quit()

        else:
            driver.quit()
            print("re-trying to find image wrapper")
            retry = retry + 1
            # patent_download_class = PatentDownload()
            # patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

finally:
    driver.quit()
