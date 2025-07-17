import logging
import os
import ssl
import json
import time
import glob
import os
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

logging.basicConfig(filename='task_execution_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def login_to_website(driver, selenium_url, username, password):
    driver.get(selenium_url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(username)
    logging.info("Username entered.")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(password)
    logging.info("Password entered.")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Login"))).click()
    logging.info("Login button clicked.")
    time.sleep(20)


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

login_done = False


def process_events (output_directory, selenium_url, driver):
    try:

        output_directory = r"C:\Users\WIN10\Desktop\project\FinalPrepod\temptaskupdate"

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

                    failed_leads = set()

                    for index, lead_data in enumerate(data):
                        print(f"🔁 Processing lead {index + 1}/{len(data)}: {lead_data.get('lead_id')}")
 
                
                    for entry in data:
                            try:
                                logging.info(f"Processing event: {entry}")
                                task_id = (entry.get('task_id') or '').strip()
                                lead_email = entry.get('lead_email', '').lower()
                                subject = entry.get('subject', '')  
                                desired_status = entry.get("status", '').strip()
                                comments= entry.get('comments','')
                                url = entry.get('url', '')

                                if not url:
                                    print("Missing URL, skipping task...")
                                    failed_leads.add(task_id)
                                    continue

                                print(f"Processing event with task_id: {entry.get('task_id', '')}")

                                navigation_success = navigate_to_cxp_app(driver)
                                if not navigation_success:
                                    print("Failed to navigate to CXP app, refreshing and retrying...")
                                    driver.refresh()
                                    time.sleep(5)
                                    navigation_success = navigate_to_cxp_app(driver)
                                    if not navigation_success:
                                        print("Still failed to navigate, skipping this task")
                                        processed_files.add(task_id)
                                        continue
                                
                                time.sleep(5)
                                print("code yaha tak pahucha ")
                            

                                try:
                                    driver.switch_to.window(driver.window_handles[0])
                                    driver.get(url)
                                    print(f"{task_id}: Opened test event page.")
                                    print(f"Opened URL: {url}")
                                    time.sleep(10)
                                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                                    print("Error opening URL:", e)
                                    logging.error(" Opening URL Error", exc_info=True)
                                    processed_files.add(task_id)
                                    continue

                                driver.execute_script("window.scrollBy(0, 400);")
                                print(f"{task_id}: Page scrolled down.")

                                try:
                                    # Click pencil/edit icon for Comments
                                    WebDriverWait(driver, 15).until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[@title='Edit Comments']"))
                                    ).click()
                                    print("Clicked edit pencil for Comments.")
                                    time.sleep(2)

                                    # Edit the comment field
                                    comment_field = WebDriverWait(driver, 15).until(
                                        EC.element_to_be_clickable((By.XPATH, "//textarea[contains(@class, 'textarea')]"))
                                    )
                                    comment_field.clear()
                                    comment_field.send_keys(comments)
                                    print(f"Entered comment: {comments}")
                                    time.sleep(1)

                                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                                    print(f"Failed to update comment for task_id {task_id}: {e}")
                                    logging.error(f"Failed to update comment for task_id {task_id}: {e}")
                                    processed_files.add(task_id)
                                    continue

                                try:
                                    driver.execute_script("window.scrollBy(0, 100);")
                                    print("ab scroll kiya hai aur status update karne wale hain")
                                    status_box = WebDriverWait(driver, 10).until(
                                        EC.element_to_be_clickable((By.XPATH, "//a[@role='combobox' and contains(@class, 'select')]"))
                                    )
                                    status_box.click()
                                    time.sleep(2)

                                    # Fetch the desired status from the event data
                                    
                                    print(f"Selecting status: {desired_status}")

                                    # Wait and click on the desired status option from dropdown
                                    status_option = WebDriverWait(driver, 10).until(
                                        # //ul[@class='scrollable']//a[text()='{desired_status}']

                                        EC.element_to_be_clickable((By.XPATH, f"//ul[@class='scrollable']//a[text()='{desired_status}']"))
                                    )
                                    status_option.click()
                                    time.sleep(2)
                                    print(f"Selected status: {desired_status}")
                                    time.sleep(2)
                        

                                    # Save after status update
                                    # WebDriverWait(driver, 10).until(
                                    #     EC.element_to_be_clickable((By.XPATH, "//button[@name='SaveEdit' or @title='Save' or text()='Save']"))
                                    # ).click()
                                    # print("Clicked Save after status update.")
                                    # time.sleep(5)

                                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                                    print(f"Failed to update status for task_id {task_id}: {e}")
                                    logging.error("Failed to update status for task_id", exc_info = True)
                                    processed_files.add(task_id)
                                    continue

                                try:
                                    save_button = WebDriverWait(driver, 10).until(
                                        EC.element_to_be_clickable((
                                            By.XPATH,
                                            "//button[@title='Save' and contains(@class, 'forceActionButton')] | " +
                                            "//button[.//span[normalize-space(text())='Save']] | " +
                                            "//button[normalize-space()='Save' or .//span[normalize-space()='Save']] | " +
                                            "//button[contains(@class,'uiButton') and contains(@class,'forceActionButton') and .//span[contains(text(),'Save')]]"
                                        ))
                                    )
                                    save_button.click()
                                    print("✅ Save button clicked successfully.")
                                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                                    logging.error(f"❌ Save button click failed: {e}")
                                    print(f"❌ Save button click failed: {e}")
                                    processed_files.add(task_id)  
                                    continue



                                current_url = driver.current_url
                                print(f"Captured URL: {current_url}")
                                time.sleep(10)

                                file_name = "TaskUpdate.json"
                                lead_data = {"task_id": task_id, "url": current_url}

                                with open(file_name, 'w') as json_files:
                                    json.dump(lead_data, json_files, indent=4)

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

                                        conn.request("PUT", "/api/RPA/tasks/updated/flag-inactive", body=payload_json, headers=headers)
                                        response = conn.getresponse()

                                        if response.status == 200:
                                            print("Successfully updated the task data!")
                                            data = response.read().decode()
                                            logging.info(f"PUT Response: {data}")
                                        try:
                                            os.remove(json_file)
                                            print(f"🗑️ Deleted {json_file}")
                                            time.sleep(2)
                                        except Exception as e:
                                            print(f"⚠️ Could not delete file: {e}")
                                        

                                        else:
                                            print(f"Failed to update task data. HTTP {response}")
                                            logging.error(f"PUT Error Response: {response.read().decode()}")
                                    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                                        logging.error(f"PUT request error: {e}")
                                        print(f"PUT request error: {e}")

                                try:
                                    driver.get(selenium_url)  # Go back to main page instead of using back()
                                    time.sleep(5)
                                    print("Returned to main page for next event")
                                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                                    print(f"Error returning to main page: {e}")

                            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                                logging.error(f"Error processing task ID {entry.get('task_id')}: {e}")
                                print(f"Error processing task ID {entry.get('task_id')}: {e}")
                                processed_files.add(task_id)
                                continue   

            print(f"Processing complete. Failed event: {processed_files}")

    except Exception as e:
        logging.error(f"Error in process_events: {e}")
        print(f"Error in process_events: {e}")
                    
       

if __name__ == "__main__":
    # Configuration
    # api_url = "https://api.smartassistapp.in/api/RPA/tasks-data/updated"
    output_directory = "C:\\Users\\User\\Desktop\\SaleLead\\alljsonfile"
    selenium_url = "https://cxp--preprod.sandbox.my.salesforce.com"
    username = "smartassist@ariantechsolutions.com.preprod"
    password = "Preprod@ATS07"

    # Initialize Chrome options
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Firefox(options=options)

    try:
        # Step 1: Login to Salesforce
        login_to_website(driver, selenium_url, username, password)

        navigate_to_cxp_app(driver)

        # Step 2: Process events from API and navigate CXP URLs
        process_events( output_directory, selenium_url, driver)

    except Exception as e:
        logging.error(f"Script execution failed with error: {e}")
        print(f"Something went wrong: {e}")
