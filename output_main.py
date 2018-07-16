from csv_cleaner import CsvCleaner
import os
import json
from tqdm import tqdm


_output_headphone_dir = "headphone_specs"
_headphone_csv_dir = "headphone_csv"
_output_tv_dir = "tv_specs"
_tv_csv_dir = "tv_csv"
_domains = ["headphone", "tv"]

csv_cleaner = CsvCleaner("headphone")

for domain in tqdm(os.listdir(_headphone_csv_dir)):
    print(domain)
    curr_dir = _output_headphone_dir + "/" + domain
    csv_dir = _headphone_csv_dir + "/" + domain
    if not os.path.exists(curr_dir):
        os.mkdir(curr_dir)
    index = open(curr_dir + "/index.txt", "w")
    index_csv = open(csv_dir + "/index_csv.txt")
    i = 1
    for line in tqdm(index_csv.readlines()):
        strings = line.split("\t")
        site = strings[0].strip()
        csv_file = strings[1].strip()
        output = csv_cleaner.get_csv_information_as_dict(csv_dir + "/" + csv_file)
        with open(curr_dir + "/" + str(i) + ".json", "w") as json_output:
            json.dump(output, json_output, indent=4)
        index.write(site + "\t" + str(i) + ".json\n")
        i += 1
    index.close()
    index_csv.close()

csv_cleaner = CsvCleaner("tv")

for domain in tqdm(os.listdir(_tv_csv_dir)):
    print(domain)
    curr_dir = _output_tv_dir + "/" + domain
    csv_dir = _tv_csv_dir + "/" + domain
    if not os.path.exists(curr_dir):
        os.mkdir(curr_dir)
    index = open(curr_dir + "/index.txt", "w")
    index_csv = open(csv_dir + "/index_csv.txt")
    i = 1
    for line in tqdm(index_csv.readlines()):
        strings = line.split("\t")
        site = strings[0].strip()
        csv_file = strings[1].strip()
        output = csv_cleaner.get_csv_information_as_dict(csv_dir + "/" + csv_file)
        with open(curr_dir + "/" + str(i) + ".json", "w") as json_output:
            json.dump(output, json_output, indent=4)
        index.write(site + "\t" + str(i) + ".json\n")
        i += 1
    index.close()
    index_csv.close()