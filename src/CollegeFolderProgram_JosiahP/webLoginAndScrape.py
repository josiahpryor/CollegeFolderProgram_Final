from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# Create global var. for shadow3. Found in drilling, needed in class extraction
shadow3 = ""
# Define constants for the CSS selectors
CSS_SELECTORS = {
    "host1": "d2l-my-courses",
    "host2": "d2l-my-courses-container",
    "host3": "d2l-tabs > d2l-tab-panel:nth-child(3) > d2l-my-courses-content",  # Current semester
    "host4": "d2l-my-courses-card-grid",
    "host5": ".course-card-grid.columns-2 > d2l-enrollment-card:nth-child(2)",  # Different enrollment cards for different classes
    "host6": "d2l-card"  # Holds class info
}

# Shepherd Brightspace login URL
LOGIN_URL = "https://suadfs1.shepherd.edu/adfs/ls/?SAMLRequest=jdE7b4MwEADgvVL%2fg%2bUdjG0C2IJIUbtESpek7dClMnAEJLCpz1T9%2bSWN%2bhi73UMnfXdX7pbQ2yO8LYCB7O8rimYa%2fTV%2f5YmEpOOZ4apOAYpiY7KirkVS51lrZEvJM3gcnK2oiBNK9ogL7C0GY8NaSkQacR7x%2fJFLLbgWMpYyk5ts80LJDhF8WGfvnMVlAn8C%2fz408HQ8VLQPYUbNWO2Hcx9wNg3E2MPcg29jaBfWipGNMzOrno3uPFh2cR8uUbz2KPmYRosVXbzVzuCA2poJUIdGn3YPB71y9exdcI0b6fb2hpDyC%2b%2f%2fM2i%2b6XT7A5Wp6JIuj6TIkygtVBepQtWRapURSklZiCYOYNfDYPx3q8ZNv%2fSSXRErqGR%2fP7P9BA%3d%3d&RelayState=%2fd2l%2fhome"

def init_driver():
    """Initialize and return the Chrome WebDriver."""
    return webdriver.Chrome()

def wait_for_element(driver, css_selector, timeout=30):
    """Wait for an element to become visible based on the given CSS selector."""
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.TAG_NAME, css_selector)))

def drill_down_to_classes(driver):
    """Navigate through the shadow DOM and return class elements."""
    start = driver.find_element(By.TAG_NAME, CSS_SELECTORS["host1"])
    shadow0 = start.shadow_root # First shadow drill
    shadow1 = shadow0.find_element(By.CSS_SELECTOR, CSS_SELECTORS["host2"]).shadow_root
    time.sleep(1)  # Ensures shadow loaded
    shadow2 = shadow1.find_element(By.CSS_SELECTOR, CSS_SELECTORS["host3"]).shadow_root
    time.sleep(1)
    global shadow3 # Used in class extraction
    shadow3 = shadow2.find_element(By.CSS_SELECTOR, CSS_SELECTORS["host4"]).shadow_root

    # Return the class elements inside the shadow DOM
    return shadow3.find_elements(By.CSS_SELECTOR, "d2l-enrollment-card") # List of sections containing class info

def extract_class_text(classes):
    """Extract and return the text content of each class."""
    num_classes = len(classes) # Number of sections that will contain class info
    class_num = 1 # Used for iterator through classes
    all_class_text = "" # For appending class text

    for Class in classes:
        # Drills down into each class section individually
        shadow4 = shadow3.find_element(By.CSS_SELECTOR, f".course-card-grid.columns-2 > d2l-enrollment-card:nth-child({class_num})").shadow_root
        class_num += 1
        # Collects class text
        class_text = shadow4.find_element(By.CSS_SELECTOR, CSS_SELECTORS["host6"]).text
        all_class_text += class_text  # Append each class's text
    return all_class_text

def scrape():
    """Scrape the classes from the Shepherd Brightspace website."""
    # Inits brightspace login web with chrome
    driver = webdriver.Chrome()
    driver.get(LOGIN_URL)

    try:
        #Waits 30 seconds for starting element to load
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.TAG_NAME, CSS_SELECTORS["host1"]))) 
        classes = drill_down_to_classes(driver)  # Get class elements from the shadow DOM
        return extract_class_text(classes)  # Return all class text

    finally:
        driver.quit()  # Ensure the driver is quit even if an exception occurs

def organize(all_class_text):
    """Organize and extract unique class names from the messy text."""
    pattern = r"\w{3,4} \d{3} \d{2} - [^,]*"  # Regular expression to match class names
    matches = re.findall(pattern, all_class_text)

    # Create a set of unique class names
    return set(match.strip() for match in matches)

def collect_classes():
    """Collect and return a set of unique class names."""
    unorganized_class_text = scrape()
    return organize(unorganized_class_text)

def sample_classes():
    """What the class tuple should appear as."""
    return {
        'COMM 202 06 - Fund of Speech',
        'CIS 321 01 - Data & File Structures',
        'CIS 302 01 - Windows Programming',
        'CIS 314 01 - Adv Computer Lang Concepts',
        'CIS 332 01 - Web Programming I'
    }

if __name__ == "__main__":
    organized_class_tuple = collect_classes()
    print(organized_class_tuple)
