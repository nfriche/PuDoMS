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
from bs4 import BeautifulSoup
from seleniumbase import Driver

def find_part_names_related_text(soup):
    part_names_element = soup.find('th', string=lambda x: x and 'Part names' in x)
    if part_names_element:
        related_td = part_names_element.find_next_sibling('td')
        if related_td:
            return related_td.get_text(strip=True)
    return "Not found"

## Function to add a random break or delay while interacting with website
def random_interact_delay(min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    print(f"Random break: Waiting for {delay:.2f} seconds...")
    time.sleep(delay)

download_directory = "C:\\Users\\nikit\\escraping_hell"
metadata_file = os.path.join(download_directory, "NEW.csv")
metadata_exists = os.path.exists(metadata_file)

chromedriver_path = "C:\\Users\\nikit\\chromedriver-win32\\chromedriver.exe"
chrome_service = ChromeService(executable_path=chromedriver_path)
driver = Driver(uc=True)

with open(metadata_file, mode='a', encoding='utf-8', newline='') as csv_file:
    fieldnames = ['File_Number', 'Instruments']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if not metadata_exists:
        writer.writeheader()

    with open('urls.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        login_done = False
        for index, row in enumerate(csv_reader, start=1):
            if index < 7669:
                continue
            url = row['URL']
            driver.get(url)

            if not login_done:
                privacy_accept = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))
                privacy_accept.click()

                try:
                    popup_x = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/article/section/button/svg')))
                    popup_x.click()
                except TimeoutException:
                    print("Popup did not appear")

                login_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/header/nav/div[4]/section/button[2]/span')))
                login_button.click()
                username_input = WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
                username_input.send_keys('downloadmusescore')
                password_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
                password_input.send_keys('downloadmusescore')
                login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="user-login-form"]/div/section[1]/button/span')))
                login.click()
                login_done = True

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            instruments = find_part_names_related_text(soup)
            # Avoid making too many requests too quickly with random rate limit
            random_interact_delay(3, 7)

            writer.writerow({'File_Number': index, 'Instruments': instruments})

driver.quit()
print("You just got scraped, son!")
