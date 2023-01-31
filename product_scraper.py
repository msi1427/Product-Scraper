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

    with open("product_urls.json", "r") as fp:
        product_urls = json.load(fp)

    # product_urls = [
    #     "https://aero-naut.de/produkt/moewe-2-fischkutter/",
    #     "https://aero-naut.de/produkt/airmarine-special/",
    #     "https://aero-naut.de/produkt/alex-mehrzweckboot/",
    #     "https://aero-naut.de/produkt/beschlag-anna-2/",
    #     "https://aero-naut.de/produkt/anna-2-fischkutter/",
    #     "https://aero-naut.de/produkt/anna-3-fischkutter/",
    #     "https://aero-naut.de/produkt/bella-segelboot/",
    #     "https://aero-naut.de/produkt/ballast-bellissima/",
    #     "https://aero-naut.de/produkt/bellissima-segelboot/",
    #     "https://aero-naut.de/produkt/bert-schlepper/"
    # ]

    data = []
    for idx, product_url in enumerate(tqdm(product_urls)):
        driver.get(product_url)
        instance = {}
        if idx == 0: time.sleep(3)
        translate_element = driver.find_element(By.CLASS_NAME, "switcher")
        translate_element.click()
        time.sleep(1)
        translate_element = translate_element.find_element(By.CLASS_NAME, 'option')
        translate_options = translate_element.find_elements(By.TAG_NAME, 'a')
        for option in translate_options:
            if option.text == "Français":
                option.click()
                break
        time.sleep(1.5) 
        instance['UGS'] = ""

        product_title = driver.find_element(By.CLASS_NAME, "product_title").text
        instance['Nom'] = product_title

        instance['Description courte'] = ""

        try:
            description = driver.find_element(By.ID, "tab-description").text
        except:
            description = ""
        instance['Description'] = description

        try:
            price = driver.find_element(By.CLASS_NAME, "dtwpb-price").text
            price = price.split("€")[0]
        except:
            price = ""
        instance['Tarif régulier'] = price

        categories = driver.find_element(By.CLASS_NAME, "zm-breadcrumb").text
        categories = " > ".join(categories.split(" » ")[2:-1])
        instance['Catégories'] = categories

        images = []
        image_text = ""
        try:
            post_image_url = driver.find_element(By.CLASS_NAME, "wp-post-image").get_attribute('src')
            image_name = post_image_url.split("/")[-1]
            img = Image.open(requests.get(post_image_url, stream = True).raw)
            img.save(f"images\{image_name}")
            images.append(image_name)
            image_text = image_name
        except:
            image_text = ""
        try:
            image_list = driver.find_element(By.CLASS_NAME, "flex-control-nav")
            image_list = image_list.find_elements(By.TAG_NAME, "img")[1:4]
            for img_idx, image in enumerate(image_list): 
                image_url = image.get_attribute('src')
                image_name = image_url.split("/")[-1]
                images.append(image_name)
                image_text = image_text + ", " + image_name
                img = Image.open(requests.get(image_url, stream = True).raw)
                img.save(f"images\{image_name}")
        except:
            images = []
        instance['Images'] = image_text

        data.append(instance)
    
        df = pd.DataFrame(data=data, columns=data[0].keys())
        df.to_csv("Products.csv", index=False)

