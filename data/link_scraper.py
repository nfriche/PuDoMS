import os
import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

## Function to add a random break or delay while interacting with the website
def random_interact_delay(min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    #print(f"Random break: Waiting for {delay:.2f} seconds...")
    time.sleep(delay)

## Specify the directory where files will be downloaded
download_directory = "C:/WRITE_YOUR_OWN_DIRECTORY"

## Specify the path to chromedriver.exe
chromedriver_path = "C://WRITE_WHERE_YOUR_CHROMEDRIVER_IS"

## Create a Chrome service with the specified chromedriver path
chrome_service = ChromeService(executable_path=chromedriver_path)

## Create a Chrome WebDriver instance with custom download settings
chrome_options = webdriver.ChromeOptions()
## Set a custom User-Agent header to further avoid getting IP blocked
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

## Create a Chrome WebDriver instance with the specified chromedriver path and options
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

## Open the MuseScore website
driver.get('https://musescore.com/sheetmusic?instrument=2&instrumentation=114&license=to_modify_commercially%2Cto_share%2Cto_use_commercially&recording_type=public-domain')

## Element's XPATH can be found by right-clicking and selecting "Inspect" in Chrome
## Forcing driver to wait mitigates the risk of clicking when the page hasn't fully loaded yet
privacy_accept = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))
privacy_accept.click()

## Initialize CSV file
csv_file_path = "url.csv"
csv_header = ["URL"]

with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    csv_writer.writeheader()

while True:
    try:
        ## Generate JavaScript path for each search result
        search_result_js_paths = []
        for i in range(1, 21):  # Assuming there are 20 search results per page
            js_path = f'document.querySelector("body > div.js-page.react-container > div.b1GqE > section > section > main > div.G0g4K > section > article:nth-child({i}) > div > div.EzJvq > a")'
            search_result_js_paths.append(js_path)

        ## Extract and print the links
        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)
            for js_path in search_result_js_paths:
                link = driver.execute_script(f'return {js_path}.getAttribute("href");')
                csv_writer.writerow({"URL": link})
        
        ## Find the "Next" button
        next_button = driver.find_element(By.CSS_SELECTOR, 'body > div.js-page.react-container > div > section > section > main > div.G0g4K > nav > a.VECGt.oosdZ.HFvdW.Dhs0s.wXNik.A1Z8I.u_VDg > span')
        ## If the button is not enabled, exit the loop
        if not next_button.is_enabled():
            break
        else:
            next_button.click()
            random_interact_delay(2, 5) 
    
    except Exception as e:
        print("Error scraping links:", e)
        break

## Close the browser
driver.quit()
print("Wanna link up?")


