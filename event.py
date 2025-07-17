import logging
import os
import ssl
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
import time
import requests
import http.client
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import threading
import socket
import subprocess
import urllib3
import os
import glob


logging.basicConfig(
    filename='Event.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def login_to_website(driver, selenium_url, username, password):
    """Log in to the website."""
    driver.get(selenium_url)
    time.sleep(10)
   
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
        driver.get("https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default")
        time.sleep(10)
        return True
    
    else:
        print("cxp app is not displayed")
        return False


def send_put_request(api_url, payload):
    """Send a PUT request to the API with SSL verification disabled."""
    try:
        response = requests.put(api_url, json=payload, verify=False)
        response.raise_for_status()
        logging.info(f"PUT request successful for payload: {payload}. Response: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"PUT request failed for payload {payload}: {e}")
        return None

# def navigate_to_cxp_app(driver):
#     """Navigate to CXP app - separate function for reusability"""
#     try:
#         app_launcher_xpath = "//button[@title='App Launcher']"
#         app_launcher = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.XPATH, app_launcher_xpath))
#         )
#         app_launcher.click()
#         time.sleep(5)
#         print("app launcher clicked")

#         cxp_app_xpath = "//p[text()='CXP Lightning']"
#         cxp_element = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.XPATH, cxp_app_xpath))
#         )

#         if cxp_element.is_displayed():
#             print("cxp app is displayed")
#             cxp_element.click()
#             time.sleep(5)
#             return True
#         else:
#             print("cxp app is not displayed")
#             return False

#     except Exception as e:
#         print(f"Error navigating to CXP app: {e}")
#         return False

# login_done = False

def process_emails(output_directory, selenium_url, driver):
    try:
        output_directory = r"C:\Users\WIN10\Desktop\project\FinalPrepod\tempeventcreate"

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

                    failed_tasks = set()

                    for index, task_data in enumerate(data):
                        print(f"🔁 Processing task {index + 1}/{len(data)}: {task_data.get('task_id')}")

                    for entry in data:
                        try:
                            event_id_followup = (entry.get('event_id')  or '').strip()
                            subject_data   = (entry.get('subject')  or '').strip()
                            # status_data = entry.get('status', '')
                            start_date_data = (entry.get('start_date')  or '').strip()
                            brand_data =(entry.get('brand')  or '').strip()
                            # model_data = (entry.get(('PMI') or '')).strip()
                            model_data = "Range Rover Velar"
                            # owner_email = (entry.get('owner_email')  or '').strip()
                            owner_email = "prem.s@modimotorsjlr.com"

                            # end_date_data = entry.get('end_date', '')
                            description_data = entry.get('description', '')
                            # start_time_data = entry.get('start_time', '')
                            # end_time_data = entry.get('end_time', '')
                            # VIN_data = entry.get('VIN', '')
                            # assigned_to_data = entry.get('assigned_to', '')
                            # lead_id_followup = entry.get('lead_id', '')
                            # cxp_lead_code = entry.get('cxp_lead_code', '')
                            # lead_url = entry.get('lead_url', '')
                            # lead_url =  (entry.get('Lead_url')  or '').strip()
                            lead_url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/00QVc00000CkgsSMAR/mustafa-shayyed"
                            # ((By.XPATH, "//a[@title='New Event' and contains(@class, 'forceActionLink')]"))

                            # if not lead_url or not subject_data or not start_date_data:
                            #     print("Skipping event due to missing critical data (lead_email, event_id, subject, or start_date).")
                            #     continue

                    

                            print(f"Processing task for: {event_id_followup}")

                            # navigation_success = navigate_to_cxp_app(driver)
                            # if not navigation_success:
                            #     print("Failed to navigate to CXP app, refreshing and retrying...")
                            #     driver.refresh()
                            #     time.sleep(5)
                            #     navigation_success = navigate_to_cxp_app(driver)
                            #     if not navigation_success:
                            #         print("Still failed to navigate, skipping this task")
                            #         failed_tasks .add(event_id_followup)
                            #           continue

                            time.sleep(5)
                            print("code yaha tak pahucha ")

                            try:
                                driver.switch_to.window(driver.window_handles[0])
                                url = lead_url
                                driver.get(url)
                                print(f"Opened URL: {url}")
                                time.sleep(10)
                            except Exception as e:
                                print("Error opening URL:", e)
                                failed_tasks.add(event_id_followup)
                                continue

                        except Exception as e:
                            print(f"Error processing entry {entry}: {e}")
                            failed_tasks .add(event_id_followup)

                        driver.execute_script("window.scrollBy(0, 800);")

                        # WebDriverWait(driver, 20).until(
                        #     EC.element_to_be_clickable((By.XPATH, "//a[@title='New Task' and contains(@class, 'forceActionLink')]"))
                        # ).click()
                        # time.sleep(5)

                        # Click Next
                        element = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[@title='New Event' and contains(@class, 'forceActionLink')]"))
                        )
                        element.click()
                        time.sleep(5)


                        try:

                            delete_anchor = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
                            By.XPATH, "//span[text()='Smart Assist']/parent::span//a[@class='deleteAction']")))
                            delete_anchor.click()

                            print("✅ Clicked deleteAction for Smart Assist.")

                        except Exception as e:
                                print("Error entering subject:", e)
                                failed_tasks.add(event_id_followup)
                                continue
                        

                        try:
                                # XPath based on your exact input field
                                search_input_xpath = "//input[@placeholder='Search People...']"

                                search_input = WebDriverWait(driver, 15).until(
                                    EC.visibility_of_element_located((By.XPATH, search_input_xpath))
                                )
                                
                                search_input.send_keys(owner_email)  # 👈 email from JSON
                                logging.info(f"✅ Entered email '{owner_email}' in Partner Users search box.")
                                print(f"✅ Typed email '{owner_email}' into search box.")

                                time.sleep(3)  # Wait for dropdown suggestion to load

                                

                           

                                time.sleep(7)  # Wait for dropdown suggestion to load - Increased to 7s for safety

                                # email_result_xpath_1 = f"//div[contains(@class, 'lookup__header') or contains(@class, 'lookup__item')][.//span[@title='\"{owner_email}\" in Partner Users']]"
                                email_result_xpath_2 = f"//div[contains(@class, 'lookup__header') or contains(@class, 'lookup__item')][.//span[contains(text(), '{owner_email}')]]"
                                # email_result_xpath_3 = f"//div[contains(@class,'listbox')]//div[contains(@class,'slds-text-link_reset')][contains(.,'{owner_email}')]"
                                # email_result_xpath_4 = "//ul[contains(@class, 'lookup__list')]//li[1]//div[contains(@class, 'itemContainer')]"
                                # 5. Added another fallback if the email is directly inside an 'a' tag within the list item.
                                # email_result_xpath_5 = f"//li[contains(@class, 'slds-listbox__option')]//a[contains(@title, '{owner_email}') or .//span[contains(text(), '{owner_email}')]]"
                                
                                result_xpaths_to_try = [
                                    # email_result_xpath_1,
                                    email_result_xpath_2,
                                    # email_result_xpath_3,
                                    # email_result_xpath_4,
                                    # email_result_xpath_5 # New XPath added
                                ]
                            
                                result_clicked = False
                                for xpath_to_try in result_xpaths_to_try:
                                    try:
                                        print(f"DEBUG: Trying XPath: {xpath_to_try}") 
                                        email_result_element = WebDriverWait(driver, 20).until( 
                                            EC.element_to_be_clickable((By.XPATH, xpath_to_try))
                                        )
                                        print("yaha tak aaya hai.")
                                        driver.execute_script("arguments[0].click();", email_result_element)
                                        time.sleep(5)
                                        logging.info(f"✅ Clicked dynamic email search result '{owner_email}' using XPath: {xpath_to_try}.")
                                        print(f"✅ Dynamic email search result '{owner_email}' clicked using XPath: {xpath_to_try}.")
                                        result_clicked = True
                                        break 
                                    except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException) as inner_e:
                                        logging.warning(f"Attempt with dynamic XPath '{xpath_to_try}' failed for email '{owner_email}': {inner_e}. Retrying with next XPath.")
                                        print(f"DEBUG: Attempt with dynamic XPath '{xpath_to_try}' failed: {inner_e}")
                                    except Exception as inner_e:
                                        logging.error(f"An unexpected error occurred with dynamic XPath '{xpath_to_try}': {inner_e}. Retrying.")
                                        print(f"DEBUG: Unexpected error with dynamic XPath '{xpath_to_try}': {inner_e}")

                                if not result_clicked:
                                    logging.error(f"❌ Could not click on the dynamic email search result for '{owner_email}' after trying all XPaths. Skipping this lead.")
                                    print(f"❌ Failed to click on the dynamic email search result for '{owner_email}'. Skipping this lead.")
                                    failed_tasks.add(event_id_followup)
                                    continue 
                                time.sleep(5) 
                        except Exception as e:
                                logging.error(f"❌ Error interacting with Partner Users search input: {e}")
                                print(f"❌ Error typing email: {e}")

                        try:
                            
                           
                            popup_xpath = "//div[contains(@class, 'modal-body') or contains(@class, 'slds-modal__container')]"
                            WebDriverWait(driver, 20).until(
                                EC.visibility_of_element_located((By.XPATH, popup_xpath))
                            )
                            logging.info("✅ Partner Users popup/modal appeared.")
                            print("✅ Partner Users popup/modal appeared.")

                            
                            # full_name_link_in_table_xpath = f"//tr[.//a[contains(text(), '{email}') or @href='mailto:{email}'] ]//a[contains(@class, 'outputLookupLink')]"
                            
                           
                            xpath_variant_1 = f"//tr[.//a[@href='mailto:{owner_email}']]/td/a[contains(@class, 'outputLookupLink')]"
                            
                           
                            xpath_variant_2 = f"//tr[.//td[contains(., '{owner_email}')]]//a[contains(@class, 'outputLookupLink')]"

                            
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
                                    logging.info(f"✅ Clicked Full Name for email '{owner_email}' in the popup table using XPath: {xpath}.")
                                    print(f"✅ Clicked Full Name for email '{owner_email}' in the popup table using XPath: {xpath}.")
                                    name_clicked_in_popup = True
                                    break

                                except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException) as e:
                                    logging.warning(f"❌ Failed to click Full Name with XPath '{xpath}' for email '{owner_email}': {e}. Trying next XPath.")
                                    print(f"DEBUG: Failed to click Full Name with XPath '{xpath}' for email '{owner_email}': {e}")
                                except Exception as e:
                                    logging.error(f"❌ An unexpected error occurred while trying to click Full Name with XPath '{xpath}': {e}.")
                                    print(f"DEBUG: Unexpected error clicking Full Name with XPath '{xpath}': {e}")

                            if not name_clicked_in_popup:
                                logging.error(f"❌ Could not click on Full Name for email '{owner_email}' in the popup table after trying all XPaths. Skipping this lead.")
                                print(f"❌ Failed to click on Full Name for email '{owner_email}' in the popup table. Skipping this lead.")
                                
                                failed_tasks.add(event_id_followup) 
                                continue 

                            time.sleep(5) 

                        except Exception as e:
                            logging.error(f"❌ Error during Full Name selection in Partner Users popup for email '{owner_email}': {e}")
                            print(f"❌ Exception during Full Name selection in Partner Users popup for email '{owner_email}': {e}")
                            failed_tasks.add(event_id_followup)
                            continue


                        # if not clicked:
                        #     print("❌ Failed to click on 'New Event' button using all known XPaths.")

                        subject_value = subject_data

                        xpaths = [
                            "//label[contains(text(), 'Subject')]/following::input[1]",
                            "//input[contains(@class, 'slds-combobox__input') and @role='combobox']",
                            "//input[@type='text' and contains(@aria-haspopup, 'listbox')]"
                        ]
                            
                        for xpath in xpaths:
                            try:
                                subject_input = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, xpath))
                                )
                                subject_input.click()
                                print(f"Clicked subject input using xpath: {xpath}")
                                time.sleep(1)

                                dropdown_option_xpath = f"//lightning-base-combobox-item//span[contains(text(), '{subject_value}')]"
                                dropdown_option = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, dropdown_option_xpath))
                                )
                                dropdown_option.click()
                                print(f"Selected subject value: {subject_value}")
                                break
                            except Exception as e:
                                print(f"Failed with xpath: {xpath} trying next... Error: {e}")
                                failed_tasks.add(event_id_followup)
                                continue

                        start_date_value = start_date_data  # JSON se value

                        start_date_xpaths = [
                            "//legend[contains(text(), 'Start')]/following::input[@type='text'][1]",
                            # "//label[contains(text(), 'Start')]/following::input[@type='text']",
                            # "//input[@aria-describedby and contains(@class, 'slds-input') and @type='text']",
                        ]

                        for xpath in start_date_xpaths:
                            try:
                                start_date_input = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, xpath))
                                )
                                start_date_input.click()
                                start_date_input.clear()
                                start_date_input.send_keys(start_date_value)
                                print(f"Filled start date using xpath: {xpath} with value: {start_date_value}")

                            except Exception as e:
                                print(f"Failed to fill start date using xpath: {xpath} trying next... Error: {e}")
                                failed_tasks.add(event_id_followup)
                                continue
                    

                        try:
                            print("🚀 Trying to click Brand combobox with multiple XPaths...")

                            xpaths = [
                                "//div[@data-target-selection-name='sfdc:RecordField.Event.Brand__c']//a[@role='combobox']",
                                "//span[text()='Brand']/ancestor::div[contains(@class, 'slds-form-element')]/descendant::a[@role='combobox']",
                                "//span[text()='Brand']/following::a[@role='combobox'][1]",
                                "(//a[@role='combobox' and contains(@class, 'select')])[last()]"
                            ]

                            brand_value = brand_data.strip()  # JSON se value

                            combobox_element = None
                            for i, xpath in enumerate(xpaths):
                                try:
                                    print(f"🔍 Trying XPath {i+1}: {xpath}")
                                    elem = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, xpath))
                                    )
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                                    time.sleep(1.5)

                                    if elem.is_displayed() and elem.is_enabled():
                                        elem.click()
                                        print(f"✅ Brand combobox clicked using XPath {i+1}")
                                        logging.info(f"✅ Brand combobox clicked using XPath {i+1}: {xpath}")
                                        combobox_element = elem
                                        break
                                except Exception as e:
                                    print(f"❌ XPath {i+1} failed: {e}")

                                    driver.execute_script("window.scrollBy(0, 250);")
                                    time.sleep(1.5)
                            else:
                                raise Exception("❌ Brand combobox not found/clicked after all XPaths.")

                            if combobox_element:
                                # Dropdown options ka xpath - ye depend karta hai UI pe, example de raha hu:
                                option_xpath = f"//a[@role='option' and @title='{brand_value}']"

                                # Wait for dropdown to appear and option to be clickable
                                option_element = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                                )
                                time.sleep(2)
                                option_element.click()
                                print(f"✅ Brand option '{brand_value}' selected.")

                        except Exception as final_e:
                            logging.error(f"🔥 Brand selection failed: {final_e}")
                            print(f"🔥 Brand selection failed: {final_e}")
                            failed_tasks.add(event_id_followup)
                            continue

                        try:
                            print("🚀 Trying to click Model combobox with multiple XPaths...")

                            xpaths = [
                                "//div[@data-target-selection-name='sfdc:RecordField.Event.Model__c']//a[@role='combobox']",
                                "//span[text()='Model']/ancestor::div[contains(@class, 'slds-form-element')]/descendant::a[@role='combobox']",
                                "//span[text()='Model']/following::a[@role='combobox'][1]",
                                "(//a[@role='combobox' and contains(@class, 'select')])[last()]"
                            ]

                            model_value = model_data.strip()  # JSON se value

                            combobox_element = None
                            for i, xpath in enumerate(xpaths):
                                try:
                                    print(f"🔍 Trying XPath {i+1}: {xpath}")
                                    elem = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, xpath))
                                    )
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                                    time.sleep(1.5)

                                    if elem.is_displayed() and elem.is_enabled():
                                        elem.click()
                                        print(f"✅ Model combobox clicked using XPath {i+1}")
                                        logging.info(f"✅ Model combobox clicked using XPath {i+1}: {xpath}")
                                        combobox_element = elem
                                        break
                                except Exception as e:
                                    print(f"❌ XPath {i+1} failed: {e}")
                                    driver.execute_script("window.scrollBy(0, 250);")
                                    time.sleep(1.5)
                            else:
                                raise Exception("❌ Model combobox not found/clicked after all XPaths.")

                            if combobox_element:
                                # Dropdown option XPath for model, assuming 'title' attribute has model name
                                option_xpath = f"//a[@role='option' and @title='{model_value}']"

                                print(f"🔍 Waiting for dropdown option: {option_xpath}")
                                option_element = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                                )
                                driver.execute_script("arguments[0].scrollIntoView(true);", option_element)
                                time.sleep(0.5)
                                option_element.click()
                                print(f"✅ Model option '{model_value}' selected.")

                        except Exception as final_e:
                            logging.error(f"🔥 Model selection failed: {final_e}")
                            print(f"🔥 Model selection failed: {final_e}")
                            failed_tasks.add(event_id_followup)
                            continue

                        try:
                            print("🚀 Trying to scroll to and fill Description field...")

                            description_label_xpath = "//span[text()='Description']"
                            description_textarea_xpath = "//textarea[@role='textbox' and contains(@class, 'uiInputTextArea')]"

                            # Wait for the label
                            description_label_elem = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, description_label_xpath))
                            )
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", description_label_elem)
                            time.sleep(1)  # thoda wait kare page scroll hone ke liye

                            # Wait for textarea to be clickable
                            description_textarea_elem = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, description_textarea_xpath))
                            )
                            description_textarea_elem.click()
                            time.sleep(0.5)

                            # ✅ Check for None/null
                            if description_data:
                                description_comment = description_data.strip()  # Clean text
                                description_textarea_elem.clear()
                                time.sleep(0.3)
                                description_textarea_elem.send_keys(description_comment)
                                print(f"✅ Description field filled with comment: {description_comment}")
                            else:
                                print("⚠️ No description data found (null); skipping Description field.")

                        except Exception as e:
                            print(f"🔥 Failed to fill Description field: {e}")
                            logging.error(f"Failed to fill Description field: {e}")
                            failed_tasks.add(event_id_followup)
                            continue

                        
                        try:
                            
                            # Correct XPath based on your HTML structure
                            save_btn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "(//button[@title='Save' and contains(@class, 'uiButton--brand') and .//span[text()='Save']])[last()]"))
                            )
                            
                            if save_btn.is_displayed():
                                print("Save button is displayed")
                                save_btn.click()
                                
                        except Exception as e:
                            print("Save button error:", str(e))
                            logging.error(f"Save button error: {str(e)}")
                            failed_tasks.add(event_id_followup)     
                            continue
                            
                        time.sleep(5)   
                            
                        try:
                            toast_element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'forceToastMessage')]//a[contains(@class, 'forceActionLink')]"))
                            )
                            if toast_element.is_displayed():
                                print("Toast element is displayed")
                                toast_element.click()
                            else:
                                print("Toast element not found")
                                failed_tasks.add(event_id_followup)
                                continue
                        except Exception as e:
                            print("Toast message handling:", e)

                            time.sleep(5)

                        # Capture URL and send PUT request
                        current_url = driver.current_url
                        print(f"Captured URL: {current_url}")

                        file_name = "EventCreatePut.json"
                        event_data = {"event_id": event_id_followup, "url": current_url}

                        with open(file_name, 'w') as json_files:
                            json.dump(event_data, json_files, indent=4)

                        with open(file_name, 'r') as json_files:
                            payload = json.load(json_files)

                        try:
                            context = ssl._create_unverified_context()
                            conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)

                            payload_json = json.dumps(payload)
                            headers = {
                                "Content-Type": "application/json",
                                "Content-Length": str(len(payload_json))
                            }

                            conn.request("PUT", "/api/RPA/events/new/flag-inactive", body=payload_json, headers=headers)
                            response = conn.getresponse()

                            if response.status == 200:
                                print("Successfully updated the lead data!")
                                data = response.read().decode()
                                logging.info(f"PUT Response: {data}")

                            try:
                                os.remove(json_file)
                                print(f"🗑️ Deleted {json_file}")
                                time.sleep(2)
                            except Exception as e:
                                print(f"⚠️ Could not delete file: {e}")

                            else:
                                print(f"Failed to update lead data. HTTP {response.status}")
                                logging.error(f"PUT Error Response: {response.read().decode()}")
                        except Exception as e:
                            logging.error(f"PUT request error: {e}")
                            print(f"PUT request error: {e}")

                        # Return to main page for next iteration
                        try:
                            driver.get(selenium_url)  # Go back to main page instead of using back()
                            time.sleep(5)
                            print("Returned to main page for next task")
                        except Exception as e:
                            print(f"Error returning to main page: {e}")

                        except Exception as e:
                            logging.error(f"Error processing task ID {entry.get('event_id')}: {e}")
                            print(f"Error processing task ID {entry.get('event_id')}: {e}")
                            failed_tasks .add(event_id_followup)
                            continue



            print(f"Processing complete. Failed tasks: {failed_tasks }")
                        
                
    except Exception as e:
        logging.error(f"Error in process_emails: {e}")
        print(f"Error in process_emails: {e}")
                
             

if __name__ == "__main__":
    
    output_directory = "C:\\Users\\User\\Desktop\\FinalPrepod\\tempeventcreate"
    selenium_url = "https://cxp--preprod.sandbox.my.salesforce.com"
    username = "smartassist@ariantechsolutions.com.preprod"
    password = "Preprod@ATS07"

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Firefox(options=options)

    login_to_website(driver, selenium_url, username, password)
    process_emails(output_directory, selenium_url, driver)
                

                    



            

            

               


            
                        

