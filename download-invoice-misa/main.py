from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, urllib.request

def main():
    URL_TRA_CUU = "https://www.meinvoice.vn/tra-cuu"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    THU_MUC_TAI_VE = os.path.join(BASE_DIR, "downloads")
    os.makedirs(THU_MUC_TAI_VE, exist_ok=True)

    code_file = os.path.join(BASE_DIR, "code.txt")
    with open(code_file, "r", encoding="utf-8") as f:
        danh_sach_ma = [line.strip() for line in f if line.strip()]

    options = Options()
    prefs = {
        "download.default_directory": THU_MUC_TAI_VE,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    try:
        for MA_TRA_CUU in danh_sach_ma:
            print(f"Đang xử lý mã: {MA_TRA_CUU}")
            driver.get(URL_TRA_CUU)

            input_code = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "txtCode"))
            )
            input_code.clear()
            input_code.send_keys(MA_TRA_CUU)

            driver.find_element(By.ID, "btnSearchInvoice").click()

            def wait_pdf(driver):
                try:
                    iframe = driver.find_element(By.ID, "frmResult")
                    url = iframe.get_attribute("src")
                    return url and f"Code={MA_TRA_CUU}" in url
                except:
                    return False

            WebDriverWait(driver, 20).until(wait_pdf)

            iframe = driver.find_element(By.ID, "frmResult")
            pdf_url = iframe.get_attribute("src")

            if pdf_url:
                filename = os.path.join(THU_MUC_TAI_VE, f"{MA_TRA_CUU}.pdf")
                urllib.request.urlretrieve(pdf_url, filename)
                print(f"Đã tải: {filename}")
            else:
                print(f"Không tìm thấy PDF cho mã: {MA_TRA_CUU}")

            time.sleep(2)

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        driver.quit()
        print("Đã hoàn tất.")

if __name__ == "__main__":
    main()
