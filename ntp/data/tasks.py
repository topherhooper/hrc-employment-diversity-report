from celery import Celery
import api

APP = Celery("ntp.data.tasks")
APP.config_from_object("ntp.data.celeryconfig")


@APP.task
def check_and_fetch():
    """
    Check for an update to the HR data on the open data portal.  If one exists do.
    """
    api.check_load_data()


@APP.task
def test_task(a):
    """
    Stupid task for testing purposes
    """
    return a + 1


if __name__ == '__main__':
    check_and_fetch()
