import os
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
import json

WORKING_DIR = r'D:\jjm'  # Ensure this is the absolute path to avoid issues in IDE
STATE_NAME = 'Maharashtra'


def save_html_from_element(driver, element_id, file_path):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            data_div = driver.find_element(By.ID, element_id)
            html = data_div.get_attribute("outerHTML")
            with open(file_path, 'w', encoding='utf8') as f:
                f.write(html)
            return
        except StaleElementReferenceException as e:
            print(f"StaleElementReferenceException: {e}")
            print("Retrying...")
            retries += 1
            sleep(2)
            driver.refresh()
    print(f"Failed to save HTML from element with ID {element_id} after {max_retries}")


def find_elements(driver, selector_type, selector):
    selector_type = selector_type.lower()

    if selector_type == 'css':
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
    elif selector_type == 'xpath':
        elements = driver.find_elements(By.XPATH, selector)
    elif selector_type == 'id':
        elements = driver.find_elements(By.ID, selector)
    elif selector_type == 'name':
        elements = driver.find_elements(By.NAME, selector)
    elif selector_type == 'class':
        elements = driver.find_elements(By.CLASS_NAME, selector)
    elif selector_type == 'tag':
        elements = driver.find_elements(By.TAG_NAME, selector)
    elif selector_type == 'link_text':
        elements = driver.find_elements(By.LINK_TEXT, selector)
    elif selector_type == 'partial_link_text':
        elements = driver.find_elements(By.PARTIAL_LINK_TEXT, selector)
    else:
        raise ValueError(f"Unsupported selector type: {selector_type}")

    return elements


def click_option(driver, xpath, value):
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath.format(value))))
            driver.execute_script("arguments[0].scrollIntoView(true);", option)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath.format(value))))
            option.click()
            return
        except (StaleElementReferenceException, TimeoutException, WebDriverException) as e:
            print(f"Error clicking option {value}: {e}")
            print(f"XPath of the element: {xpath.format(value)}")
            print("Retrying...")
            retries += 1
            sleep(5)
            driver.refresh()


def strip_whitespace(string):
    return string.strip()


def format_option_text(text):
    return text.replace("'", "\\'")


def click_habitation_link(driver):
    try:
        link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'CPHPage_lblHab')))
        link.click()
    except TimeoutException:
        print("Habitation link not found. Trying again...")
        driver.refresh()
        sleep(2)
        return False
    return True


def create_directory_if_not_exists(directory):
    # directory = re.sub(r'[<>:"/\\|?*]', '', directory)
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_json(obj, filepath, ensure_ascii=False):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf8", errors='ignore') as f:
        json.dump(obj, f, indent=True, ensure_ascii=ensure_ascii)


def _villages(driver, panchayat_dir):
    village_elements = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddVillage")]//option')[1:]
    village_names = [vil.text.strip() for vil in village_elements]
    for index, vil_text in enumerate(village_names):
        village_dir = os.path.join(panchayat_dir, vil_text)
        create_directory_if_not_exists(village_dir)
        write_json(village_names, os.path.join(village_dir, 'vil.json'))

        formatted_vil = format_option_text(vil_text)
        xpath = '//*[contains(@id, "CPHPage_ddVillage")]/option[normalize-space(text())="{}"]'
        click_option(driver, xpath, formatted_vil)
        sleep(1)
        print("village_name", index, vil_text)

        driver.find_element(By.ID, 'CPHPage_btnShow').click()
        sleep(3)

        if not click_habitation_link(driver):
            return

        file_name = os.path.join(village_dir, f'{vil_text}.html')
        save_html_from_element(driver, 'CPHPage_divgrid', file_name)


def _panchayats(driver, block_dir):
    panchayat_elements = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddPanchayat")]//option')[17:]
    panchayat_names = [panc.text.strip() for panc in panchayat_elements]

    for index, panc_text in enumerate(panchayat_names):
        panchayat_dir = os.path.join(block_dir, str(panc_text))
        create_directory_if_not_exists(panchayat_dir)
        write_json(panchayat_names, os.path.join(panchayat_dir, 'panchayat.json'))

        formatted_panc = format_option_text(panc_text)
        xpath = '//*[contains(@id, "CPHPage_ddPanchayat")]/option[normalize-space(text())="{}"]'
        click_option(driver, xpath, formatted_panc)
        sleep(5)
        print("panchayat_name", index, panc_text)

        _villages(driver, panchayat_dir)


def _blocks(driver, district_dir):
    block_elements = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddBlock")]//option')[1:]
    block_names = [blk.text.strip() for blk in block_elements]
    for blk_text in block_names:
        block_dir = os.path.join(district_dir, str(blk_text))
        create_directory_if_not_exists(block_dir)
        write_json(block_names, os.path.join(block_dir, 'block.json'))

        click_option(driver, '//*[contains(@id, "CPHPage_ddBlock")]/option[text()="{}"]'.format(blk_text), blk_text)
        print(blk_text)
        sleep(2)

        _panchayats(driver, block_dir)


def _districts(driver, current_dir):
    state = find_elements(driver, 'xpath', '//*[contains(@id, "CPHPage_ddState")]')[0].text.split('\n')[21:22]
    for item in state:
        item = strip_whitespace(item)
        write_json([state], os.path.join(current_dir, 'state.json'))

        click_option(driver, '//*[contains(@id, "CPHPage_ddState")]/option[text()="{}"]'.format(item), item)
        sleep(3)
        print(item)

        district_elements = driver.find_elements(By.XPATH, '//*[contains(@id, "CPHPage_ddDistrict")]//option')[21:]
        district_names = [dist.text.strip() for dist in district_elements]
        for dist_text in district_names:
            district_dir = os.path.join(current_dir, str(dist_text))
            create_directory_if_not_exists(district_dir)
            write_json(district_names, os.path.join(district_dir, 'district.json'))

            click_option(driver, '//*[contains(@id, "CPHPage_ddDistrict")]/option[text()="{}"]'.format(dist_text),
                         dist_text)
            sleep(2)
            print(dist_text)

            _blocks(driver, district_dir)


def recur_scrape(current_dir):
    try:
        os.makedirs(current_dir, exist_ok=True)
    except PermissionError:
        print("Permission denied: Unable to create directories.")
        return
    options = FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.get("https://ejalshakti.gov.in/JJM/JJM/Public/Profile/VillageProfile.aspx")
    sleep(5)
    driver.maximize_window()

    _districts(driver, current_dir)
    driver.quit()


if __name__ == '__main__':
    current_dir = os.path.join(WORKING_DIR, STATE_NAME)
    recur_scrape(current_dir)
