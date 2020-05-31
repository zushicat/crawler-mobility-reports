import csv
import json
import os
from typing import Any, Optional

import requests

from _by_date import get_date


DIRNAME = os.path.dirname(__file__)


def _get_csv_link() -> Optional[str]:
    '''
    Request returns:
    {
        "basePath":"/covid19-mobility-data/2009HotfixDev12/v3",
        "mobilityDataVersion":"2009HotfixDev12:2020-05-28",
        "regions": {
            "en-us":{
                "jsonPath":"/en-us/applemobilitytrends.json",
                "localeNamesPath":"/en-us/locale-names.json",
                "csvPath":"/en-us/applemobilitytrends-2020-05-28.csv",
                "initialPath":"/en-us/initial-data.json",
                "shards":{
                    "defaults":"/en-us/shards/defaults.json"
                }
            }
        }
    }
    Returns:
    "https://covid19-static.cdn-apple.com/covid19-mobility-data/2009HotfixDev12/v3/en-us/applemobilitytrends-2020-05-28.csv"
    '''
    json_url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json"
    r = requests.get(json_url)

    csv_url = None

    try:
        mobility_data_paths = json.loads(r.text)
        base_url = "https://covid19-static.cdn-apple.com"
        csv_url = f'{base_url}{mobility_data_paths["basePath"]}{mobility_data_paths["regions"]["en-us"]["csvPath"]}'
    except Exception as e:
        print(f"Error with json processing: {e}")

    return csv_url


def _request_csv_url(csv_url: str) -> None:
    file_name = f'apple_{csv_url.split("/")[-1]}'
    r = requests.get(csv_url)

    decoded_content = r.content.decode('utf-8')

    csv_data = csv.reader(decoded_content.splitlines(), delimiter=',')
    _write_csv(csv_data, file_name)


def _write_csv(csv_data: Any, file_name: str) -> None:
    today = get_date()
    
    with open(f"{DIRNAME}/data/{today}/{file_name}", "w") as f:
       writer = csv.writer(f, delimiter=",")
       writer.writerows(csv_data)


def request_apple():
   csv_url = _get_csv_link()
   if csv_url is not None:
       _request_csv_url(csv_url)
