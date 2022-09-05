'''
#series - column
#dataframe - table
import pandas as pd
df = pd.read_excel("vgsales.xlsx")
#df.loc => column names
#df.iloc => column indices

for i in df.iterrows():
    #i is a tuple
    #i[0] is the row index
    #i[1] is a series
    print(i[1]["Name"])
    break
'''
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service_object = Service("WebDrivers\\chromedriver.exe")
browser = webdriver.Chrome(service = service_object)

#Web Scraping of Amazon Search Results

search_keyword = "espresso machine"

browser.get("https://www.amazon.com")
browser.find_element(By.ID,"twotabsearchtextbox").send_keys(search_keyword)
browser.find_element(By.ID,"twotabsearchtextbox").send_keys(Keys.ENTER)
#browser.find_element(By.ID,"nav-search-submit-button").click()

product_name = []
product_price = []
product_ratings = []
product_ratings_num = []
product_link = []

items = WebDriverWait(browser,15).\
    until(EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"s-result-item s-asin")]')))

print(len(items))

for item in items:
    #Adding Name
    name = item.find_element(By.XPATH, ".//span[@class='a-size-base-plus a-color-base a-text-normal']")
    product_name.append(name.text)

    #Adding Price
    try:
        price_whole = item.find_element(By.XPATH,".//span[@class='a-price-whole']")
        price_fraction = item.find_element(By.XPATH,".//span[@class='a-price-fraction']")
        price = ".".join([price_whole.text,price_fraction.text])
        product_price.append(price)
        #print(price_whole.text,price_fraction.text,sep='.')
    except NoSuchElementException:
        product_price.append("None")

    #Adding Ratings & Num_Ratings
    ratings = item.find_elements(By.XPATH,'.//div[@class="a-row a-size-small"]/span')
    if(len(ratings)!=0):
        #print(ratings[0].get_attribute('aria-label'))
        #print(ratings[1].get_attribute('aria-label'))
        product_ratings.append(ratings[0].get_attribute('aria-label')[0:3])
        product_ratings_num.append(ratings[1].get_attribute('aria-label'))
    else:
        product_ratings.append("None")
        product_ratings_num.append("None")

    #Adding Link

    #Add Description (Go to the link and find description)

print("Name Length",len(product_name),"Price Length",len(product_price),
      "Ratings Length",len(product_ratings),"Num Ratings Len",len(product_ratings_num))
print(product_name)
print(product_price)
print(product_ratings)
print(product_ratings_num)

import pandas as pd

di = {"Product Name": product_name,
      "Price in USD": product_price,
      "Ratings / 5":product_ratings,
      "Number of Ratings":product_ratings_num}

df = pd.DataFrame.from_dict(di)
filename = search_keyword+".xlsx"
df.to_excel(filename)