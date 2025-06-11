import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

base_url = "https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep"
driver.get(base_url)

time.sleep(2)

pagination = driver.find_elements(By.CSS_SELECTOR, "ul.pagination li.page-item a.page-link")

page_urls = []
page_urls.insert(0, base_url)
for link in pagination:
    url = link.get_attribute("href")
    if url and "page=" in url and url not in page_urls:
        page_urls.append(url)

print(f"Có {len(page_urls)} trang.")

all_sheets_data = {}

for i, page_url in enumerate(page_urls, start=1):
    time.sleep(2)

    print(f"Đang xử lý trang {i} - {page_url}")
    driver.get(page_url)

    rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")

    results = []

    for row in rows:
        try:
            mst_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a strong")
            mst = mst_element.text.strip()

            name_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(3) div a")
            name = name_element.text.strip()

            date_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
            date = date_element.text.strip()

            results.append({
                "Mã số thuế": mst,
                "Tên doanh nghiệp": name,
                "Ngày cấp": date
            })
        except Exception as e:
            continue

    df = pd.DataFrame(results)
    all_sheets_data[f"Trang_{i}"] = df

driver.quit()

with pd.ExcelWriter("doanh_nghiep.xlsx") as writer:
    for sheet_name, df in all_sheets_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Tạo 'doanh_nghiep.xlsx'")
