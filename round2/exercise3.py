import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Danh sách tài khoản
usernames = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]
password = "secret_sauce"

chrome_options = Options()
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

product_data = []

for username in usernames:
    driver.get("https://www.saucedemo.com")

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    time.sleep(1)

    if driver.find_elements(By.CLASS_NAME, "error-button"):
        print(f"Đăng nhập thất bại: [{username}]")
        continue

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
        print(f"Đăng nhập thành công: [{username}]")
    except TimeoutException:
        print(f"Tải sản phẩm quá lâu: [{username}]")
        continue

    items = driver.find_elements(By.CLASS_NAME, "inventory_item")

    for item in items:
        try:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
            desc = item.find_element(By.CLASS_NAME, "inventory_item_desc").text

            product_data.append({
                "Username": username,
                "Product Name": name,
                "Price": price,
                "Description": desc
            })
        except NoSuchElementException:
            continue

driver.quit()

df = pd.DataFrame(product_data)
df.to_excel("products.xlsx", index=False)
print("Tạo 'products.xlsx'")
