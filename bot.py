from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time

# ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disk-cache-size=4096")  # Set the cache size
prefs = {"profile.managed_default_content_settings.images": 2, 
         "profile.managed_default_content_settings.stylesheets": 2}  # Disable CSS
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

# Log in
def login_to_website(username, password):
    driver.get('https://foreupsoftware.com/index.php/booking/19765/2431#teetimes')

    #Click the "Resident" button before login/ might have to be non resident
    try:
        resident_button = driver.find_element(By.XPATH, '//button[contains(text(), "Resident")]')  
        resident_button.click()
        print("Clicked on Resident button.")
        time.sleep(.5)  
    except Exception as e:
        print(f"Failed to click the Resident button: {e}")
        return
    
    try:
        log_button = driver.find_element(By.ID,'teetime-login')  
        log_button.click()
        print("Clicked on Login button.")
        time.sleep(.5)  
    except Exception as e:
        print(f"Failed to click the Login button: {e}")
        return

    username_input = driver.find_element(By.ID, 'login_email')
    password_input = driver.find_element(By.ID, 'login_password')

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn btn-primary') and text()='Log In']")

    login_button.click()

    time.sleep(2)

def search_for_tee_times(Preferred_Date, Preferred_Time_str):

    tee_time_course_selection = Select(driver.find_element(By.ID, 'schedule_select'))
    tee_time_course_selection.select_by_visible_text('Bethpage 9 Holes Midday Front 9')
    
    date_selection = driver.find_element(By.ID, 'date-field')
    date_selection.click()
    date_selection.send_keys(Keys.CONTROL, 'a')
    date_selection.send_keys(Keys.BACKSPACE)
    date_selection.send_keys(Preferred_Date)
    date_selection.send_keys(Keys.ENTER)
    
    time.sleep(.5)
    
    preferred_time = datetime.strptime(Preferred_Time_str, '%I:%M %p')

    tee_time_elements = driver.find_elements(By.CSS_SELECTOR, '.js-times .time-tile')

    closest_time_element = None
    closest_time_difference = None

    for tee_time_element in tee_time_elements:
        time_label_element = tee_time_element.find_element(By.CSS_SELECTOR, '.booking-start-time-label')
        tee_time_str = time_label_element.text.strip()

        try:
            tee_time = datetime.strptime(tee_time_str, '%I:%M%p')
            
            time_difference = abs((preferred_time - tee_time).total_seconds())

            if closest_time_difference is None or time_difference < closest_time_difference:
                closest_time_difference = time_difference
                closest_time_element = tee_time_element  

        except ValueError:
            print(f"Could not parse time: {tee_time_str}")

    if closest_time_element:
        print(f"Clicking on the closest tee time: {closest_time_element.text}")
        closest_time_element.click()  
    else:
        print("No available tee times found.")
        
def book_tee_time(players):

    time.sleep(.8)
    try:
        container = driver.find_element(By.CSS_SELECTOR, "div.js-booking-field-buttons[data-field='players']")
        
        if players == 4:
            button = container.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[data-value='4']")
            button.click()
            print("Selected 4 players.")
        elif players == 3:
            button = container.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[data-value='3']")
            button.click()
            print("Selected 3 players.")
        elif players == 2:
            button = container.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[data-value='2']")
            button.click()
            print("Selected 2 players.")
        else:
            button = container.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[data-value='1']")
            button.click()
            print("Selected 1 players.")
    except NoSuchElementException:
        print("Button for 4 players not found.")
        
    book_now_button = driver.find_element(By. CSS_SELECTOR, 'button.btn.btn-success.js-book-button')
    #book_now_button.click()

if __name__ == "__main__":
    USERNAME = "markmmnashed@gmail.com"
    PASSWORD = Password
    PREFERRED_TEE_TIME = "09:00 AM"

    login_to_website(USERNAME, PASSWORD)
    #run_booking_bot(USERNAME, PASSWORD, PREFERRED_TEE_TIME)
    search_for_tee_times('10-15-2024', '3:06 PM')
    book_tee_time(1)

    input("Close the program")
