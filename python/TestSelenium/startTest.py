from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_yiche_sales():
    
    # 1. 启动浏览器（可配置为无头模式）
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # 无头模式，不显示界面
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=options)

    try:
        driver.get("https://car.yiche.com/salesranking/")
        # 2. 等待目标数据表格加载出现（关键！）
        wait = WebDriverWait(driver, 10)
        # 需要根据实际网页结构调整定位器，这里是一个示例
        #table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, ".rk-list-box")))
        htmlObj = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div .rk-list-box")))
        # 3. 获取页面源码并使用BeautifulSoup解析
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 4. 解析表格，提取数据到列表（此处需根据实际HTML结构调整）
        data = []
        rows = soup.select('.rk-list-box .rk-item')
        for row in rows:
            #print(row)
            carType = row.get('data-cxname', '')
            carPrice = row.find('div', class_='rk-car-price').text.strip() if row.find('div', class_='rk-car-price') else ''
            qty = row.find('span', class_='rk-car-num').text.strip() if row.find('span', class_='rk-car-num') else ''
            row_data = {
                'carType': carType,
                'carPrice': carPrice,
                'qty': qty
            }
            data.append(row_data)
            print(row_data)
            #if row_data:
            #    data.append(row_data)
        # 5. 转换为DataFrame
        #df = pd.DataFrame(data)
        #return df
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    sales_data = scrape_yiche_sales()
    print(sales_data)