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


def get_samples(arg1, arg2, arg3, arg4=29):
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
        sourceResponseIsInvalid = _is_response_text_valid(responseText)
    
    sourceSamplesDataDict = _get_source_samples_data_dict_from_source_response_text(response.text)        
    return _get_sample_objects_from_source_samples_data_dict(sourceSamplesDataDict)


def _get_sample_objects_from_source_samples_data_dict(sourceSamplesDataDict):
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

def _get_text_after_start_string(text):
    return text.split(START_STRING)[1]

def _remove_5_last_characters(text):
    return text[:len(text) - 5]


def _get_source_samples_data_dict_from_source_response_text(sourceResponseText):
    reponseTextWithRightStart = _get_text_after_start_string(sourceResponseText)
    reponseText = "[" + _remove_5_last_characters(reponseTextWithRightStart)
    return json.loads(reponseText)


def _get_first_string_between_two_strings(string, string1, string2):
    return string.split(string1,1)[1].split(string2,1)[0]


def _is_response_text_valid(responseText):
    print("REEEESPOOOONSE")
    print(_get_first_string_between_two_strings(responseText, "response\":", "});"))
    return _get_first_string_between_two_strings(responseText, "response\":", "});") == "null"