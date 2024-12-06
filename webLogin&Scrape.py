login_url = "https://suadfs1.shepherd.edu/adfs/ls/?SAMLRequest=jdE7b4MwEADgvVL%2fg%2bUdjG0C2IJIUbtESpek7dClMnAEJLCpz1T9%2bSWN%2bhi73UMnfXdX7pbQ2yO8LYCB7O8rimYa%2fTV%2f5YmEpOOZ4apOAYpiY7KirkVS51lrZEvJM3gcnK2oiBNK9ogL7C0GY8NaSkQacR7x%2fJFLLbgWMpYyk5ts80LJDhF8WGfvnMVlAn8C%2fz408HQ8VLQPYUbNWO2Hcx9wNg3E2MPcg29jaBfWipGNMzOrno3uPFh2cR8uUbz2KPmYRosVXbzVzuCA2poJUIdGn3YPB71y9exdcI0b6fb2hpDyC%2b%2f%2fM2i%2b6XT7A5Wp6JIuj6TIkygtVBepQtWRapURSklZiCYOYNfDYPx3q8ZNv%2fSSXRErqGR%2fP7P9BA%3d%3d&RelayState=%2fd2l%2fhome"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

import time

# Set up the driver (e.g., ChromeDriver)
driver = webdriver.Chrome()

# Load the webpage
driver.get(login_url)

try:
    # Wait for an element that appears only after login (e.g., a logout button)
    WebDriverWait(driver, 300).until(
        EC.title_is("Homepage - Shepherd University")  # Replace with an appropriate locator
    )
    print("Login successful!")


    # Wait for JavaScript to load (use WebDriverWait for more robust handling)
    time.sleep(3)  # You may need to adjust this depending on the page's load time

    # This element is inside 6 nested shadow DOMs.
    #css_selector_for_host1 = "d2l_1_15_896" # DWH - This number changes every time the page loads.  So when the addon shows it as _896, the next load it might be _360
    css_selector_for_host2 = "d2l-my-courses-container"
    css_selector_for_host3 = "d2l-tabs > d2l-tab-panel:nth-child(3) > d2l-my-courses-content" #only works with current semester
    
     # This, too, is going to be specific to how many classes a person has.  Might need to find a more generic tag to search on, instead of the CSS "d2l-tabs:nth-child(3) > d2l-tab-panel:nth-child(1) > d2l-my-courses-content:nth-child(1)"
    css_selector_for_host4 = "d2l-my-courses-card-grid"
    # "d2l-my-courses-card-grid"
    css_selector_for_host5 = ".course-card-grid.columns-2 > d2l-enrollment-card:nth-child(2)" # different enrollment cards for diff. classes
    css_selector_for_host6 = "d2l-card" # Same as before - this is a very specific tag to a very specific class.





    time.sleep(1)
    elements1 = driver.find_elements(By.TAG_NAME, "d2l-my-courses")
    for e in elements1:
        shadow0 = e.shadow_root
        time.sleep(1)
        shadow1 = shadow0.find_element(By.CSS_SELECTOR, css_selector_for_host2).shadow_root
        time.sleep(1)
        shadow2 = shadow1.find_element(By.CSS_SELECTOR, css_selector_for_host3).shadow_root
        time.sleep(1)
        shadow3 = shadow2.find_element(By.CSS_SELECTOR, css_selector_for_host4).shadow_root
        time.sleep(1)

        classes = shadow3.find_elements(By.CSS_SELECTOR, "d2l-enrollment-card")
        num_classes = len(classes)
        print(num_classes)
        class_num = 1
        all_class_text = ""
        for Class in classes:
            shadow4 = shadow3.find_element(By.CSS_SELECTOR, f".course-card-grid.columns-2 > d2l-enrollment-card:nth-child({class_num})").shadow_root
            time.sleep(1)
            class_num += 1
            
            class_text = shadow4.find_element(By.CSS_SELECTOR, "d2l-card").text
            all_class_text += class_text
            
        
        # shadow5 = shadow4.find_element(By.CSS_SELECTOR, css_selector_for_host6).shadow_root
        # time.sleep(1)
        # shadow5.find_element(By.CSS_SELECTOR, "a[href='/d2l/home/35189']")


    
finally:
    # Close the browser
    driver.quit()