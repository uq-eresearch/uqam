from celery.task import task
import requests


@task()
def send_collection(collection, url, auth):
        requests.post(url, data=collection)
