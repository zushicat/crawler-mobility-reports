import csv
import os
from typing import Any

from _by_date import get_date

import requests


DIRNAME = os.path.dirname(__file__)


def _request_url() -> None:
    file_url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
    r = requests.get(file_url)

    decoded_content = r.content.decode('utf-8')

    csv_data = csv.reader(decoded_content.splitlines(), delimiter=',')
    _write_csv(csv_data, "Global_Mobility_Report.csv")


def _write_csv(csv_data: Any, file_name: str) -> None:
    today = get_date()
    
    with open(f"{DIRNAME}/data/{today}/google_{file_name}", "w") as f:
       writer = csv.writer(f, delimiter=",")
       writer.writerows(csv_data)


def request_google():
    _request_url()
