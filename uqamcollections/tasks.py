from celery.task import task
import requests


@task()
def add(x, y):
    return x + y

def send_collection(collection, url, auth):
        requests.post(url, data=collection)
