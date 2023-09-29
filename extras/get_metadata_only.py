import os
import time
import csv
import random
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

## Specify the directory where files will be downloaded
download_directory = "C:\\Users\\nikit\\escraping_hell"

## Create a CSV file for metadata if it doesn't exist
metadata_file = os.path.join(download_directory, "metadata.csv")
metadata_exists = os.path.exists(metadata_file)

## Specify the path to chromedriver.exe
chromedriver_path = "C:\\Users\\nikit\\chromedriver-win32\\chromedriver.exe"

## Create a Chrome service with the specified chromedriver path
chrome_service = ChromeService(executable_path=chromedriver_path)

## Create a Chrome WebDriver instance with custom download settings
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "C:\\Users\\nikit\\escraping_hell"}
chrome_options.add_experimental_option("prefs", prefs)
## Set a custom User-Agent header to further avoid getting IP blocked
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")
# chrome_options.add_experimental_option("prefs", {
#     "download.default_directory": download_directory,
#     "download.prompt_for_download": False,
#     "download.directory_upgrade": True,
#     "safebrowsing.enabled": True
# })

## Create a Chrome WebDriver instance with the specified chromedriver path and options
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

## Open CSV in order to append metadata
with open(metadata_file, mode='a', encoding='utf-8', newline='') as csv_file:
    fieldnames = ['File_Number','Composer', 'Title', 'Genre', 'Difficulty', 'Pages', 'Duration', 'Description', 'Download_Status']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if not metadata_exists:
        writer.writeheader()
    ## Read the URLs from the CSV file
    with open('urls.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        ## Flag to check if login has been done
        login_done = False
        counter = 0
        for index, row in enumerate(csv_reader, start=1):
            counter += 1
            ## Start at URL number you left off 
            if counter > 231:
                break
            url = row['URL']
            ## Open the MuseScore website for the current URL
            driver.get(url)
            ## Perform login if not done already
            if not login_done:
                ## Close privacy popup
                privacy_accept = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))
                privacy_accept.click()
                try:
                    ## Close popup if it appears
                    popup_x = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/article/section/button/svg')))
                    popup_x.click()
                except TimeoutException:
                    ## Handle the case where the popup doesn't appear
                    print("Popup did not appear")
                login_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/header/nav/div[4]/section/button[2]/span')))
                login_button.click()
                ## Simulate typing username
                username_input = WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
                username_input.send_keys('wisife6131')
                ## Simulate typing password
                password_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
                password_input.send_keys('wisife6131')
                login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="user-login-form"]/div/section[1]/button/span')))
                login.click()
                login_done = True
                login_done = True  ## Set the flag to True after logging in 

                        ## Scrape metadata information from the website
            try:
                ## Find elements using their XPATHs
                title_element = driver.find_element(By.XPATH, '/html/body/div/div/section/aside/div[5]/div[2]/section[1]/h3[1]/a')
                ## Extract the text from the elements
                title = title_element.text.strip()
            except NoSuchElementException:
                    try:
                        ## Try the second XPath expression here
                        title_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/aside/div[4]/div[2]/section[1]/h3[1]/a')
                        title = title_element.text.strip()
                    except NoSuchElementException:
                        ## Handle the case when both XPath expressions don't exist
                        title = ""
            try:
                composer_element = driver.find_element(By.XPATH, '/html/body/div/div/section/aside/div[5]/div[2]/section[1]/h3[2]/a')
                composer = composer_element.text.strip()
            except NoSuchElementException:
                    try:
                        composer_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/aside/div[4]/div[2]/section[1]/h3[2]/a')
                        composer = composer_element.text.strip()
                    except NoSuchElementException:
                        composer = ""
            try:
                genre_element = driver.find_element(By.XPATH, '/html/body/div/div/section/aside/div[6]/div[2]/table/tbody/tr[5]/td/div/a')
                genre = genre_element.text.strip()
            except NoSuchElementException:
                    try:
                        genre_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/aside/div[5]/div[2]/table/tbody/tr[5]/td/div/a')
                        genre = genre_element.text.strip()
                    except NoSuchElementException:
                        genre = ""
            try:
                pages_element = driver.find_element(By.XPATH, '/html/body/div/div/section/aside/div[6]/div[2]/table/tbody/tr[1]/td/div')
                pages = pages_element.text.strip()
            except NoSuchElementException:
                    try:
                        pages_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/aside/div[5]/div[2]/table/tbody/tr[1]/td/div')
                        pages = pages_element.text.strip()
                    except NoSuchElementException:
                        pages = ""
            try:    
                duration_element = driver.find_element(By.XPATH, '/html/body/div/div/section/aside/div[6]/div[2]/table/tbody/tr[2]/td/div')
                duration = duration_element.text.strip()
            except NoSuchElementException: 
                    try:
                        duration_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/aside/div[5]/div[2]/table/tbody/tr[2]/td/div')
                        duration = duration_element.text.strip()
                    except NoSuchElementException:
                        duration = ""
            try:
                desc_element = driver.find_element(By.XPATH, '/html/body/div/div/section/aside/div[6]/div[2]/div')
                ## Use Beautiful Soup to replace <br> tags with spaces in the description
                soup = BeautifulSoup(desc_element.get_attribute("innerHTML"), "html.parser")
                desc = " ".join(soup.stripped_strings)
            except NoSuchElementException:
                desc = ""
            try:
                difficulty_element = driver.find_element(By.XPATH, '/html/body/div/div/section/aside/div[4]/div/div[2]')
                difficulty = difficulty_element.text.strip()
            except NoSuchElementException:
                difficulty = ""
            except Exception as e:
                print("Error scraping metadata:", e)

            ## Append the scraped information to the CSV file
            writer.writerow({'File_Number': index, 'Composer': composer, 'Title': title, 'Genre': genre, 'Difficulty': difficulty, 'Pages': pages, 'Duration': duration, 'Description': desc, 'Download_Status': ' '})


## Quit the driver when done
driver.quit()
print("You just got scraped, son!")