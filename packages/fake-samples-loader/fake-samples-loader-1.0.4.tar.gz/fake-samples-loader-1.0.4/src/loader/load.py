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
    data_to_send_to_source = {
        QUERY_FIELD: arg1,
        PAGE_FIELD: str(arg2)
    }

    postUrl = arg3 + POST_URL_SEARCH_PHP_PARAMETER

    source_response_is_invalid = True
    while source_response_is_invalid:
        response = requests.post(url = postUrl, data = data_to_send_to_source)
        if response.status_code != 200:
            raise Exception("Error while scrapping: " + response.reason)
        response_text = response.text
        source_response_is_invalid = _is_response_text_valid(response_text)
    
    source_samples_data_dict = _get_source_samples_data_dict_from_source_response_text(response.text)        
    samples_objects_list = _get_sample_objects_from_source_samples_data_dict(source_samples_data_dict)
    return json.dumps(get_json_from_sample_objects_list(samples_objects_list))

def get_json_from_sample_objects_list(sample_objects_list):
    samples_json = "["
    is_first_sample = True
    for sample_object in sample_objects_list:
        if not is_first_sample:
            samples_json += ","
        samples_json += sample_object.toJSON()
        is_first_sample = False
    return samples_json + "]"


def _get_sample_objects_from_source_samples_data_dict(source_samples_data_dict):
    samples = []
    for sample_json in source_samples_data_dict:
        if sample_json != START_STRING:
            samples.append(Sample(
                title=sample_json[TITLE_FIELD], 
                artistName=sample_json[ARTIST_NAME_FIELD], 
                duration=sample_json[DURATION_FIELD], 
                releasedOn=sample_json[RELEASED_ON_FIELD],
                url=sample_json[URL_FIELD]))
    return samples

def _get_text_after_start_string(text):
    return text.split(START_STRING)[1]

def _remove_5_last_characters(text):
    return text[:len(text) - 5]


def _get_source_samples_data_dict_from_source_response_text(source_response_text):
    reponse_text_with_right_start = _get_text_after_start_string(source_response_text)
    reponse_text = "[" + _remove_5_last_characters(reponse_text_with_right_start)
    return json.loads(reponse_text)


def _get_first_string_between_two_strings(string, string1, string2):
    return string.split(string1,1)[1].split(string2,1)[0]


def _is_response_text_valid(response_text):
    print("REEEESPOOOONSE")
    print(_get_first_string_between_two_strings(response_text, "response\":", "});"))
    return _get_first_string_between_two_strings(response_text, "response\":", "});") == "null"