import os
import time
import re
from selenium import webdriver

from selenium.webdriver.common.by import By

def sanitize_filename(name):
    # Replace invalid characters with an underscore
    return re.sub(r'[\/:*?"<>|]', '_', name)

def profile_selector(driver):
    driver.get(r"https://ejalshakti.gov.in/JJM/JJM/Public/Profile/VillageProfile.aspx")

    # Select the state (Maharashtra in this case)
    driver.find_element(By.XPATH, '//*[@id="CPHPage_ddState"]/option[13]').click()
    time.sleep(5)

    # Loop through each district
    dist_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddDistrict"]/option')[1:]
    for i in range(len(dist_options)):
        dist_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddDistrict"]/option')[1:]
        dist_name = sanitize_filename(dist_options[i].text)
        dist_options[i].click()

        time.sleep(5)

        # Loop through each block within the district
        block_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddBlock"]/option')[1:]
        for j in range(len(block_options)):
            block_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddBlock"]/option')[1:]
            block_text = sanitize_filename(block_options[j].text)
            block_options[j].click()
            time.sleep(5)

            # Loop through each panchayat within the block
            panchayat_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddPanchayat"]/option')[1:]
            for d in range(len(panchayat_options)):
                panchayat_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddPanchayat"]/option')[1:]
                panchayat_text = sanitize_filename(panchayat_options[d].text)
                panchayat_options[d].click()
                time.sleep(5)

                # Loop through each village within the panchayat
                village_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddVillage"]/option')[1:]
                for v in range(len(village_options)):
                    village_options = driver.find_elements(By.XPATH, '//*[@id="CPHPage_ddVillage"]/option')[1:]
                    village_name = sanitize_filename(village_options[v].text)  # Sanitize village name
                    time.sleep(5)
                    village_options[v].click()
                    time.sleep(5)

                    # Click the show button
                    driver.find_element(By.XPATH, '//*[@id="CPHPage_btnShow"]').click()
                    time.sleep(15)

                    # Get the HTML source and save it
                    dir = os.path.join(dist_name, block_text, panchayat_text, village_name)
                    custom_dir = os.path.join(r"D:\jjm\Haryana", dir)

                    # Create directories if they don't exist
                    if not os.path.exists(custom_dir):
                        os.makedirs(custom_dir)

                    # Construct the full path to save the HTML file
                    custom_path = os.path.join(custom_dir, f"{village_name}.html")

                    # Save the HTML file if it doesn't already exist
                    if not os.path.exists(custom_path):
                        html_source = driver.page_source
                        with open(custom_path, "w", encoding="utf-8") as file:
                            file.write(html_source)


def main():
    path = r"/drivers/chromedriver.exe"
    driver = webdriver.Chrome()
    profile_selector(driver)

if __name__ == '__main__':
    main()
