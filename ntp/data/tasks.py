import time
from celery import Celery
import api
import json

APP = Celery("ntp.data.tasks")
APP.config_from_object("ntp.data.celeryconfig")


@APP.task
def check_and_fetch():
    """
    Check for an update to the HR data on the open data portal.  If one exists do.
    """
    # url = 'https://data.nashville.gov/resource/9f73-up2p.json'
    odp_last_updated = api.check_for_update()
    ntp_last_updated = api.ntp_last_update()
    if api.should_update(ntp_last_updated=ntp_last_updated, odp_last_updated=odp_last_updated):
        print 'new'
        data = api.retrieve_data()
        file_name = time.strftime('%Y%m%d', time.localtime(odp_last_updated))
        full_file_path = 'ntp/files/input/{0}.csv'.format(file_name)
        api.write_csv(
            path=full_file_path,
            json_like=data)
    else:
        pass

@APP.task
def test_task(a):
    """
    Stupid task for testing purposes
    """
    return a + 1


if __name__ == '__main__':
    check_and_fetch()
