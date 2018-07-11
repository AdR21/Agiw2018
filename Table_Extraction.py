import urllib
import urllib.request
import csv

from bs4 import BeautifulSoup

import os

def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

soup = make_soup("http://au.shopping.com/sennheiser_pxc_250_ii_foldable_closed_back_stereo_mini_with_noiseguard_active_noise_cance_headphones/info")

#for record in soup.findAll('tbody'):
 #   for data in record.findAll('tr'):
        #for data in item.findAll(['th','td']):
  #      result = data.text.strip()
   # print(result)

#file = open(os.path.expanduser("aushopping1.csv"),"wb")
#file.write(bytes(result, encoding="ascii", errors='ignore'))


#for item in soup.findAll(['ul', 'p']):
 #   for object in item.findAll('li'):
  #      result1 = object.text.strip()
   #     print(result1)


csvfile="prova"

for record in soup.findAll("tr"):
    for data in record.findAll(["th","td"]):
        result=data.text.strip()
    print(result)

