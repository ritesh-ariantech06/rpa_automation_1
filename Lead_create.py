import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json
import subprocess
import socket
import threading
# import pyautogui  
# from pynput.keyboard import Controller
import glob
import os
import json
import requests
from datetime import datetime
import ssl
import urllib3
from http.client import HTTPSConnection
import http.client
from selenium.webdriver.common.action_chains import ActionChains
import traceback

import threading
# DEVICE_IP = "192.168.0.236"
# PORT_RANGE = range(30000, 60000)
# TAP_X, TAP_Y = 505, 296
SELENIUM_URL = "https://cxp--preprod.sandbox.my.salesforce.com"
USERNAME = "smartassist@ariantechsolutions.com.preprod"
PASSWORD = "Preprod@ATS07"
found_port = None
lock = threading.Lock()


output_directory = "C:\\Users\\WIN10\\Desktop\\project\\FinalPrepod\\templeadcreate"


def get_all_valid_lead_data():
    """Get all valid JSON data from rpa_logs where rpa_name == 'leads'"""
    rpa_logs_dir = "rpa_logs"
    all_followups_data = []

    if not os.path.exists(rpa_logs_dir):
        print(f"📁 Directory {rpa_logs_dir} does not exist")
        return []

    # Get all JSON files
    json_files = [f for f in os.listdir(rpa_logs_dir) if f.endswith('.json')]

    if not json_files:
        print("📭 No JSON files found.")
        return []

    for file_name in json_files:
        file_path = os.path.join(rpa_logs_dir, file_name)

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Check for rpa_name
            if isinstance(data, dict) and data.get("rpa_name", "").lower() == "leads":
                # Extract the lead data
                if isinstance(data, list):
                    all_followups_data.extend(data)
                elif isinstance(data, dict):
                    for key in ['followups_data', 'lead', 'tasks', 'events']:
                        if key in data and isinstance(data[key], list):
                            all_followups_data.extend(data[key])
                            break
                    else:
                        all_followups_data.append(data)

                print(f"✅ Processed file: {file_name}")
            else:
                print(f"⏭️ Skipped (rpa_name != 'leads'): {file_name}")

        except Exception as e:
            print(f"❌ Error reading file {file_name}: {e}")
            continue

    print(f"📊 Total valid leads collected: {len(all_followups_data)}")
    return all_followups_data


def click_element(output_directory):
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Firefox(options=options)


    driver.get("https://cxp--preprod.sandbox.my.salesforce.com")
    print("yaha pahucha")
    logging.info("Navigated to login page.")

    try:
        
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='username']"))
        ).send_keys(USERNAME)
        logging.info("Entered username.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='password']"))
        ).send_keys(PASSWORD)
        logging.info("Entered password.")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='Login']"))
        ).click()
        time.sleep(10)
        logging.info("Clicked login button.")

        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH,"//button[@title='App Launcher']"))
        ).click()
        time.sleep(5)

        WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH,"//p[text()='CXP Lightning']"))
        ).click()
        time.sleep(5)

        driver.get("https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/Default")
        time.sleep(10)
       
      
        os.makedirs(output_directory, exist_ok=True)

        # Set up logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

      
        output_directory = "C:\\Users\\WIN10\\Desktop\\project\\FinalPrepod\\templeadcreate"

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

                    if isinstance(data, dict):
                        data = [data]

                    failed_leads = set()

                    for index, lead_data in enumerate(data):
                        print(f"🔁 Processing lead {index + 1}/{len(data)}: {lead_data.get('lead_id')}")

                        currenturl = driver.current_url
                        if "lead/Lead/Default" not in currenturl:
                            print("🔄 Redirecting to the correct page...")
                            driver.back()
                            time.sleep(10)

                        try:
                            logging.info(json.dumps(lead_data, indent=4))
                            # 🛠️ Your Selenium logic to fill in the form
                            print(f"✅ Lead {lead_data.get('lead_id')} processed")

                        except Exception as e:
                            print(f"❌ Error processing lead {lead_data.get('lead_id')}: {e}")
                            failed_leads.add(lead_data.get('lead_id'))  # Optional if you want to retry later

                        time.sleep(2)
                    
                        fname = lead_data.get('fname', '')
                        lname = lead_data.get('lname', '')
                        lead_status = lead_data.get('status', '')
                        lead_source = lead_data.get('lead_source', '')
                        print(lead_source)
                        print(lead_source)
                        enquiry_type = lead_data.get('enquiry_type', '')
                        print(enquiry_type)
                        mobile = lead_data.get('mobile', '')
                        brand = lead_data.get('brand', '')
                        purchase_type = lead_data.get('purchase_type', '')
                        print(purchase_type)
                        sub_type = lead_data.get('sub_type', '')
                        PMI = lead_data.get('PMI', '')
                        print(PMI)
                        lead_id = lead_data.get('lead_id', '')
                        email=lead_data.get('email','')

                        if brand=='Jaguar':
                            driver.refresh()
                            time.sleep(10)
                            continue

                        print("yaha se start")
                        current_url = driver.current_url

                            

                        print("yaha tak end hauin")

                        time.sleep(10)
                        try:
                            driver.switch_to.window(driver.window_handles[0])
                            print("new button ke passed pahucha ")
                    
                            new_button = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.XPATH, '//a[@title="New" and contains(@class, "forceActionLink")]/div[@title="New"]'))
                            )
                            logging.info("New button is located.")
                            # //button[span[text()='Next']]

                            
                            # Scroll to the element
                            actions = ActionChains(driver)
                            actions.move_to_element(new_button).perform()
                            logging.info("Scrolled to the New button.")

                            # Check visibility and click
                            if new_button.is_displayed():
                                new_button.click()
                                time.sleep(10)
                                logging.info("Clicked the New button successfully.")
                                print("new button has been clcikded")
                            else:
                                logging.warning("New button is not visible.")

                            # next pe click kar rha hu yaha se

                            next_button = WebDriverWait(driver, 30).until(
                                EC.presence_of_element_located((By.XPATH, "//button[span[text()='Next']]"))
                            )
                            logging.info("next button is located.")
                            # //button[span[text()='Next']]

                            
                            # Scroll to the element
                            actions = ActionChains(driver)
                            actions.move_to_element(next_button).perform()
                            logging.info("Scrolled to the next button")

                            # Check visibility and click
                            if next_button.is_displayed():
                                next_button.click()
                                time.sleep(10)
                                logging.info("Clicked the next button successfully.")
                                print("next button has been clcikded")
                            else:
                                logging.warning("next button is not visible.")


                        except Exception as e:
                            logging.error(f"Failed to locate or click the New button: {e}")
                            traceback.print_exc()
                            driver.refresh()
                            time.sleep(5)
                            continue
                        time.sleep(10)
                        print("all done tiill here")                            


                        if lname:
                            
                            # salution_btn='//*[@id="sectionContent-91"]/dl/slot/records-record-layout-row[1]/slot/records-record-layout-item[1]/div/span/slot/records-record-layout-input-name/lightning-input-name/fieldset/div/div/div[1]/lightning-picklist/lightning-combobox/div/div[1]/lightning-base-combobox'
                            # salution_btn=driver.find_element(By.XPATH, salution_btn)
                            # salution_btn.click()
                            # pyautogui.press('down')
                            # pyautogui.press('enter')

                            try:
                            #     # Wait for the First Name field to be visible
                                first_name_xpath = "//label[text()='First Name']/following-sibling::div//input"
                                first_name_input = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, first_name_xpath))
                                )
                                time.sleep(2)
                                first_name_input.send_keys(fname)
                                logging.info("Entered First Name successfully.")
                            except TimeoutException:
                                logging.error("First Name input field was not found.")
                            except Exception as e:
                                logging.error(f"Unexpected error when entering First Name: {e}")

                            try:
                                # Wait for the Last Name field to be visible
                                last_name_xpath = "//label[text()='Last Name']/following-sibling::div//input"
                                last_name_input = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, last_name_xpath))
                                )
                                if last_name_input.is_displayed():
                                    print("elemnt found last name")
                                else:
                                    print("elemnt not found")
                                print(lname)
                                last_name_input.send_keys(lname)
                                logging.info("Entered Last Name successfully.")
                                driver.execute_script("arguments[0].scrollIntoView();", last_name_input)
                            except TimeoutException:
                                logging.error("Last Name input field was not found.")
                            except Exception as e:
                                print("yeh error dekho sdjvnsdjknnn: {e}")
                                traceback.print_exc()

                                print(f"yeh error dekho sdjvnsdjknnn: {e}")

                            
                            logging.info("Entered Last Name successfully.")
                            

                            # Wait for and click the cancel button
                            
                            
                            try:
    # Wait for the button to be clickable
                                button = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Lead Status' and contains(@class, 'slds-combobox__input')]"))
                                )
                                                                
                                # Click the button
                                button.click()
                                print("Button clicked successfully.")

                            except Exception as e:
                                print(f"Error occurred: {e}")
                                traceback.print_exc()
                                continue



                            # # Wait for dropdown options to be visible
                            try:
                        
                                print(f" the lead status are {lead_status}")
                                

                                # Use pyautogui to navigate if the specific status is known
                                if lead_status == "Follow Up":
                                    follow_up_xpath="//lightning-base-combobox-item[@data-value='Follow Up']"
                                    follow_up_xpath = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, follow_up_xpath)))
                                    follow_up_xpath.click()
                                    

                                    
                                    logging.info("Pressed down once for 'Follow Up'.")
                                elif lead_status == "New":
                                    new_up_xpath="//lightning-base-combobox-item[@data-value='New']"
                                    new_up_xpath = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,new_up_xpath)))
                                    new_up_xpath.click()

                                elif lead_status == "Qualified":
                                    qual_xpath="//lightning-base-combobox-item[@data-value='Qualified']"
                                    qual_xpath = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,qual_xpath)))
                                    qual_xpath.click()
                                
                                    logging.info("Pressed down twice for 'Qualified'.")
                                elif lead_status == "Lost":
                                    last_xpath="//lightning-base-combobox-item[@data-value='Lost']"
                                    last_xpath = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH,last_xpath)))
                                    last_xpath.click()
                                    
                                
                                else:
                                    logging.info(f"No specific action for status '{lead_status}'.")
                                
                            except Exception as e:
                                print(f"Error occurred: {e}")
                                traceback.format_exc()
                            
                            
                                
                            try:

                                
                                fourth_dropdown = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Lead Source' and contains(@class, 'slds-combobox__input')]"))
                                )
                                
                            # Click the dropdown
                                fourth_dropdown.click()
                                print("Fourth dropdown clicked successfully.")                            
                                
                                # After you handle lead_status and enquiry_type, add the following for lead_source
                                if lead_source == "Email":
                                    email_dropdown = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Email']"))
                                    )
                                    email_dropdown.click()
                                
                                    
                                    

                                elif lead_source == "Existing Customer":
                                    exist_drop = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Existing Customer']"))
                                    )
                                    exist_drop.click()
                                elif lead_source == "Field Visit":
                                    feild_drop = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Field Visit']"))
                                    )
                                    feild_drop.click()

                                elif lead_source == "Google SEM Ads":
                                    Google_dropdown = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Google SEM Ads']"))
                                    )
                                    Google_dropdown.click()

                                elif lead_source == "Line":
                                    line_dropdown = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Line']"))
                                    )
                                    line_dropdown.click()
                                    
                                

                                elif lead_source == "OEM Experience":
                                    OEM = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='OEM Experience']"))
                                    )
                                    OEM.click()
                                elif lead_source == "OEM Web & Digital":
                                    OEM_web = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='OEM Web & Digital']"))
                                    )
                                    OEM_web.click()
                                    

                                elif lead_source == "Online Booking":
                                    online_booking = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Online Booking']"))
                                    )
                                    online_booking.click()

                                elif lead_source == "Online Chat":
                                    online_chat = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Online Chat']"))
                                    )
                                    online_chat.click()

                                elif lead_source == "Phone-in":
                                    xpath = "//lightning-base-combobox-item[@data-value='Phone-in']"

    # Wait for presence
                                    Phone_in = WebDriverWait(driver, 5).until(
                                        EC.presence_of_element_located((By.XPATH, xpath))
                                    )

                                    # Scroll into view
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", Phone_in)

                                    # Ensure clickable
                                    Phone_in = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, xpath))
                                    )

                                    try:
                                        # Try ActionChains click
                                        ActionChains(driver).move_to_element(Phone_in).click().perform()
                                    except:
                                        # JS fallback click
                                        driver.execute_script("arguments[0].click();", Phone_in)
                 

                                elif lead_source == "Phone-out":
                                    Phone_out = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Phone-out']"))
                                    )
                                    Phone_out.click()
                                    
                                    

                                elif lead_source == "Purchased List":
                                    purchase_list = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Purchased List']"))
                                    )
                                    purchase_list.click()
                                    
                                    

                                elif lead_source == "Referral":
                                    Referral_drop = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Referral']"))
                                    )
                                    Referral_drop.click()
                                    
                                    

                                elif lead_source == "Retailer Experience":
                                    retailer_experinece = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Retailer Experience']"))
                                    )
                                    retailer_experinece.click()
                                    
                                elif lead_source == "Retailer Website":
                                    Retailer_website = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Retailer Website']"))
                                    )
                                    Retailer_website.click()
                                    
                                elif lead_source == "SMS":
                                    SMS = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='SMS']"))
                                    )
                                    SMS.click()
                                    
                                    

                                elif lead_source == "Social":
                                    
                                    Social_dropdown = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Social']"))
                                    )
                                    Social_dropdown.click()

                                elif lead_source == "Social (Retailer)":
                                    Social_dropdown_retailer = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Social (Retailer)']"))
                                    )
                                    Social_dropdown_retailer.click()

                                    
                                elif lead_source == "Walk-in":
                                    walk_in = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Walk-in']"))
                                    )
                                    walk_in.click()
                                    

                                elif lead_source == "Whatsapp":
                                    Whatsapp = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Whatsapp']"))
                                    )
                                    Whatsapp.click()
                                    

                                else:
                                    logging.info(f"No specific action for lead source '{lead_source}'.")
                                    
                            except Exception as e:
                                print("no third is not working")
                                traceback.print_exc()
                                failed_leads.add(lead_id)
                                continue


                            time.sleep(1)
                           
                            fifth_dropdown = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enquiry Type' and contains(@class, 'slds-combobox__input')]"))
                            )

                            # Click the Lead Source dropdown
                            fifth_dropdown.click()
                            print("Lead Source dropdown clicked successfully.")
                            
                            
                            try:
                                print(f"the  lead status are {enquiry_type}")
                                

                                if enquiry_type == "(Generic) Purchase intent within 90 days":
                                    genric = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Generic']"))
                                    )
                                    genric.click()
                                    
                                #             logging.info("Pressed down for '(Generic) Purchase intent within 90 days'.")
                                elif enquiry_type == "Accessory Offers":
                                    Accessories_type = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Accessory Offers']"))
                                    )
                                    Accessories_type.click()

                                elif enquiry_type == "Approved Pre-owned":
                                    Accessories_type = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Accessory Offers']"))
                                    )
                                    Accessories_type.click()
                              
                                elif enquiry_type == "KMI":
                                    KMI_TYPE = WebDriverWait(driver, 2).until(
                                    EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='KMI']"))
                                    )
                                    KMI_TYPE.click()
                               
                            
                            
                                else:
                                    logging.info(f"No specific action for enquiry type '{enquiry_type}'.")
                                time.sleep(2)
                            except Exception as e:
                                print("no  exception",e)
                                traceback.print_exc()
                                failed_leads.add(lead_id)
                                continue
                            
                            print(f"the brand is {brand}")

                            input_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search Vehicle Specifications...']"))
                            )
                            driver.execute_script("arguments[0].click();", input_element)
                            if  brand == "Land Rover":
                                input_element.send_keys("Land")
                                icon_element = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.XPATH, "//lightning-base-combobox-item[@data-value='a0Z24000007bJHYEA2']"))
                                )


                            # Click the icon
                                icon_element.click()

                            
                            elif brand=="Jaguar":
                                input_element.send_keys("Jag")
                                time.sleep(2)
                                icon_element = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.XPATH, "//lightning-icon[@icon-name='custom:custom67']"))
                                )
                                icon_element.click()
                                
                               
                            else:
                                print(" not found brand ")
                            time.sleep(1)
                           
                            print(PMI)

                       
                            try:
                                pmidata=WebDriverWait(driver,10).until(
                                    EC.element_to_be_clickable((By.XPATH,'//lightning-base-combobox//input[@placeholder="Search Vehicle Specifications..."]'))
                                )
                                if pmidata.is_displayed():
                                    print("bhail milgfaa ")
                                    pmidata.click()
                                    pmidata.send_keys(PMI[:4])
                                    time.sleep(1)
                                else:
                                    print("nahi mila yrr")
                            except Exception as e:
                                print("the errro hgas been found",e)


                            try:
                                option_data = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, f"//lightning-base-combobox-item[normalize-space(.//span[contains(@class,'slds-listbox__option-text')])='{PMI}']"))
                                )
                                if option_data.is_displayed():
                                    print("elemnt milgaya bhai")
                                    option_data.click()
                                else:
                                    print("elemnt nahi mila bhai ")
                                
                               
                            except Exception as e:
                                print("the elemnt has not been found",e)
                                logging.error(f"Error in processing PMI: {e}", exc_info=True)
                                failed_leads.add(lead_id)
                                traceback.print_exc()
                                continue
                                                                
                            try:
                               
                                mobile_xpath = "//input[@name='Email' and @type='text']"
                                
                                # Explicit wait for the element to be visible and clickable
                                mobile_element = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, mobile_xpath))
                                )
                                if mobile_element.is_displayed:
                                
                                    # Send the email to the input field
                                    mobile_element.send_keys(email)
                                    print("email has enter succesfully")
                                else:
                                    print("email is not visible")
                                
                                
                                logging.info("Entered email successfully.")
                            except Exception as e:
                                logging.error(f"The email input field was not found or there was an issue: {e}")
                                print("The email input field has not been found:", e)


                            try:
                            
                                purchase_button = "//button[contains(@class, 'slds-combobox__input') and contains(@aria-label, 'Purchase Type') and @data-value='--None--']"
                                purchase_button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, purchase_button)))
                                driver.execute_script("arguments[0].scrollIntoView(true);", purchase_button)


                                purchase_button.send_keys(purchase_type)
                                logging.info("Entered First Name successfully.")
                                
                                print(f"the  purchase type is {purchase_type}")

                                if purchase_type=='New Vehicle':
                                    purchase_btn = "//lightning-base-combobox-item[@data-value='New Vehicle']"
                                    purchase_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, purchase_btn)))
                                    purchase_btn.click()
                                    
                                elif purchase_type=='Used Vehicle':
                                    used_btn = "//lightning-base-combobox-item[@data-value='Used Vehicle']"
                                    used_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, used_btn)))
                                    used_btn.click()
                                    
                                    
                                else:
                                    print("Purchase type not found")
                            except Exception as e:
                                print("the error has been found",e)
      
                            try:
                            
                                save_btn_xpath = "//li[@data-target-selection-name='sfdc:StandardButton.Lead.SaveEdit']//button[@name='SaveEdit']"
                                save_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, save_btn_xpath)))
                                
                                if save_btn.is_displayed() and save_btn.is_enabled():
                                    logging.info("Save button is visible and enabled.")
                                    save_btn.click()  
                                    print("save button has been clciked succesfully")
                                    time.sleep(3)
                                    logging.info("Save button clicked successfully.")
                                    
                                    
                                else:
                                    logging.error("Save button is either not displayed or disabled.")
                                WebDriverWait(driver, 20).until(EC.url_changes(driver.current_url))
                                logging.info("URL has changed, page is reloading or redirecting.")
                                time.sleep(2)
                            except Exception as e:
                                failed_leads.add(lead_id)
                                driver.refresh()
                                time.sleep(5)
                                continue
                            

                            try:
                                current_url = driver.current_url

                                
                                print(f"the lead_id: {lead_id}")

                            
                                urlname = current_url
                                print(f"the url hain yeh bhai{urlname}")
                            
                                file_name = f"lead_{lead_id}.json"
                                lead_data = {"lead_id": lead_id, "url": urlname}

                            
                                with open(file_name, 'w') as json_files:
                                    json.dump(lead_data, json_files, indent=4)

                                print(f"Successfully stored lead_id: {lead_id} in file: {file_name}")

                                
                                with open(file_name, 'r') as json_files:
                                    payload = json.load(json_files)

                                
                                api_url = "https://api.smartassistapp.in/api/RPA/leads/new/flag-inactive"


                                
                                try:
                                    context = ssl._create_unverified_context()
                                    conn = http.client.HTTPSConnection("api.smartassistapp.in", context=context)

                                    
                                    payload_json = json.dumps(payload)

                                
                                    headers = {
                                        "Content-Type": "application/json",
                                        "Content-Length": str(len(payload_json))
                                    }

                                    
                                    conn.request("PUT", api_url, body=payload_json, headers=headers)

                                    
                                    response = conn.getresponse()
                                                                # existing PUT and response check
                                    if response.status == 200:
                                        print("Successfully updated the lead data!")
                                        data = response.read().decode()
                                        logging.info(f"Response: {data}")
                                    try:
                                        os.remove(json_file)
                                        print(f"🗑️ Deleted {json_file}")
                                        time.sleep(2)
                                    except Exception as e:
                                        print(f"⚠️ Could not delete file: {e}")

                                except Exception as e:
                                    logging.error(f"Error during PUT request: {e}")
                                    print(f"Error during PUT request: {e}")
                                    
                                    continue
                            except Exception as e:
                                print("the error has been found",e)
                                traceback.print_exc()
                                
                                continue
                            driver.back()
                            time.sleep(5)
                            driver.refresh()
                            time.sleep(5)

                        else:
                            logging.error("First name, last name, or lead status not found in lead data.")
                            failed_leads.add(lead_id)
                            traceback.print_exc()
                            driver.refresh()
                            time.sleep(10)
                            continue

                    else:
                        error_msg = f"Missing required data for {fname} {lname} with lead_id {lead_id}. Required fields: fname, lname, lead_status, lead_source, enquiry_type, mobile, brand, type, purchase_type, sub_type, PMI."
                        logging.error(error_msg)
                        traceback.print_exc()
                        failed_leads.add(lead_id)
                        driver.refresh()
                        time.sleep(5)
                        continue
  
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        traceback.print_exc()
        

def main():
    output_directory = "C:\\Users\\WIN10\\Desktop\\project\\FinalPrepod\\templeadcreate"
    click_element(output_directory)
    logging.info("Waiting for 1 hour before next execution...")
        
if __name__ == "__main__":
    main()