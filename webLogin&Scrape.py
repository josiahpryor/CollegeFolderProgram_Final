login_url = "https://suadfs1.shepherd.edu/adfs/ls/?SAMLRequest=jdE7b4MwEADgvVL%2fg%2bUdjG0C2IJIUbtESpek7dClMnAEJLCpz1T9%2bSWN%2bhi73UMnfXdX7pbQ2yO8LYCB7O8rimYa%2fTV%2f5YmEpOOZ4apOAYpiY7KirkVS51lrZEvJM3gcnK2oiBNK9ogL7C0GY8NaSkQacR7x%2fJFLLbgWMpYyk5ts80LJDhF8WGfvnMVlAn8C%2fz408HQ8VLQPYUbNWO2Hcx9wNg3E2MPcg29jaBfWipGNMzOrno3uPFh2cR8uUbz2KPmYRosVXbzVzuCA2poJUIdGn3YPB71y9exdcI0b6fb2hpDyC%2b%2f%2fM2i%2b6XT7A5Wp6JIuj6TIkygtVBepQtWRapURSklZiCYOYNfDYPx3q8ZNv%2fSSXRErqGR%2fP7P9BA%3d%3d&RelayState=%2fd2l%2fhome"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    css_selector_for_host1 = "#d2l_1_15_896"
    css_selector_for_host2 = "d2l-my-courses-container"
    css_selector_for_host3 = "d2l-tabs:nth-child(7) > d2l-tab-panel:nth-child(3) > d2l-my-courses-content:nth-child(1)"
    css_selector_for_host4 = "d2l-my-courses-card-grid"
    css_selector_for_host5 = "d2l-enrollment-card[href='https://b342f0f7-3270-489f-989b-9d9a2993382c.enrollments.api.brightspace.com/enrolled-user/uYvgzO3OgKP7aqqAgNARJiGl_0nNmt68TX2I6yMJ1h0/enrollment?localeId=1']"
    css_selector_for_host6 = "d2l-card[text='202430 - CIS 332 01 - Web Programming I, off.202430.30093, 202430 - Fall 2024-2025, Ends December 21, 2024 at 12:00 AM']"



    time.sleep(1)
    shadow0 = driver.find_element(By.CSS_SELECTOR, css_selector_for_host1).shadow_root
    # time.sleep(1)
    # shadow1 = shadow0.find_element(By.CSS_SELECTOR, css_selector_for_host2).shadow_root
    # time.sleep(1)
    # shadow2 = shadow1.find_element(By.CSS_SELECTOR, css_selector_for_host3).shadow_root
    # time.sleep(1)
    # shadow3 = shadow2.find_element(By.CSS_SELECTOR, css_selector_for_host4).shadow_root
    # time.sleep(1)
    # shadow4 = shadow3.find_element(By.CSS_SELECTOR, css_selector_for_host5).shadow_root
    # time.sleep(1)
    # shadow5 = shadow4.find_element(By.CSS_SELECTOR, css_selector_for_host6).shadow_root
    # time.sleep(1)
    # shadow5.find_element(By.CSS_SELECTOR, "a[href='/d2l/home/34862']")


    
finally:
    # Close the browser
    driver.quit()