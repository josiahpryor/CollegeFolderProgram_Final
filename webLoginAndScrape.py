from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

def scrape():
    #Shepherd brightspace login url
    login_url = "https://suadfs1.shepherd.edu/adfs/ls/?SAMLRequest=jdE7b4MwEADgvVL%2fg%2bUdjG0C2IJIUbtESpek7dClMnAEJLCpz1T9%2bSWN%2bhi73UMnfXdX7pbQ2yO8LYCB7O8rimYa%2fTV%2f5YmEpOOZ4apOAYpiY7KirkVS51lrZEvJM3gcnK2oiBNK9ogL7C0GY8NaSkQacR7x%2fJFLLbgWMpYyk5ts80LJDhF8WGfvnMVlAn8C%2fz408HQ8VLQPYUbNWO2Hcx9wNg3E2MPcg29jaBfWipGNMzOrno3uPFh2cR8uUbz2KPmYRosVXbzVzuCA2poJUIdGn3YPB71y9exdcI0b6fb2hpDyC%2b%2f%2fM2i%2b6XT7A5Wp6JIuj6TIkygtVBepQtWRapURSklZiCYOYNfDYPx3q8ZNv%2fSSXRErqGR%2fP7P9BA%3d%3d&RelayState=%2fd2l%2fhome"

    # Set up the driver (e.g., ChromeDriver)
    driver = webdriver.Chrome()

    # Load the webpage
    driver.get(login_url)

    try:

        #Css selectors that drill down to class name info
        css_selector_for_host1 = "d2l-my-courses"
        css_selector_for_host2 = "d2l-my-courses-container"
        css_selector_for_host3 = "d2l-tabs > d2l-tab-panel:nth-child(3) > d2l-my-courses-content" #current semester
        css_selector_for_host4 = "d2l-my-courses-card-grid"
        css_selector_for_host5 = ".course-card-grid.columns-2 > d2l-enrollment-card:nth-child(2)" #different enrollment cards for diff. classes
        css_selector_for_host6 = "d2l-card" #holds class info

        #waits for first selector to load
        WebDriverWait(driver, 30).until( EC.visibility_of_element_located((By.TAG_NAME, css_selector_for_host1)) )

        #Process of drilling down through shadow_roots to get to class info
        start = driver.find_element(By.TAG_NAME, css_selector_for_host1)
        shadow0 = start.shadow_root
        shadow1 = shadow0.find_element(By.CSS_SELECTOR, css_selector_for_host2).shadow_root
        time.sleep(1)
        shadow2 = shadow1.find_element(By.CSS_SELECTOR, css_selector_for_host3).shadow_root
        time.sleep(1)
        shadow3 = shadow2.find_element(By.CSS_SELECTOR, css_selector_for_host4).shadow_root

        
        classes = shadow3.find_elements(By.CSS_SELECTOR, "d2l-enrollment-card")#finds sections that contain class info
        num_classes = len(classes) #number of sections that will contain class info
        class_num = 1 #Used for iterator through classes
        all_class_text = "" #for appending class text

        #Goes through sections containing class info
        for Class in classes:
            #drills down into each class section individually
            shadow4 = shadow3.find_element(By.CSS_SELECTOR, f".course-card-grid.columns-2 > d2l-enrollment-card:nth-child({class_num})").shadow_root
            class_num += 1
            #collects class text
            class_text = shadow4.find_element(By.CSS_SELECTOR, "d2l-card").text
            all_class_text += class_text #appends

        return all_class_text #messy class text
            
    finally:
        # Close the browser
        driver.quit()

def organize(all_class_text):

    #reg expression to find neat class names
    pattern = r"\w{3,4} \d{3} \d{2} - [^,]*" 

    matches = re.findall(pattern, all_class_text)
    
    #creates set of class names
    unique_classes = set(match.strip() for match in matches)
    return unique_classes
    
def collectClasses():
    messy_class_text = scrape()
    class_set = organize(messy_class_text)
    return class_set
def sample():
    sample = {'COMM 202 06 - Fund of Speech', 'CIS 321 01 - Data & File Structures', 'CIS 302 01 - Windows Programming', 'CIS 314 01 - Adv Computer Lang Concepts', 'CIS 332 01 - Web Programming I'}
    return sample

if __name__ == "__main__":
    test = collectClasses()
    print(test)