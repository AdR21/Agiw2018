import json


class KnowledgeBaseExtractor:

    _specs_file = "tvs_labelled_entities.json"
    _table_attributes = "table_atts"
    _list_attributes = "list_atts"
    _attributes_mapping = "atts_map"
    _output_file = "knowledge_base_tv.json"

    def __init__(self):
        full_list = self.json2list()
        full_dictionary = self.regroup_items(full_list)
        with open(self._output_file, "w") as output:
            json.dump(full_dictionary, output, indent=4)

    def json2list(self):
        with open(self._specs_file) as json_file:
            full_dictionary = json.load(json_file)
        res = []
        for elem in full_dictionary:
            new_elem = {
                self._table_attributes: {},
                self._list_attributes: {},
                self._attributes_mapping: {}
            }
            for mapping in elem[self._attributes_mapping]:
                strings = mapping.split(":", 1)
                key = strings[0].strip()
                value = strings[1].strip()
                new_elem[self._attributes_mapping][key] = value
            mapping_copy = new_elem[self._attributes_mapping].copy()
            for item in elem[self._table_attributes]:
                strings = item.split(":", 1)
                if len(strings) == 2:
                    key = strings[0].strip()
                    value = strings[1].strip()
                    mapped_key = self.key_mapping(key, mapping_copy)
                    new_elem[self._table_attributes][mapped_key] = value
            for item in elem[self._list_attributes]:
                strings = item.split(":", 1)
                key = strings[0].strip()
                value = strings[1].strip()
                mapped_key = self.key_mapping(key, mapping_copy)
                new_elem[self._list_attributes][mapped_key] = value
            res.append(new_elem)
        return res

    def regroup_items(self, object_list):
        res = {
            self._table_attributes: {},
            self._list_attributes: {},
            self._attributes_mapping: {}
        }
        for elem in object_list:
            for table_attribute in elem[self._table_attributes]:
                if table_attribute not in res[self._table_attributes]:
                    res[self._table_attributes][table_attribute] = list()
                if elem[self._table_attributes][table_attribute] not in res[self._table_attributes][table_attribute]:
                    res[self._table_attributes][table_attribute].append(elem[self._table_attributes][table_attribute])
            for list_attribute in elem[self._list_attributes]:
                if list_attribute not in res[self._list_attributes]:
                    res[self._list_attributes][list_attribute] = list()
                if elem[self._list_attributes][list_attribute] not in res[self._list_attributes][list_attribute]:
                    res[self._list_attributes][list_attribute].append(elem[self._list_attributes][list_attribute])
            for mapping in elem[self._attributes_mapping]:
                if mapping not in res[self._attributes_mapping]:
                    res[self._attributes_mapping][mapping] = list()
                if elem[self._attributes_mapping][mapping] not in res[self._attributes_mapping][mapping]:
                    res[self._attributes_mapping][mapping].append(elem[self._attributes_mapping][mapping])
        return res

    @staticmethod
    def key_mapping(elem, mapping):
        mapped_key = elem
        if elem in mapping:
            mapped_key = mapping[elem]
        return mapped_key


if __name__ == "__main__":
    KnowledgeBaseExtractor()
