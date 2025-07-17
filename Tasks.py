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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time
import requests
import http.client
from datetime import datetime, timedelta
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import threading
import subprocess
import socket
import traceback
import urllib3
import glob 
import os

logging.basicConfig(
    filename='TasksCreate.log',
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



def process_emails(output_directory, selenium_url, driver):
    try:
        
        output_directory = r"C:\Users\WIN10\Desktop\project\FinalPrepod\temptaskcreate"
       
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
                        task_id_followup = (entry.get('task_id') or '').strip()
                        subject            = (entry.get('subject')  or '').strip()
                        comments           = (entry.get('comments') or '').strip()
                        status_data        = (entry.get('status')   or '').strip()
                        # priority_data      = (entry.get('priority') or '').strip()
                        priority_data = "High"
                        # url           =   (entry.get('lead_url') or '').strip()
                        # owner_email      = (entry.get('owner_email') or '').strip()
                        owner_email = "prem.s@modimotorsjlr.com"
                        url = "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/00QVc00000CkgsSMAR/mustafa-shayyed"

                        print(f"✅ Processing task for: {task_id_followup}")

                        time.sleep(5)
                        print("code yaha tak pahucha ")

                        try:
                            driver.switch_to.window(driver.window_handles[0])
                            driver.get(url)
                            print(f"Opened URL: {url}")
                            time.sleep(15)
                            print("yaha tak pahucha")
                        except Exception as e:
                            print("Error opening URL:", e)
                            failed_tasks.add(task_id_followup)
                            continue

                        driver.execute_script("window.scrollBy(0, 800);")

                        # Click New Task
                        WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[@title='New Task' and contains(@class, 'forceActionLink')]"))
                        ).click()
                        time.sleep(5)

                        # Click Next
                        element = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next' and contains(@class, 'label')]"))
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
                                failed_tasks.add(task_id_followup)
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
                                    failed_tasks.add(task_id_followup)
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
                                
                                failed_tasks.add(task_id_followup) 
                                continue 

                            time.sleep(5) 

                        except Exception as e:
                            logging.error(f"❌ Error during Full Name selection in Partner Users popup for email '{owner_email}': {e}")
                            print(f"❌ Exception during Full Name selection in Partner Users popup for email '{owner_email}': {e}")
                            failed_tasks.add(task_id_followup)
                            continue

                        

                    # Enter Subject
                        try:
                            print(f"Trying to enter subject: {subject}")
                            subject_btn = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "//label[normalize-space(text())='Subject']/following::input[1]"))
                            )
                            subject_btn.clear()
                            subject_btn.send_keys(subject)
                            logging.info(f"Entered subject: {subject}")
                            time.sleep(2)
                        except Exception as e:
                            print("Error entering subject:", e)
                            failed_tasks.add(task_id_followup)
                            continue

                        driver.execute_script("window.scrollBy(0, 200);")

                        # Enter Comments
                        comments_xpath = "//span[normalize-space(text())='Comments']/following::textarea[1]"
                        try:
                            comments_btn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, comments_xpath))
                            )
                            if comments_btn.is_displayed():
                                print("comments button is displayed")
                                comments_btn.clear()
                                comments_btn.send_keys(comments)
                                logging.info(f"Entered comment: {comments}")
                                print("comments entered")
                                time.sleep(3)
                            else:
                                print("comments button is not displayed")
                                
                                continue
                        except Exception as e:
                            print("Error entering comments:", e)
                            continue

                        # Optimized Status Selection
                        # ✅ Optimized Status Selection
                        try:
                            print(f"Trying to select status: {status_data}")
                            driver.execute_script("window.scrollBy(0, 200);")
                            time.sleep(2)
                            
                            # Find and click the status dropdown
                            status_btn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space(text())='Status']/following::a[@role='combobox'][1]"))
                            )
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_btn)
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", status_btn)
                            print("Status dropdown clicked")
                            time.sleep(3)
                            
                            # Select the status option
                            status_option = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, f"//a[@role='option' and normalize-space(text())='{status_data}']"))
                            )
                            driver.execute_script("arguments[0].click();", status_option)
                            print(f"Successfully selected status: {status_data}")
                            logging.info(f"Selected status: {status_data}")
                            time.sleep(2)

                        except Exception as e:
                            print(f"Status selection error: {str(e)}")
                            logging.error(f"Status selection error: {str(e)}")
                            failed_tasks.add(task_id_followup)
                            continue


                        # ✅ Optimized Priority Selection
                        try:
                            if not priority_data:
                                logging.warning(f"No priority provided for task {task_id_followup}, skipping priority selection.")
                            else:
                                logging.info(f"Trying to select priority: {priority_data}")

                                # Find and click the priority dropdown
                                priority_input = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((
                                        By.XPATH,
                                        "//span[normalize-space(text())='Priority']/following::a[@role='combobox' and contains(@class,'select')][1]"
                                    ))
                                )
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", priority_input)
                                time.sleep(1)
                                driver.execute_script("arguments[0].click();", priority_input)
                                logging.info("Clicked on Priority dropdown")
                                time.sleep(2)

                                # priority hamesa high rhega
                                priority_option = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((
                                        By.XPATH,
                                        f"//a[@role='option' and normalize-space(text())='{priority_data}']"
                                    ))
                                )
                                driver.execute_script("arguments[0].click();", priority_option)
                                logging.info(f"Successfully selected priority: {priority_data}")
                                time.sleep(2)

                        except Exception as e:
                            logging.warning(f"Failed to set priority '{priority_data}' for task {task_id_followup}: {e}")
                            failed_tasks.add(task_id_followup)
                            time.sleep(3)
                            continue


                        # Save Button Click - Using correct XPath from HTML structure
                        try:
                            
                            print("yaha tak pahocha di pr atak q gaya")
                            # Correct XPath based on your HTML structure
                            save_btn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "(//button[@title='Save' and contains(@class, 'uiButton--brand') and .//span[text()='Save']])[last()]"))
                            )
                            
                            if save_btn.is_displayed():
                                print("Save button is displayed")
                                save_btn.click()
                                
                        except Exception as e:
                            print("Save button error:", str(e))
                            failed_tasks.add(task_id_followup)
                            time.sleep(5)   
                            continue
            
                        # Handle toast message
                        try:
                            toast_element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'forceToastMessage')]//a[contains(@class, 'forceActionLink')]"))
                            )
                            if toast_element.is_displayed():
                                print("Toast element is displayed")
                                toast_element.click()
                            else:
                                print("Toast element not found")
                        except Exception as e:
                            print("Toast message handling:", e)
                            time.sleep(5)

                        # Capture URL and send PUT request
                        current_url = driver.current_url
                        print(f"Captured URL: {current_url}")
                        
                        file_name = "TasksCreatePut.json"
                        lead_data = {"task_id": task_id_followup, "url": current_url}

                        with open(file_name, 'w') as json_files:
                            json.dump(lead_data, json_files, indent=4)

                        with open(file_name, 'r') as json_files:
                            payload = json.load(json_files)

                            # Send PUT request
                            try:
                                context = ssl._create_unverified_context()
                                conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)

                                payload_json = json.dumps(payload)
                                headers = {
                                    "Content-Type": "application/json",
                                    "Content-Length": str(len(payload_json))
                                }

                                conn.request("PUT", "/api/RPA/tasks/new/flag-inactive", body=payload_json, headers=headers)
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
                                    print(f"Failed to update lead data. HTTP {response}")
                                    logging.error(f"PUT Error Response: {response.read().decode()}")
                                




                            except Exception as e:
                                logging.error(f"PUT request error: {e}")
                                print(f"PUT request error: {e}")
                        try:
                            driver.get(selenium_url)  # Go back to main page instead of using back()
                            time.sleep(5)
                            print("Returned to main page for next task")
                        except Exception as e:
                            print(f"Error returning to main page: {e}")


                    
            time.sleep(6)
            print(f"Processing complete. Failed tasks: {failed_tasks}")
    except Exception as e:
        logging.error(f"Critical error in process_emails: {e}")
        print(f"Critical error: {e}")

if __name__ == "__main__":
   
    output_directory = "C:\\Users\\User\\Desktop\\FinalPrepod\\temptaskcreate"
    selenium_url = "https://cxp--preprod.sandbox.my.salesforce.com"
    username = "smartassist@ariantechsolutions.com.preprod"
    password = "Preprod@ATS07"

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Firefox(options=options)

    login_to_website(driver, selenium_url, username, password)
    process_emails(output_directory, selenium_url, driver)