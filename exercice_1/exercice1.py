#import modules
from lxml import html
import re
import requests
import pandas as pd
from datetime import datetime

#get html and tree
html_page_link = 'candidateEvalData/webpage.html'

with open(html_page_link, "r") as f:
    page = f.read()
tree = html.fromstring(page)

info_dict = {}

# parse artist name
artist = tree.xpath('//h1[@class="lotName"]')
# Extract name without birth year
info_dict["artist_name"] = re.findall("(.*)(?:\s\()",artist[0].text)[0]

#parse painting name
paint = tree.xpath('//h2[@class="itemName"]/i')
info_dict["paint_name"] = paint[0].text


#parse price GBP
price_gbp = tree.xpath('//*[contains(@id, "PriceRealizedPrimary")]')
info_dict["price_gbp"] = re.findall("(?:GBP\s)([\d,]*)",price_gbp[0].text)[0]

#parse price US
price_usd = tree.xpath('//*[contains(@id, "PriceRealizedSecondary")]')
info_dict["price_usd"] = re.findall("(?:USD\s)([\d,]*)",price_usd[0].text)[0]

#parse price GBP est
price_gbp = tree.xpath('//*[contains(@id, "PriceEstimatedPrimary")]')
info_dict["price_gbp_est"] = re.findall("(?:GBP\s)([\d,]*)",price_gbp[0].text)

#parse price US est
price_usd = tree.xpath('//*[contains(@id, "PriceEstimatedSecondary")]')
info_dict["price_usd_est"] = re.findall("(?:USD\s)([\d,]*)",price_usd[0].text)

#image link
imgs = tree.xpath('//img[@id="imgLotImage"]')
info_dict["image_link"] = imgs[0].attrib.get("src")

# Sale date
sale_date = tree.xpath('//*[contains(@id,"SaleDate")]')
info_dict["sale_date"] = (
    datetime.strptime(sale_date[0].text, "%d %B %Y, ")
    .strftime('%Y-%m-%d')
) 

# To dataframe
df = pd.DataFrame([info_dict])
# To file
df.to_csv("result_1.csv", index=None)