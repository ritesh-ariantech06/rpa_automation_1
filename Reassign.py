import logging
import os
import ssl
import glob
import urllib3
import json
import requests
import time
import http.client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)

logging.basicConfig(
    filename='LeadReassign.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login_to_website(driver, selenium_url, username, password):
    """Log in to the website."""
    driver.get(selenium_url)
   
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='username']"))
    ).send_keys(username)
    logging.info("Entered username.")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//*[@id='password']"))
    ).send_keys(password)
    logging.info("Entered password.")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='Login']"))
    ).click()
    logging.info("Clicked login button.")

    time.sleep(5)

   
def navigate_to_cxp_app(driver):
    """Navigate to CXP app - separate function for reusability"""
    try:
        # Try to find app launcher
        app_launcher_xpath = "//button[@title='App Launcher']"
        app_launcher = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, app_launcher_xpath))
        )
        app_launcher.click()
        time.sleep(5)
        print("app launcher clicked")
        
        cxp_app_xpath = "//p[text()='CXP Lightning']"
        cxp_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, cxp_app_xpath))
        )
        
        if cxp_element.is_displayed():
            print("cxp app is displayed")
            cxp_element.click()
            time.sleep(5)
            return True
        else:
            print("cxp app is not displayed")
            return False
            
    except Exception as e:
        print(f"Error navigating to CXP app: {e}")
        return False

# login_done = False

def process_emails(output_directory, driver):
    try:
            
        output_directory = r"C:\Users\WIN10\Desktop\project\FinalPrepod\tempassign"

        json_files = glob.glob(os.path.join(output_directory, '*.json'))
        processed_files = set()

        while True:
            json_files = glob.glob(os.path.join(output_directory, "*.json"))
            new_files = [f for f in json_files if f not in processed_files]

            if not new_files:
                print("⏳ No new files. Waiting...")
                time.sleep(5)
                continue

            new_files.sort(key=os.path.getmtime)  
            print("fcdkfkddkb q ata ch gya ")

            for json_file in new_files:
                    print(f"📄 Processing: {json_file}")
                    processed_files.add(json_file)

                    with open(json_file, 'r') as f:
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            print(f"❌ Error decoding JSON in file: {json_file}")
                            continue

                    print("Data inside file:")
                    print(data)

                    if isinstance(data, dict):
                        data = [data]

                    failed_followups = set()

                    for index, lead_data in enumerate(data):
                        print(f"🔁 Processing lead {index + 1}/{len(data)}: {lead_data.get('lead_id')}")

                    for entry in data:
                        try:   
                            lead_id =(entry.get('lead_id') or '').strip()
                            email= (entry.get('owner_email') or '').strip()
                            url = (entry.get('url') or '').strip()

                            if not lead_id or not email:
                                logging.warning(f"Skipping entry with missing lead_id or email: {entry}")
                                continue

                            print(f"✅ Processing task for: {lead_id}")
                            time.sleep(5)
                            print("code yaha tak pahucha ")
                            try:
                                driver.switch_to.window(driver.window_handles[0])
                                url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/00QVc00000CkgsSMAR/mustafa-shayyed"
                                driver.get(url)
                                print(f"Opened URL: {url}")
                                time.sleep(10)
                            except Exception as e:
                                print("Error opening URL:", e)
                                failed_followups.add(lead_id)
                                continue

                            try:
                                change_owner_btn = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Change Owner']"))
                                )
                                driver.execute_script("arguments[0].click();", change_owner_btn)
                                time.sleep(3)
                                print("Clicked Change Owner button using title-based XPath.")
                            except Exception as e:
                                print("❌ Method 1 failed:", e)

                            xpaths = [
                                "//a[contains(@aria-label, 'Select New Owner')]",
                                "//a[@class='entityMenuTrigger slds-button slds-button--icon slds-shrink-none slds-m-vertical--xxx-small slds-grid slds-grid_align-center']",
                                "//span[contains(text(),'Pick an object')]/ancestor::a",
                                "//div[contains(@class,'uiPopupTrigger')]//a[@role='button']",
                                "(//a[contains(@href, 'javascript:void') and contains(@class, 'entityMenuTrigger')])[1]"
                            ]

                            clicked = False
                            for xpath in xpaths:
                                try:
                                    dropdown_icon = WebDriverWait(driver, 10).until(
                                        EC.element_to_be_clickable((By.XPATH, xpath))
                                    )
                                    dropdown_icon.click()
                                    time.sleep(2)  # Wait for dropdown to open
                                    logging.info(f"Clicked dropdown using XPath: {xpath}")
                                    print(f"✅ Clicked dropdown using XPath: {xpath}")
                                    clicked = True
                                    break
                                except Exception as e:
                                    logging.warning(f"❌ Failed to click with XPath {xpath}: {e}")

                            if not clicked:
                                try:
                                    
                                    driver.execute_script(
                                        "document.querySelector('a.entityMenuTrigger[aria-label*=\"Select New Owner\"]')?.click()"
                                    )
                                    logging.info("Clicked dropdown using JavaScript fallback.")
                                    print("✅ Clicked dropdown using JavaScript fallback.")
                                except Exception as js_error:
                                    logging.error(f"❌ JavaScript fallback failed: {js_error}")
                                    print(f"❌ JavaScript fallback failed: {js_error}")
                                time.sleep(5)

                            try:
                                # Wait and click on the matching dropdown result
                                partner_option_xpath_variants = [
                                    "//span[@title='Partner Users']",
                                    "//span[text()='Partner Users']",
                                    "//span[contains(text(), 'Partner Users')]"
                                ]

                                option_clicked = False
                                for xpath in partner_option_xpath_variants:
                                    try:
                                        partner_option = WebDriverWait(driver, 10).until(
                                            EC.element_to_be_clickable((By.XPATH, xpath))
                                        )
                                        partner_option.click()
                                        time.sleep(2)  # Wait for the click to register
                                        logging.info(f"✅ Clicked 'Partner Users' using XPath: {xpath}")
                                        print(f"✅ Partner Users clicked using XPath: {xpath}")
                                        option_clicked = True
                                        break
                                    except Exception as e:
                                        logging.warning(f"❌ Failed to click with XPath {xpath}: {e}")

                                if not option_clicked:
                                    logging.error("❌ Could not click on 'Partner Users' option from dropdown.")
                                    print("❌ 'Partner Users' option not clickable.")
                            except Exception as e:
                                logging.error(f"❌ Error while selecting 'Partner Users': {e}")
                                print(f"❌ Exception during selecting 'Partner Users': {e}")  
            
                            try:
                                # XPath based on your exact input field
                                search_input_xpath = "//input[@placeholder='Search Partner Users...']"

                                search_input = WebDriverWait(driver, 15).until(
                                    EC.visibility_of_element_located((By.XPATH, search_input_xpath))
                                )
                                
                                search_input.send_keys(email)  # 👈 email from JSON
                                logging.info(f"✅ Entered email '{email}' in Partner Users search box.")
                                print(f"✅ Typed email '{email}' into search box.")

                                time.sleep(3)  # Wait for dropdown suggestion to load

                                

                           

                                time.sleep(7)  # Wait for dropdown suggestion to load - Increased to 7s for safety

                                email_result_xpath_1 = f"//div[contains(@class, 'lookup__header') or contains(@class, 'lookup__item')][.//span[@title='\"{email}\" in Partner Users']]"
                                email_result_xpath_2 = f"//div[contains(@class, 'lookup__header') or contains(@class, 'lookup__item')][.//span[contains(text(), '{email}')]]"
                                email_result_xpath_3 = f"//div[contains(@class,'listbox')]//div[contains(@class,'slds-text-link_reset')][contains(.,'{email}')]"
                                email_result_xpath_4 = "//ul[contains(@class, 'lookup__list')]//li[1]//div[contains(@class, 'itemContainer')]"
                                # 5. Added another fallback if the email is directly inside an 'a' tag within the list item.
                                email_result_xpath_5 = f"//li[contains(@class, 'slds-listbox__option')]//a[contains(@title, '{email}') or .//span[contains(text(), '{email}')]]"
                                
                                result_xpaths_to_try = [
                                    email_result_xpath_1,
                                    email_result_xpath_2,
                                    email_result_xpath_3,
                                    email_result_xpath_4,
                                    email_result_xpath_5 # New XPath added
                                ]
                            
                                result_clicked = False
                                for xpath_to_try in result_xpaths_to_try:
                                    try:
                                        print(f"DEBUG: Trying XPath: {xpath_to_try}") 
                                        email_result_element = WebDriverWait(driver, 20).until( 
                                            EC.element_to_be_clickable((By.XPATH, xpath_to_try))
                                        )
                                        
                                        driver.execute_script("arguments[0].click();", email_result_element)
                                        time.sleep(5)
                                        logging.info(f"✅ Clicked dynamic email search result '{email}' using XPath: {xpath_to_try}.")
                                        print(f"✅ Dynamic email search result '{email}' clicked using XPath: {xpath_to_try}.")
                                        result_clicked = True
                                        break 
                                    except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException) as inner_e:
                                        logging.warning(f"Attempt with dynamic XPath '{xpath_to_try}' failed for email '{email}': {inner_e}. Retrying with next XPath.")
                                        print(f"DEBUG: Attempt with dynamic XPath '{xpath_to_try}' failed: {inner_e}")
                                    except Exception as inner_e:
                                        logging.error(f"An unexpected error occurred with dynamic XPath '{xpath_to_try}': {inner_e}. Retrying.")
                                        print(f"DEBUG: Unexpected error with dynamic XPath '{xpath_to_try}': {inner_e}")

                                if not result_clicked:
                                    logging.error(f"❌ Could not click on the dynamic email search result for '{email}' after trying all XPaths. Skipping this lead.")
                                    print(f"❌ Failed to click on the dynamic email search result for '{email}'. Skipping this lead.")
                                    failed_followups.add(lead_id)
                                    continue 
                                time.sleep(5) 
                            except Exception as e:
                                logging.error(f"❌ Error interacting with Partner Users search input: {e}")
                                print(f"❌ Error typing email: {e}")

                        except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException) as e:
                            logging.error(f"Error processing lead {lead_id}: {e}", exc_info=True)
                            failed_followups.add(lead_id)
                            continue

                        try:
                            
                           
                            popup_xpath = "//div[contains(@class, 'modal-body') or contains(@class, 'slds-modal__container')]"
                            WebDriverWait(driver, 20).until(
                                EC.visibility_of_element_located((By.XPATH, popup_xpath))
                            )
                            logging.info("✅ Partner Users popup/modal appeared.")
                            print("✅ Partner Users popup/modal appeared.")

                            
                            # full_name_link_in_table_xpath = f"//tr[.//a[contains(text(), '{email}') or @href='mailto:{email}'] ]//a[contains(@class, 'outputLookupLink')]"
                            
                           
                            xpath_variant_1 = f"//tr[.//a[@href='mailto:{email}']]/td/a[contains(@class, 'outputLookupLink')]"
                            
                           
                            xpath_variant_2 = f"//tr[.//td[contains(., '{email}')]]//a[contains(@class, 'outputLookupLink')]"

                            
                            # xpath_variant_3 = f"//tr[.//a[@href='mailto:{email}']]/td[1]/a"


                            xpaths_to_try = [
                                xpath_variant_1,
                                xpath_variant_2,
                                # xpath_variant_3 # Keep this commented unless others fail and you are sure of column order.
                            ]

                            name_clicked_in_popup = False
                            for xpath in xpaths_to_try:
                                try:
                                    print(f"DEBUG: Trying to click Full Name in popup table using XPath: {xpath}")
                                    full_name_link_element = WebDriverWait(driver, 25).until( 
                                        EC.element_to_be_clickable((By.XPATH, xpath))
                                    )
                                    
                                    driver.execute_script("arguments[0].click();", full_name_link_element)
                                    time.sleep(7) 
                                    logging.info(f"✅ Clicked Full Name for email '{email}' in the popup table using XPath: {xpath}.")
                                    print(f"✅ Clicked Full Name for email '{email}' in the popup table using XPath: {xpath}.")
                                    name_clicked_in_popup = True
                                    break 

                                except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException) as e:
                                    logging.warning(f"❌ Failed to click Full Name with XPath '{xpath}' for email '{email}': {e}. Trying next XPath.")
                                    print(f"DEBUG: Failed to click Full Name with XPath '{xpath}' for email '{email}': {e}")
                                except Exception as e:
                                    logging.error(f"❌ An unexpected error occurred while trying to click Full Name with XPath '{xpath}': {e}.")
                                    print(f"DEBUG: Unexpected error clicking Full Name with XPath '{xpath}': {e}")

                            if not name_clicked_in_popup:
                                logging.error(f"❌ Could not click on Full Name for email '{email}' in the popup table after trying all XPaths. Skipping this lead.")
                                print(f"❌ Failed to click on Full Name for email '{email}' in the popup table. Skipping this lead.")
                                
                                failed_followups.add(lead_id) 
                                continue 

                            time.sleep(5) 

                        except Exception as e:
                            logging.error(f"❌ Error during Full Name selection in Partner Users popup for email '{email}': {e}")
                            print(f"❌ Exception during Full Name selection in Partner Users popup for email '{email}': {e}")
                            failed_followups.add(lead_id)
                            continue 

                        try:
                            print("DEBUG: Attempting to click the 'Change Owner' button.")
                        
                            change_owner_button_xpath = "//button[@name='change owner' and contains(text(), 'Change Owner')]"
                            
                            
                            # change_owner_button_xpath = "//button[contains(@class, 'slds-button_brand') and contains(text(), 'Change Owner')]"

                            change_owner_button = WebDriverWait(driver, 15).until( # Increased wait to 15s for stability
                                EC.element_to_be_clickable((By.XPATH, change_owner_button_xpath))
                            )
                            
                            
                            driver.execute_script("arguments[0].click();", change_owner_button)
                            time.sleep(7) # Wait for the change to process and UI to update/modal to close
                            
                            logging.info(f"✅ Clicked 'Change Owner' button using XPath: {change_owner_button_xpath}.")
                            print(f"✅ Clicked 'Change Owner' button using XPath: {change_owner_button_xpath}.")

                            try:
                                os.remove(json_file)
                                logging.info(f"✅ Successfully deleted processed JSON file: {json_file}")
                                print(f"✅ Deleted processed file: {json_file}")
                            except OSError as file_error:
                                logging.error(f"❌ Error deleting file {json_file}: {file_error}")
                                print(f"❌ Error deleting file {json_file}: {file_error}")

                        except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException) as e:
                            logging.error(f"❌ Failed to click 'Change Owner' button with XPath '{change_owner_button_xpath}': {e}.")
                            print(f"❌ Failed to click 'Change Owner' button: {e}")
                            failed_followups.add(lead_id)
                            continue 


                        except Exception as e:
                            logging.error(f"❌ An unexpected error occurred while trying to click 'Change Owner' button: {e}.")
                            print(f"❌ Unexpected error clicking 'Change Owner' button: {e}")
                            failed_followups.add(lead_id)
                            continue

            time.sleep(6)
            print(f"Processing complete. Failed tasks: {failed_followups}")
    except Exception as e:
        logging.error(f"Error processing emails: {e}", exc_info=True)
        return   




if __name__ == "__main__":

   
    selenium_url = "https://cxp--preprod.sandbox.my.salesforce.com"
    output_directory = r"C:\Users\WIN10\Desktop\project\FinalPrepod\tempassign"
    username = "smartassist@ariantechsolutions.com.preprod"
    password = "Preprod@ATS07"

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Firefox(options=options)

    login_to_website(driver, selenium_url, username, password)
    navigate_to_cxp_app(driver)
    process_emails( output_directory , driver)

