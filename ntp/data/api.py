"""
Primary python API for interacting with the data from the open data portal.  There's a lot of cases in here that need
to be tested.
"""
import requests


def write_csv(path, json_like, fieldnames=None, delimiter=","):
    """
    :param path: full path of file to write out
    :param json_like: json_like to write to csv
    :param fieldnames: the fields to use as the csv header
    :param delimiter: defaults to ","
    :return: None, writes file to path
    """
    import csv
    if not fieldnames:
        fieldnames = [key for key in json_like[0]]
    with open(path, 'w') as path:
        dw = csv.DictWriter(path, delimiter=delimiter, fieldnames=fieldnames)
        dw.writeheader()
        for doc in json_like:
            try:
                dw.writerow({key: unicode(doc[key]).encode("utf8") for key in doc})
            except UnicodeEncodeError:
                print doc


def should_update(ntp_last_updated, odp_last_updated):
    """
    Check rethinkdb for a record of imported datasets.
    """
    if int(odp_last_updated) > int(ntp_last_updated):
        return True
    return False


def check_for_update():
    """
    Shameless hard coded.  Check the open data portal for the demographic data's explicit api and get
    the last updated value.
    """

    endpoint = "https://data.nashville.gov/api/views/4ibi-mxs4"
    response = requests.get(endpoint)
    demographics_object = response.json()
    epoch_timestamp = demographics_object.get("rowsUpdatedAt")
    return epoch_timestamp


def retrieve_data():
    """
    Grab the actual demographics data from the Open Data Portal
    """

    api_endpoint = "https://data.nashville.gov/resource/4ibi-mxs4.json?$limit=50000"
    data = requests.get(api_endpoint).json()
    return data


def ntp_last_update():
    """
    Get the last updated value of Inclucivics Data
    """
    import os
    def strip_date(date_string):
        from datetime import datetime
        return datetime.strptime(date_string, '%Y%m%d')

    file_path = 'ntp/files/input/201441207.csv'
    input_path = os.path.os.path.dirname(os.path.realpath((file_path)))
    onlyfiles = [
        strip_date(os.path.splitext(f)[0])
        for f in os.listdir(input_path)
        if os.path.isfile(os.path.join(input_path, f))]
    return max(onlyfiles).strftime('%s')
