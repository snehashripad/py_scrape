from time import sleep
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException, \
    NoSuchElementException

logging.basicConfig(level=logging.INFO)

def select_option_with_js(driver, dropdown_id, option_text):
    try:
        select_script = f"""
        var dropdown = document.getElementById("{dropdown_id}");
        for (var i = 0; i < dropdown.options.length; i++) {{
            if (dropdown.options[i].text === "{option_text}") {{
                dropdown.selectedIndex = i;
                dropdown.dispatchEvent(new Event('change', {{bubbles: true}}));
                break;
            }}
        }}
        """
        driver.execute_script(select_script)
        logging.info(f"Selected option '{option_text}' from dropdown '{dropdown_id}' using JavaScript")
    except Exception as e:
        logging.error(f"Error selecting option with JavaScript: {e}")

def select_option(driver, dropdown_id, text=None):
    try:
        if text is not None:
            dropdown = driver.find_element(By.ID, dropdown_id)
            select = Select(dropdown)
            select.select_by_visible_text(text)
            logging.info(f"Selected by visible text: {text}")
            return
    except StaleElementReferenceException:
        logging.warning("Stale element reference encountered. Retrying...")
        # Re-fetch the dropdown element and retry the operation
        select_option(driver, dropdown_id, text)
    except Exception as e:
        logging.error(f"Error selecting option: {e}")

def select_dropdown(driver, wait, dropdown_id, text=None):
    dropdown = wait.until(EC.presence_of_element_located((By.ID, dropdown_id)))
    select = Select(dropdown)
    select_option_with_js(driver, dropdown_id, text)

def process_village_data(driver):
    try:
        show_button = driver.find_element(By.ID, "CPHPage_btnShow")
        show_button.click()
        logging.info("Clicked show button")
        habitation_link_clicked = click_habitation_link(driver)
        if habitation_link_clicked:
            logging.info("Clicked on habitation link")
    except Exception as e:
        logging.error(f"Error processing village data: {e}")

def click_habitation_link(driver):
    try:
        link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'CPHPage_lblHab')))
        link.click()
        return True
    except TimeoutException:
        logging.warning("Habitation link not found. Trying again...")
        driver.refresh()
        return False

def main():
    options = FirefoxOptions()
    options.headless = True  # Run browser in headless mode
    driver = None
    try:
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)

        driver.get("https://ejalshakti.gov.in/JJM/JJM/Public/Profile/VillageProfile.aspx")
        sleep(5)

        # Example for selecting state by visible text
        state_text = "Maharashtra"  # Corrected the state name
        select_dropdown(wait, "CPHPage_ddState", text=state_text)

        district_dropdown_id = "CPHPage_ddDistrict"
        district_dropdown = wait.until(EC.presence_of_element_located((By.ID, district_dropdown_id)))
        district_select = Select(district_dropdown)
        sleep(3)

        for district_option in district_select.options[1:]:
            district_text = district_option.text.strip()
            logging.info(f"Attempting to select district: {district_text}")
            select_dropdown(wait, district_dropdown_id, text=district_text)
            sleep(3)

            block_dropdown_id = "CPHPage_ddBlock"
            block_dropdown = wait.until(EC.presence_of_element_located((By.ID, block_dropdown_id)))
            block_select = Select(block_dropdown)

            for block_option in block_select.options[1:]:
                block_text = block_option.text.strip()
                logging.info(f"Attempting to select block: {block_text}")
                select_dropdown(wait, block_dropdown_id, text=block_text)

                panchayat_dropdown_id = "CPHPage_ddPanchayat"
                panchayat_dropdown = wait.until(EC.presence_of_element_located((By.ID, panchayat_dropdown_id)))
                panchayat_select = Select(panchayat_dropdown)

                for panchayat_option in panchayat_select.options[1:]:
                    panchayat_text = panchayat_option.text.strip()
                    logging.info(f"Attempting to select panchayat: {panchayat_text}")
                    try:
                        select_dropdown(wait, panchayat_dropdown_id, text=panchayat_text)

                        # Added sleep interval to wait for villages to load
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CPHPage_ddVillage")))
                        process_village_data(driver)
                    except NoSuchElementException:
                        logging.warning(f"No panchayat option found: {panchayat_text}. Skipping...")
                        continue

    except Exception as e:
        logging.error(f"Error in main function: {e}")
    finally:
        if driver:
            driver.quit()
            logging.info("Driver quit")

if __name__ == "__main__":
    main()
