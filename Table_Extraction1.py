import csv
import json
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

#html = urlopen("http://au.shopping.com/sennheiser-sennheiser-hd239-on-ear-stereo-headphones-with-open-air-design-for-high-resolution-stereo-sound/info")
with open("cleanedurls.json") as urls:
    sites = json.load(urls)
for domain in sites:
    print(domain)
    values = sites[domain]
    if len(values) != 0:
        if os.path.exists(domain):
            os.mkdir(domain)
        i=0
        for sites in values:
            html = urlopen(sites)
            bsObj = BeautifulSoup(html,"lxml")
            table = bsObj.findAll("table", {"class":""})[0]
            rows = table.findAll("tr")
            csvFile = open(str(i)+ ".csv",'wt', newline='')
            writer = csv.writer(csvFile)
            try:
                for row in rows:
                    csvRow = []
                    for cell in row.findAll(['th', 'td']):
                        csvRow.append(cell.get_text().strip())
                        writer.writerow(csvRow)
            finally:
                i += 1
                csvFile.close()