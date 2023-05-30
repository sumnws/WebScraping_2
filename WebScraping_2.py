from xml.dom import minidom
import requests
import json
import html
from bs4 import BeautifulSoup
import time
import pandas as pd


# parse an xml file by name
file = minidom.parse('sitemap_products_eng.xml')

#use getElementsByTagName() to get tag
url = file.getElementsByTagName('url')

# single item data
jsonUrl =url[1].getElementsByTagName('loc')[0].firstChild.nodeValue+"/products.json"

# list
list_title = []
list_option_name_real = []
list_option_real = []
list_description = []
list_details = []
list_one_image = []
list_image = []

index = 0
for index, elem in enumerate(url):
  if index < 800:
    jsonUrl =elem.getElementsByTagName('loc')[0].firstChild.nodeValue+"/products.json"
    jsonName = jsonUrl[len('https://hk.cozymatic.com/products/'):].replace('/','_')
    r = requests.get(jsonUrl, stream=True)
    with open("..\\json\\"+jsonName, 'wb') as out_file:
      out_file.write(r.content)

    def getSource(image):
        return image['src']

    # f = open("..\\json\\amandra-solid-wood-hook-rack_products.json")
    f = open("..\\json\\"+jsonName)
    # f = open("..\\json\\for-the-united-states-only-bradwell-solid-wood-tv-stand_products.json")
    # f = open("..\\json\\calandra-bottle-rack_products.json")
    try:
      data = json.load(f)
      # print(str(index)+":"+str(data))
      # index += 1
      # with open("amandra-solid-wood-hook-rack_products.txt", 'w', encoding='UTF-8') as out_file:
      
      # Append title 
      try:
        product = data['products'][0]
      except:
        product = data['product']
      list_title.append(product['title'])
      print(str(index)+"::: "+product['title'])
      # print(product['title'])
      # list_title.append(product['title'])
      # print(list_title)

      # Append option details
      list_option_name = []
      list_option = []
      try:
        options = product['options']
        for option in options:
          try:
            list_option_name.append(option['name'])
            # print(list_option_name)
          except:
            list_option_name.append("No option name")
          list_option.append(option['values'])
          # print(list_option)
      except:
        list_option_name.append("No option name")
        list_option.append("No option")
        list_title.append(product['title'])
      list_option_name_real.append(list_option_name)
      list_option_real.append(list_option)

      # Append description
      try:
        description = product['body_html'][:product['body_html'].index('Product Details')]
        soup = BeautifulSoup(description, 'html.parser')
        # print(soup)
        text = soup.get_text()
        list_description.append(text)
        # print(list_description)
      except:
        list_description.append("No text")

      # Append Product Details
      try:
        details = product['body_html'][product['body_html'].index('Product Details'):]
      except:
        details = product['body_html'][product['body_html'].index('Specifications'):]
      # print(details)
      soup = BeautifulSoup(details, 'html.parser')
      # trs = soup.find_all('td')
      tds = soup.find_all('td')
      lis = soup.find_all('li')

      # print("trs : "+ str(len(tds)))
      # print("lis : "+ str(len(lis)))
      tableContent = ""

      # if trs.size != 0:
      #   tableContent =tableContent+trs[0].text
      for index, td in enumerate(tds[1:]):
        if(index %2 == 0):
          tableContent =tableContent+ td.text.strip()+" : "
        else:
          tableContent =tableContent+td.text.strip()+"\n"
        # print(str(index) + row.text)
      for row in lis:
        tableContent +=row.text.strip()+"\n"
        # print(row.text)
      list_details.append(tableContent)
      # print(list_details)

      # Append image
      images  = product['images']
      list_one_image.append(images[0]['src'])
      list_image.append(", ".join(map(getSource,images))+"\n")
      # print(list_image)
      time.sleep(1.5)
    except:
      print(str(index)+":::")
    index =+ 1

data = {
  "Product Name": list_title,
  "Option Name": list_option_name_real,
  "Option": list_option_real,
  "Description": list_description,
  "Details": list_details,
  "Image": list_one_image,
  "All images": list_image
}

#load data into a DataFrame object:
df = pd.DataFrame(data)

# print(df) 
# df.info()
df.to_csv("All_product.csv")