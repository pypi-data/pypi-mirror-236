import json



def convertDictJson(dictObj):
    """Converts the given dictionary object into a json object

    Args:
        dictObj (dict): dictionary object
    """
    # convert to string
    stringDict = json.dumps(dictObj)
    # convert to json object
    return json.loads(stringDict)


def writeDictToJsonFile(dictObj, filename):
    jsonObj = convertDictJson(dictObj)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jsonObj, f)


