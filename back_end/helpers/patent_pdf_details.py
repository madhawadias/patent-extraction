from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from back_end.app import get_base_path
from chrome_downlaod import DownloadWait
# import csv
# from selenium.webdriver.chrome.options import Options
import time

#starting execution time
start = time.time()

chrome_driver_path = "{}/utils/chromedriver".format(get_base_path())

driver = webdriver.Chrome(chrome_driver_path)
driver.get("https://portal.uspto.gov/pair/PublicPair")

# search = driver.find_element_by_id("number_id")
# search.send_keys("14/688463")
# submit_btn = driver.find_element_by_id("SubmitPAIR")
# submit_btn.click()
# time.sleep(5)
#
try:

    search = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID,"number_id"))
    )
    search.send_keys("14/688463")
    submit_btn = driver.find_element_by_id("SubmitPAIR")
    submit_btn.click()

    image_file_wrapper = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, "imageFileWrapperId"))
    )
    image_file_wrapper.click()

    select_all_rows = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, "selectallrows"))
    )
    select_all_rows.click()

    download_all_pdf = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="buttonsID"]/a'))
    )
    download_all_pdf.click()
    startDownload = time.time()
    paths = WebDriverWait(driver,7200).until(DownloadWait.every_downloads_chrome)
    endDownload = time.time()
    print(paths)
    print("complete")
    time.sleep(10)

finally:
    driver.quit()

end = time.time()
print(f"Runtime of the program is {end - start}")
print(f"Runtime of the download is {endDownload - startDownload}")








