import csv
import json
import os
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from tqdm import tqdm


class CsvExtractor:
    _prefix = "tv_csv/"
    _MAXIMUM_TEXT_LENGTH = 10

    def __init__(self):
        pass

    def extract(self):
        with open("cleanedurls_tv.json") as urls:
            sites = json.load(urls)
            print("%s" % sites)
        for domain in tqdm(sites):
            print(domain)
            values = sites[domain]
            if len(values) != 0:
                if not os.path.exists(self._prefix + domain):
                    os.mkdir(self._prefix + domain)
                i = 1
                index_csv = open(self._prefix + domain + "/index_csv.txt", "w")
                for site in tqdm(values):
                    print(site)
                    try:
                        req = Request(site, headers={'User-Agent': "Magic Browser"})
                        html = urlopen(req)
                        bsObj = BeautifulSoup(html, "lxml")
                        for script in bsObj(["script", "style"]):
                            script.decompose()
                        csvFile = open(self._prefix + domain + "/" + str(i) + ".csv", 'wt', newline='')
                        writer = csv.writer(csvFile)
                        csvRows = list()
                        product_name = bsObj.find("h1")
                        if product_name:
                            writer.writerow(["name:", product_name.get_text()])
                        tables = bsObj.findAll("table")
                        index_csv.write(site + "\t" + str(i) + ".csv\n")
                        if tables:
                            for table in tables:
                                rows = table.findAll("tr")
                                for row in rows:
                                    csvRow = list()
                                    for cell in row.findAll(['th', 'td']):
                                        text = ' '.join(
                                            cell.get_text().replace('\n', ' ').replace('\t', ' ').strip().split())
                                        if text:
                                            if ':' in text:
                                                strings = text.split(':', 1)
                                                elements = self.group(strings, 2)
                                                for el in elements:
                                                    if el not in csvRows:
                                                        csvRows.append(el)
                                            else:
                                                if len(text.split()) <= self._MAXIMUM_TEXT_LENGTH:
                                                    csvRow.append(text)
                                        full_text = cell.get_text().replace('•', '\n').splitlines()
                                        for string in full_text:
                                            if 0 < len(string.split()) <= self._MAXIMUM_TEXT_LENGTH and ':' in string:
                                                strings = string.replace('\n', ' ').replace('\t', ' ').strip().split(':', 1)
                                                elements = self.group(strings, 2)
                                                for el in elements:
                                                    if el not in csvRows:
                                                        csvRows.append(el)
                                    if len(csvRow) > 0:
                                        if csvRow not in csvRows:
                                            csvRows.append(csvRow)
                        lists = bsObj.findAll("ul")
                        if lists:
                            for lis in lists:
                                li = lis.findAll("li")
                                for row in li:
                                    csvRow = list()
                                    if row.get_text().strip():
                                        text = ' '.join(
                                            row.get_text().replace('\n', ' ').replace('\t', ' ').strip().split())
                                        if ':' in text:
                                            strings = text.split(':', 1)
                                            elements = self.group(strings, 2)
                                            for el in elements:
                                                if el not in csvRows:
                                                    csvRows.append(el)
                                        else:
                                            if len(text.split()) <= self._MAXIMUM_TEXT_LENGTH:
                                                csvRow.append(text)
                                    if len(csvRow) > 0:
                                        if csvRow not in csvRows:
                                            csvRows.append(csvRow)
                        for r in csvRows:
                            writer.writerow(r)
                        i += 1
                        csvFile.close()
                    except Exception as e:
                        print(e)
                        continue
                index_csv.close()

    def group(self, lst, n):
        return zip(*[lst[i::n] for i in range(n)])


if __name__ == "__main__":
    extractor = CsvExtractor()
    extractor.extract()
