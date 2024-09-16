import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def sanitize_filename(name):
    return re.sub(r'[\/:*?"<>|]', '_', name)


def select_option(driver, element_id, index):
    options = driver.find_elements(By.XPATH, f'//*[@id="{element_id}"]/option')[1:]
    if index < len(options):
        options[index].click()
        time.sleep(5)
    else:
        raise IndexError(f"Index {index} is out of range for element with ID {element_id}.")


def process_villages(driver, dist_name, block_text, panchayat_text):
    village_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddVillage"]/option')[1:]
    for v in range(len(village_options)):
        village_name = sanitize_filename(village_options[v].text)
        village_options[v].click()
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="CPHPage_btnShow"]').click()
        time.sleep(15)

        dir_path = os.path.join(dist_name, block_text, panchayat_text, village_name)
        custom_dir = os.path.join(r"D:\jjm\Maharashtra", dir_path)

        if not os.path.exists(custom_dir):
            os.makedirs(custom_dir)

        custom_path = os.path.join(custom_dir, f"{village_name}.html")
        if not os.path.exists(custom_path):
            html_source = driver.page_source
            with open(custom_path, "w", encoding="utf-8") as file:
                file.write(html_source)


def profile_selector(driver):
    driver.get("https://ejalshakti.gov.in/JJM/JJM/Public/Profile/VillageProfile.aspx")

    select_option(driver, "CPHPage_ddState",11)

    dist_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddDistrict"]/option')[1:]
    for i in range(len(dist_options)):
        dist_name = sanitize_filename(dist_options[i].text)
        select_option(driver, "CPHPage_ddDistrict", i)

        block_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddBlock"]/option')[1:]
        for j in range(len(block_options)):
            block_text = sanitize_filename(block_options[j].text)
            select_option(driver, "CPHPage_ddBlock", j)

            panchayat_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddPanchayat"]/option')[1:]
            for d in range(len(panchayat_options)):
                panchayat_text = sanitize_filename(panchayat_options[d].text)
                select_option(driver, "CPHPage_ddPanchayat", d)

                process_villages(driver, dist_name, block_text, panchayat_text)


def main():
    path = r"/drivers/chromedriver.exe"
    driver = webdriver.Chrome()
    profile_selector(driver)

if __name__ == '__main__':
    main()

