from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time, os, shutil
import xml.etree.ElementTree as ET


def setup_chrome_driver(download_dir):
    options = Options()
    options.add_argument("--safebrowsing-disable-download-protection")
    prefs = {
        "safebrowsing.enabled": True,
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=options)


def create_invoice_folder(base_dir, invoice_code):
    invoice_dir = os.path.join(base_dir, invoice_code)
    os.makedirs(invoice_dir, exist_ok=True)
    return invoice_dir


def move_downloaded_files(temp_dir, target_dir, invoice_code, extensions):
    for ext in extensions:
        for filename in os.listdir(temp_dir):
            if filename.endswith(ext):
                src = os.path.join(temp_dir, filename)
                dst = os.path.join(target_dir, f"{invoice_code}{ext}")
                try:
                    shutil.move(src, dst)
                    print(f"Đã di chuyển {filename} -> {dst}")
                except Exception as e:
                    print(f"Lỗi di chuyển file {filename}: {e}")

# =======
# MEINVOICE

def handle_meinvoice(driver, invoice_code, temp_dir, target_dir):
    try:
        input_code = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "txtCode"))
        )
        input_code.clear()
        input_code.send_keys(invoice_code)
        driver.find_element(By.ID, "btnSearchInvoice").click()
        time.sleep(3)
        
        if check_meinvoice_error(driver, invoice_code):
            return False
            
        if download_meinvoice_files(driver, invoice_code):
            time.sleep(3)
            move_downloaded_files(temp_dir, target_dir, invoice_code, ['.pdf', '.xml'])
            return True
        
    except Exception as e:
        print(f"Lỗi xử lý meinvoice cho mã {invoice_code}: {e}")
    return False


def check_meinvoice_error(driver, invoice_code):
    try:
        error_modal = driver.find_elements(By.CSS_SELECTOR, "div[aria-describedby='showPopupInvoicNotExist']")
        if error_modal and "display: none" not in error_modal[0].get_attribute("style"):
            print(f"Không tìm thấy hóa đơn cho mã: {invoice_code}")
            close_modal(driver, "button.btn-close-invoiceerror")
            return True
            
        error_text = driver.find_elements(By.XPATH, "//div[@id='popup-invoicnotexist-content']//div[contains(text(), 'Không tìm thấy hóa đơn')]")
        if error_text and error_text[0].is_displayed():
            print(f"Không tìm thấy hóa đơn cho mã: {invoice_code}")
            close_modal(driver, "button.btn-close-invoiceerror")
            return True
    except Exception as e:
        print(f"Lỗi kiểm tra modal: {e}")
    return False


def close_modal(driver, selector):
    try:
        close_button = driver.find_element(By.CSS_SELECTOR, selector)
        close_button.click()
        time.sleep(1)
    except Exception as e:
        print(f"Không thể đóng modal: {e}")


def download_meinvoice_files(driver, invoice_code):
    try:
        download_button = driver.find_element(By.CSS_SELECTOR, "div.res-btn.download")
        
        download_button.click()
        time.sleep(1)
        try:
            pdf_option = driver.find_element(By.CSS_SELECTOR, "div.dm-item.pdf.txt-download-pdf")
            pdf_option.click()
            print(f"Đã tải PDF cho mã: {invoice_code}")
            time.sleep(2)
        except Exception as e:
            print(f"Không thể tải PDF cho mã {invoice_code}: {e}")
        
        download_button.click()
        time.sleep(1)
        try:
            xml_option = driver.find_element(By.CSS_SELECTOR, "div.dm-item.xml.txt-download-xml")
            xml_option.click()
            print(f"Đã tải XML cho mã: {invoice_code}")
            time.sleep(2)
        except Exception as e:
            print(f"Không thể tải XML cho mã {invoice_code}: {e}")
        
        return True
    except Exception as e:
        print(f"Không thể tìm thấy nút tải hóa đơn cho mã {invoice_code}: {e}")
        return False

# =======
# EHOADON

def handle_ehoadon(driver, invoice_code, temp_dir, target_dir):
    try:
        input_ma_tra_cuu = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "txtInvoiceCode"))
        )
        input_ma_tra_cuu.clear()
        input_ma_tra_cuu.send_keys(invoice_code)
        
        btn_tra_cuu = driver.find_element(By.ID, "Button1")
        btn_tra_cuu.click()
        time.sleep(3)
        
        if check_ehoadon_error(driver, invoice_code):
            return False
            
        if download_ehoadon(driver, invoice_code):
            time.sleep(3)
            move_downloaded_files(temp_dir, target_dir, invoice_code, ['.pdf'])
            return True
            
    except Exception as e:
        print(f"Lỗi khi xử lý ehoadon.vn cho mã {invoice_code}: {e}")
    return False


def check_ehoadon_error(driver, invoice_code):
    try:
        # Chờ tối đa 5s xem popup lỗi có hiện không
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'ui-dialog') and contains(@class, 'ui-draggable') and not(contains(@style, 'display: none'))]"
            ))
        )
        print(f"Không tìm thấy hóa đơn cho mã: {invoice_code}")
        return True
    except:
        return False


def download_ehoadon(driver, invoice_code):
    try:
        dropdown_menu = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#divDownloads ul.dropdown-menu.pull-right"))
        )

        driver.execute_script(
            "arguments[0].style.setProperty('display', 'block', 'important');", dropdown_menu
        )
        
        try:
            pdf_link = driver.find_element(By.ID, "LinkDownPDF")
            pdf_link.click()
            print(f"Đã tải PDF cho mã: {invoice_code}")
            time.sleep(2)
        except Exception as e:
            print(f"Không thể tải PDF cho mã {invoice_code}: {e}")
        
        driver.execute_script("arguments[0].style.display = 'block';", dropdown_menu)
        time.sleep(1)
        
        try:
            xml_link = driver.find_element(By.ID, "LinkDownXML")
            xml_link.click()
            print(f"Đã tải XML cho mã: {invoice_code}")
            time.sleep(2)
        except Exception as e:
            print(f"Không thể tải XML cho mã {invoice_code}: {e}")
        
        return True
    except Exception as e:
        print(f"Không tìm thấy dropdown menu cho mã {invoice_code}: {e}")
        return False

# =======
# FPT

def handle_fpt_tracuu(driver, invoice_code, tax_code, temp_dir, target_dir):
    if not tax_code or tax_code.lower() == "nan":
        print(f"Bỏ qua vì thiếu mã số thuế cho mã tra cứu {invoice_code}")
        return False
    
    try:
        input_mst = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='MST bên bán']"))
        )
        input_ma = driver.find_element(By.XPATH, "//input[@placeholder='Mã tra cứu hóa đơn']")
        
        input_mst.clear()
        input_ma.clear()
        input_mst.send_keys(tax_code)
        input_ma.send_keys(invoice_code)
        
        driver.find_element(By.XPATH, "//button[.//span[contains(@class, 'wxi-search')]]").click()
        time.sleep(3)
        
        if check_fpt_error(driver, invoice_code):
            return False
            
        if download_fpt_files(driver, invoice_code):
            time.sleep(5)
            move_downloaded_files(temp_dir, target_dir, invoice_code, ['.xml', '.pdf', '.xls'])
            return True
            
    except Exception as e:
        print(f"Lỗi khi tra cứu trên FPT cho mã {invoice_code}: {e}")
    return False


def check_fpt_error(driver, invoice_code):
    try:
        error_modal = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'ui-dialog') and contains(@class, 'ui-widget-content')]//div[@id='Bkav_alert_dialog']"
            ))
        )
        
        error_content = error_modal.find_element(By.XPATH, ".//div[contains(text(), 'không đúng')]")
        if error_content:
            print(f"Mã tra cứu {invoice_code} không đúng hoặc không tồn tại")
            close_modal(driver, "//button[contains(@class, 'btn-primary') and contains(text(), 'Đóng')]")
            return True
            
    except TimeoutException:
        pass
    return False


def download_fpt_files(driver, invoice_code):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//ul[contains(@class, 'dropdown-menu')]//a[@id='LinkDownXML' or @id='LinkDownPDF']"
            ))
        )
        
        print(f"Tìm thấy hóa đơn cho mã {invoice_code}, bắt đầu tải file")
        
        download_fpt_file(driver, "LinkDownXML", "XML", invoice_code)
        download_fpt_file(driver, "LinkDownPDF", "PDF", invoice_code)
        download_fpt_file(driver, "LinkDownXLS", "XLS", invoice_code)
        
        return True
    except TimeoutException:
        print(f"Không tìm thấy menu download cho mã {invoice_code}")
        return False


def download_fpt_file(driver, link_id, file_type, invoice_code):
    try:
        link = driver.find_element(By.XPATH, f"//a[@id='{link_id}']")
        if link.is_displayed():
            link.click()
            print(f"Đã bấm tải {file_type} cho mã {invoice_code}")
            time.sleep(3)
    except Exception as e:
        print(f"Không thể tải {file_type} cho mã {invoice_code}: {e}")

# =======

def selenium_tai_xml(df, base_download_dir):
    temp_download_dir = os.path.join(base_download_dir, "temp")
    os.makedirs(temp_download_dir, exist_ok=True)
    
    driver = setup_chrome_driver(temp_download_dir)

    try:
        for idx, row in df.iterrows():
            invoice_code = str(row["Mã tra cứu"]).strip()
            url_tracuu = str(row["URL"]).strip()
            tax_code = str(row.get("Mã số thuế", "")).strip()

            print(f"Đang xử lý mã: {invoice_code} - URL: {url_tracuu}")
            
            target_dir = create_invoice_folder(base_download_dir, invoice_code)
            driver.get(url_tracuu)

            success = False
            if "meinvoice.vn" in url_tracuu:
                success = handle_meinvoice(driver, invoice_code, temp_download_dir, target_dir)
            if "ehoadon.vn" in url_tracuu:
                success = handle_ehoadon(driver, invoice_code, temp_download_dir, target_dir)
            elif "tracuuhoadon.fpt.com" in url_tracuu:
                success = handle_fpt_tracuu(driver, invoice_code, tax_code, temp_download_dir, target_dir)
            else:
                print(f"Không hỗ trợ trang: {url_tracuu}")

            if not success:
                try:
                    os.rmdir(target_dir)
                except:
                    pass

            time.sleep(2)

    except Exception as e:
        print(f"Lỗi trong quá trình Selenium: {e}")
    finally:
        driver.quit()
        shutil.rmtree(temp_download_dir, ignore_errors=True)
        print("Đã hoàn tất phần Selenium - tải file")


def parse_xml_va_xuat_excel(df, thu_muc_tai_ve):
    print("\nBắt đầu parse XML và tạo file kết quả...")
    
    ket_qua_rows = []
    
    for idx, row in df.iterrows():
        invoice_code = str(row["Mã tra cứu"]).strip()
        tax_code = str(row["Mã số thuế"]).strip()
        url_tim_kiem = str(row["URL"]).strip()
        
        row_kq = {
            "STT": idx + 1,
            "Mã số thuế": tax_code,
            "Mã Tra cứu": invoice_code,
            "URL": url_tim_kiem,
            "Số hóa đơn": "",
            "Đơn vị bán hàng": "",
            "Mã số thuế (ghi tiếp)": "",
            "Địa chỉ": "",
            "Điện thoại": "",
            "Số tài khoản": "",
            "Họ tên người mua hàng": "",
            "Địa chỉ (người mua)": "",
            "Số tài khoản (người mua)": "",
        }
        
        xml_file = os.path.join(thu_muc_tai_ve, invoice_code, f"{invoice_code}.xml")
        
        if os.path.exists(xml_file):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                row_kq["Số hóa đơn"] = root.findtext(".//SHDon") or ""
                row_kq["Đơn vị bán hàng"] = root.findtext(".//NBan/Ten") or ""
                row_kq["Mã số thuế (ghi tiếp)"] = root.findtext(".//NBan/MST") or ""
                row_kq["Địa chỉ"] = root.findtext(".//NBan/DChi") or ""
                row_kq["Điện thoại"] = root.findtext(".//NBan/SDThoai") or ""
                row_kq["Họ tên người mua hàng"] = root.findtext(".//NMua/Ten") or ""
                row_kq["Địa chỉ (người mua)"] = root.findtext(".//NMua/DChi") or ""

                print(f"Đã parse XML cho mã {invoice_code} thành công.")

            except Exception as e:
                print(f"Lỗi khi parse XML cho mã {invoice_code}: {e}")
        else:
            print(f"Không tìm thấy file XML cho mã: {invoice_code}")
        
        ket_qua_rows.append(row_kq)

    if ket_qua_rows:
        df_out = pd.DataFrame(ket_qua_rows)
        output_file = "ket_qua.xlsx"
        df_out.to_excel(output_file, index=False)
        print(f"Đã lưu file {output_file} với {len(ket_qua_rows)} dòng.")
        print(f"Trong đó có {len([r for r in ket_qua_rows if r['Số hóa đơn']])} dòng có thông tin XML.")
    else:
        print("Không có dữ liệu để xuất Excel.")


def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    THU_MUC_TAI_VE = os.path.join(BASE_DIR, "downloads")
    os.makedirs(THU_MUC_TAI_VE, exist_ok=True)

    file_excel = os.path.join(BASE_DIR, "input.xlsx")
    try:
        df = pd.read_excel(file_excel, dtype={"Mã số thuế": str, "Mã tra cứu": str})
        print(f"Đã đọc file {file_excel} với {len(df)} dòng dữ liệu")
    except Exception as e:
        print(f"Lỗi khi đọc file Excel: {e}")
        return
    
    selenium_tai_xml(df, THU_MUC_TAI_VE)
    parse_xml_va_xuat_excel(df, THU_MUC_TAI_VE)
    
    print("\nHOÀN TẤT TẤT CẢ!")


if __name__ == "__main__":
    main()