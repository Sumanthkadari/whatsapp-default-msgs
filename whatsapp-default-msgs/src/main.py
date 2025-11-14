from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import time
import pandas as pd

def make_driver(cfg):
    user_data_dir = cfg["chrome"]["user_data_dir"]
    profile_dir = cfg["chrome"]["profile_directory"]
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    subprocess.Popen([
        chrome_path,
        f"--user-data-dir={user_data_dir}",
        f"--profile-directory={profile_dir}",
        "--remote-debugging-port=9222",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        "--start-maximized"
    ])

    print(" Launching Chrome and connecting...")
    time.sleep(5)

    chrome_opts = Options()
    chrome_opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_opts)
    print(" Connected to existing Chrome session")

    driver.get("https://web.whatsapp.com")
    print("Opening WhatsApp Web...")
    time.sleep(10)
    return driver

# def send_message(driver, phone, message):
#     try:
#         url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
#         driver.get(url)
#         print(f" Opening chat for {phone}...")
#         time.sleep(10)

#         # Press Enter to send
#         send_btn = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label='Send']")
#         send_btn.click()
#         print(f" Message sent to {phone}")
#         time.sleep(5)
#     except Exception as e:
#         print(f"Failed to send message to {phone}: {e}")\
def send_message(driver, phone, message):
    try:
        url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
        driver.get(url)
        print(f" Opening chat for {phone}...")
        time.sleep(10)

        # Updated with your provided XPath
        send_btn = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div[5]/div/footer/div[1]/div/span/div/div[2]/div/div[4]/div/span/div/div/div[1]/div[1]/span"
        )
        send_btn.click()

        print(f" Message sent to {phone}")
        time.sleep(5)

    except Exception as e:
        print(f"Failed to send message to {phone}: {e}")


def main():
    # --- Config for your Chrome profile ---
    cfg = {
        "chrome": {
            "user_data_dir": r"C:\Users\AI ML PC Sumanth\AppData\Local\Google\Chrome\User Data\Profile 1", # change your profile here
            "profile_directory": "Default"
        }
    }

    # C:\Users\AI ML PC Sumanth\AppData\Local\Google\Chrome\User Data\Profile 3

    # --- Message and CSV ---
    message = (
    "📢 Notice – Leo Fitness Club\n"
    "Dear Members,\n"
    "Please note that Leo Fitness Club will remain closed tomorrow on account of Dasara festival.\n"
    "We will reopen on Friday morning at 5:30 AM as usual.\n"
    "Wishing you and your family a very Happy Dasara! 🎉💪\n"
    "– Team Leo Fitness Club")
    
    csv_path = r"contacts.csv"

    # --- Load contacts ---
    contacts = pd.read_csv(csv_path)

    # --- Start browser ---
    driver = make_driver(cfg)

    # --- Loop through all contacts ---
    for index, row in contacts.iterrows():
        phone = str(row['phone']).strip()
        send_message(driver, phone, message)

    print(" All messages sent successfully!")
    driver.quit()

if __name__ == "__main__":
    main()
