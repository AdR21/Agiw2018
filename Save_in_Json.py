def writeToJSONFile(path, fileName, result):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fout:
        json.dump(result, fout, indent=4)

path = './'
fileName = 'au_shopping_com'

writeToJSONFile(path, fileName, result)