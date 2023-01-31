from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
import time, requests
from tqdm import tqdm
import pandas as pd
import json


if __name__ == "__main__":
    webdriver_path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(webdriver_path)

    all_urls = []
    for idx in tqdm(range(1,10)):
        if idx == 1:
            url = "https://aero-naut.de/product-sitemap.xml"
        else:
            url = f"https://aero-naut.de/product-sitemap{idx}.xml"
        
        print(url)

        driver.get(url)
        time.sleep(5)
        table = driver.find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody")
        table_rows = table.find_elements(By.TAG_NAME, "tr")
        
        for table_row in table_rows:
            prod_url = table_row.find_element(By.TAG_NAME, 'a').get_attribute('href') 
            if prod_url.startswith("https://aero-naut.de/produkt/"):
                all_urls.append(prod_url)
        
        print(len(all_urls))
    
    print(len(all_urls))
    print(all_urls[:5])

    with open("product_urls.json", "w") as fp:
        json.dump(all_urls, fp)


