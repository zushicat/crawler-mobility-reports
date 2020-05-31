import csv
import json
import os
from typing import Any, Tuple

from _by_date import get_date

import requests
from bs4 import BeautifulSoup


DIRNAME = os.path.dirname(__file__)


def _request_csv_url(csv_url: str) -> None:
    file_name = f'teralytics_{csv_url.split("/")[-1]}'
    r = requests.get(csv_url)

    decoded_content = r.content.decode('utf-8')

    csv_data = csv.reader(decoded_content.splitlines(), delimiter=',')
    _write_csv(csv_data, file_name)


def _write_csv(csv_data: Any, file_name: str) -> None:
    today = get_date()
    
    with open(f"{DIRNAME}/data/{today}/{file_name}", "w") as f:
       writer = csv.writer(f, delimiter=",")
       writer.writerows(csv_data)


def _get_csv_file_name(script_url:str) -> Tuple[str, str]:
    '''
    Get "de":{"fileSuffix": "2020-05-29", ... from script and compose csv filename "counts.2020-05-29.csv"
    '''
    r = requests.get(script_url)
    js_fragment = r.text[:800]  # use first short part of reuqested JS data, only
    
    # ***
    # cut JS fragment to relevant string: "de":{"fileSuffix":"2020-05-29","focusStartDate":"2020-03-11"
    # get dates from extracted data
    start = js_fragment.find('"de":{"fileSuffix":"')
    end = start + js_fragment[start:].find(',"referenceWeekdayPattern":"')
    date_data = json.loads(f"{{ {js_fragment[start:end]} }}}}")  # {'de': {'fileSuffix': '2020-05-29', 'focusStartDate': '2020-03-11'}}

    csv_file_suffix = date_data["de"]["fileSuffix"]
    csv_start_date = date_data["de"]["focusStartDate"]

    csv_file_name = f"counts.{csv_file_suffix}.csv"

    return csv_file_name, csv_start_date


def _request_url() -> None:
    base_url = "https://rki.mobility-covid19.teralytics.net/"
    r = requests.get(base_url)
    
    soup = BeautifulSoup(r.text, 'html.parser')

    # ***
    # get script with info about file (to compose csv file name)
    source_script = None
    for script_node in soup.findAll("script", {"src":True}):
        if script_node["src"].find("/static/js/main.") != -1:
            source_script = script_node["src"]
            break

    # ***
    # get ccomposed csv filename and csv start date (earliest date in timeseries)
    script_url = f"{base_url}{source_script}"  
    csv_file_name, csv_start_date = _get_csv_file_name(script_url)

    # ***
    # https://rki.mobility-covid19.teralytics.net/data/de/counts.2020-05-29.csv
    csv_url = f"{base_url}data/de/{csv_file_name}"
    _request_csv_url(csv_url)


def request_rki():
    _request_url()