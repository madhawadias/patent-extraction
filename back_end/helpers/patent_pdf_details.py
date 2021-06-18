import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from back_end.app import get_base_path

global retry
retry = 0


class PatentDownload:

    def __init__(self):

        self.options = Options()
        self.options.add_argument("--disable-notifications")

        # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        # self.options.add_argument(f'user-agent={user_agent}')

        # self.options.add_argument("--headless")
        self.options.add_argument('--no-sandbox')

        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        # starting execution time
        # self.chrome_driver_path = "{}/utils/chromedriver".format(get_base_path())
        self.chrome_driver_path = "C:/Users/ASUS/Documents/patent-extract/patent-extraction/utils/chromedriver.exe"
        # search = driver.find_element_by_id("number_id")
        # search.send_keys("14/688463")
        # submit_btn = driver.find_element_by_id("SubmitPAIR")
        # submit_btn.click()
        # time.sleep(5)
        #

    async def runner(self, patent_id, file_name):
        self.patent_pdf(patent_id=patent_id, file_name=file_name)

    def patent_pdf(self, patent_id, file_name):
        global retry
        # options = webdriver.ChromeOptions()
        options = self.options
        path = "{}/temp_data/pdf/{}".format(get_base_path(), file_name[0:-4])
        print("filename :" + file_name[0:-4])
        prefs = {'download.default_directory': path}
        options.add_experimental_option('prefs', prefs)
        print(patent_id)

        print(self.chrome_driver_path)
        # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
        driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=options)
        # driver = webdriver.Chrome(self.chrome_driver_path, chrome_options=self.options)
        driver.get("https://portal.uspto.gov/pair/PublicPair")

        try:
            search = ''
            submit = ''
            try:
                search = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.ID, "number_id"))
                )
            except Exception as e:
                print(e)
                print("redo 1")
                driver.quit()
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

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
                patent_download_class = PatentDownload()
                patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

            submit.click()
            print("searching for PDFs to the relevant application number")
            time.sleep(5)

            try:
                driver.find_element_by_id("imageFileWrapperId")
                adminCheckBox = ''
                try:
                    image_file_wrapper = WebDriverWait(driver, 40).until(
                        EC.presence_of_element_located((By.ID, "imageFileWrapperId"))
                    )
                    time.sleep(3)
                    image_file_wrapper.click()

                except Exception as e:
                    print(e)
                    print("redo 3")
                    driver.quit()
                    patent_download_class = PatentDownload()
                    patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

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
                        params = {'behavior': 'allow', 'downloadPath': r"C:\Users\ASUS\Documents\patent-extract\patent-extraction\back_end\temp_data\pdf"+path_a+r"\1"}
                        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
                        download_all_pdf.click()
                    except Exception as e:
                        print(e)
                        print("redo 4")
                        driver.quit()
                        patent_download_class = PatentDownload()
                        patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

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
                        patent_download_class = PatentDownload()
                        patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

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
                        params = {'behavior': 'allow', 'downloadPath': r"C:\Users\ASUS\Documents\patent-extract\patent-extraction\back_end\temp_data\pdf"+path_b+r"\2"}
                        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
                        download_all_pdf.click()
                    except Exception as e:
                        print(e)
                        print("redo 6")
                        driver.quit()
                        patent_download_class = PatentDownload()
                        patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

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
                        patent_download_class = PatentDownload()
                        patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)
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
                    return
                else:
                    driver.quit()
                    print("re-trying to find image wrapper")
                    retry = retry + 1
                    patent_download_class = PatentDownload()
                    patent_download_class.patent_pdf(patent_id=patent_id, file_name=file_name)

        finally:
            driver.quit()
            return

        # end = time.time()
        # print(f"Runtime of the program is {end - start}")
        # print(f"Runtime of the download is {endDownload - startDownload}")

# PatentDownload().patent_pdf(patent_id="15/617585", file_name="test.csv")
