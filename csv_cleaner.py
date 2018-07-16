import csv
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import math
from sklearn.feature_extraction.text import TfidfVectorizer


class CsvCleaner:

    _MIN_SIMILARITY = 0.7
    _ROUND = 2
    _MAXIMUM_KEY_LENGTH = 10
    _MAXIMUM_VALUE_LENGTH = 20
    _MAXIMUM_UNKOWN_VALUE_LENGTH = 5
    _key_unknown = "Unknown key"
    _headphone_know = "knowledge_base_headphone.json"
    _tv_know = "knowledge_base_tv.json"

    def __init__(self, domain):
        self.cpu_num = multiprocessing.cpu_count()
        if domain == "headphone":
            with open(self._headphone_know) as know:
                self.base = json.load(know)
        elif domain == "tv":
            with open(self._tv_know) as know:
                self.base = json.load(know)

    def get_csv_information_as_dict(self, csv_path):
        result = dict()
        data = list()
        with open(csv_path) as csv_specs:
            reader = csv.reader(csv_specs, delimiter=",")
            for line in reader:
                data.append(line)
        datas = self.chunks(data, math.ceil(len(data)/self.cpu_num))
        executor = ThreadPoolExecutor(max_workers=self.cpu_num)
        wait_for = [executor.submit(self.parallel_search, d.copy(), self.base.copy()) for d in datas]
        for future in as_completed(wait_for):
            result.update(future.result())
        executor.shutdown()
        return result

    def parallel_search(self, data, base):
        result = dict()
        to_be_evaluated = dict()
        for i, line in enumerate(data):
            if line:
                if line[0] == "name:":
                    self.put_if_not_exists(result, "Name", line[1])
                elif len(line) >= 2:
                    key = line[0]
                    value = line[1]
                    if len(key.split()) <= self._MAXIMUM_KEY_LENGTH:
                        known = self.get_matching_key(key, base)
                        if known:
                            self.put_if_not_exists(result, key, value)
                        else:
                            to_be_evaluated[i] = [key, value]
                    elif len(value.split()) <= self._MAXIMUM_VALUE_LENGTH:
                        known = self.get_matching_value(value, base)
                        if known:
                            self.put_if_not_exists(result, key, value)
                        else:
                            to_be_evaluated[i] = [key, value]
                """else:
                    value = line[0]
                    if value:
                        if len(value.split()) <= self._MAXIMUM_UNKOWN_VALUE_LENGTH:
                            known = self.get_matching_value(value, base)
                            if known:
                                key = self.get_matching_key(value, base)
                                translated_key = self.get_key(key, base)
                                self.put_if_not_exists(result, translated_key, value)"""
        for index in to_be_evaluated:
            key = to_be_evaluated[index][0]
            value = to_be_evaluated[index][1]
            if (len(key.split()) <= self._MAXIMUM_KEY_LENGTH and
                    len(value.split()) <= self._MAXIMUM_VALUE_LENGTH and
                    self.search(data, result, index, self._ROUND)):
                self.put_if_not_exists(result, key, value)
        return result

    def get_matching_key(self, key, base):
        for known in base["atts_map"]:
            if self.cosine_sim(key.lower(), known.lower()) >= self._MIN_SIMILARITY:
                return known
        return ''

    def get_matching_value(self, value, base):
        values = [item for sublist in base["table_atts"].values() for item in sublist]
        values.extend([item for sublist in base["list_atts"].values() for item in sublist])
        for known in values:
            if self.cosine_sim(value.lower(), known.lower()) >= self._MIN_SIMILARITY:
                return known
        return ''

    def get_key(self, key, base):
        for key_t in base["atts_map"]:
            if key in base["atts_map"][key_t]:
                return key_t
        return ''

    def put_if_not_exists(self, dic, key, value):
        if key not in dic:
            dic[key] = value

    def cosine_sim(self, text1, text2):
        vectorizer = TfidfVectorizer()
        try:
            tfidf = vectorizer.fit_transform([text1, text2])
            return (tfidf * tfidf.T).A[0, 1]
        except ValueError as e:
            return 0.0

    def search(self, data, extracted, index, around):
        for i in range(-around + index, around + index):
            try:
                if data[i][0] in extracted or data[i][1] in extracted.values():
                    return True
            except IndexError:
                continue
        return False

    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


if __name__ == "__main__":
    res = CsvCleaner("headphone").get_csv_information_as_dict("headphone_csv/au.shopping.com/1.csv")
    with open("test.json", "w") as output:
        json.dump(res, output, indent=4)
