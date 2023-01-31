# Product-Scraper

This is a client project. The client's requirement was to get product details and images from https://aero-naut.de/ 

## Build From Sources and Run the Selenium Scraper
1. Clone the repo
```bash
git clone https://github.com/msi1427/Product-Scraper.git
```
2. Intialize and activate virtual environment
```bash
virtualenv --no-site-packages  venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Download Chrome WebDrive from https://chromedriver.chromium.org/downloads 
5. Run the `url_scraper` to get all the product urls. You will get a file `product_urls.json` containing the list of product urls
```bash
python url_scraper.py
```
6. Run the `product_scraper` to get all the product details and images. 

  ```bash
  python product_scraper.py
  ```

7. You will get a file named `Products.csv` containing all the required fields. The product images will be stored in `images` folder.
   
  Alternatively, check a snippet of scraped data here: https://github.com/msi1427/Product-Scraper/blob/main/Products.csv