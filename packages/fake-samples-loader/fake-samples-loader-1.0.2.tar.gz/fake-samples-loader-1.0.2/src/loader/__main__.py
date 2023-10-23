import sys
import requests
import json
from loader.Sample import Sample

POST_URL_SEARCH_PHP_PARAMETER = 'api_search.php?callback=jQuery2130003814019662980783_1697629885270'

DATA_FIELD = "response"
TITLE_FIELD = "title"
ARTIST_NAME_FIELD = "artist"
URL_FIELD = "url"
RELEASED_ON_FIELD = "date"
DURATION_FIELD = "duration"

QUERY_FIELD = "q"
PAGE_FIELD = "page"
PAGE_SIZE_FIELD = "page_size"

START_STRING = "apple\","


def main():
    arg1 = sys.argv[1]
    arg2 = int(sys.argv[2])
    arg3 = sys.argv[3]
    arg4 = 29

    dataToSendToSource = {
        QUERY_FIELD: arg1,
        PAGE_FIELD: str(arg2)
    }

    postUrl = arg3 + POST_URL_SEARCH_PHP_PARAMETER

    sourceResponseIsInvalid = True
    while sourceResponseIsInvalid:
        response = requests.post(url = postUrl, data = dataToSendToSource)
        if response.status_code != 200:
            raise Exception("Error while scrapping: " + response.reason)
        responseText = response.text
        sourceResponseIsInvalid = _isResponseTextValid(responseText)
    
    sourceSamplesDataDict = _getSourceSamplesDataDictFromSourceResponseText(response.text)        
    return _getSampleObjectsFromSourceSamplesDataDict(sourceSamplesDataDict)


def _getSampleObjectsFromSourceSamplesDataDict(sourceSamplesDataDict):
    samples = []
    for sampleJson in sourceSamplesDataDict:
        if sampleJson != START_STRING:
            samples.append(Sample(
                title=sampleJson[TITLE_FIELD], 
                artistName=sampleJson[ARTIST_NAME_FIELD], 
                duration=sampleJson[DURATION_FIELD], 
                releasedOn=sampleJson[RELEASED_ON_FIELD],
                url=sampleJson[URL_FIELD]))
    return samples

def _getTextAfterStartString(text):
    return text.split(START_STRING)[1]

def _remove5LastCharacters(text):
    return text[:len(text) - 5]


def _getSourceSamplesDataDictFromSourceResponseText(sourceResponseText):
    reponseTextWithRightStart = _getTextAfterStartString(sourceResponseText)
    reponseText = "[" + _remove5LastCharacters(reponseTextWithRightStart)
    return json.loads(reponseText)


def _getFirstStringBetweenTwoStrings(string, string1, string2):
    return string.split(string1,1)[1].split(string2,1)[0]


def _isResponseTextValid(responseText):
    print("REEEESPOOOONSE")
    print(_getFirstStringBetweenTwoStrings(responseText, "response\":", "});"))
    return _getFirstStringBetweenTwoStrings(responseText, "response\":", "});") == "null"


if __name__ == "__main__":
    main()