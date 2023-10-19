import logging
import pandas as pd
import urllib3
import ssl
import io
import numpy as np
import skimage as ski
import matplotlib.pyplot as plt
import os.path

logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

logger.info("Start marcuslion lib")
resource_path = os.path.join(os.path.split(__file__)[0], "resources")
image = ski.io.imread(resource_path + "/marcus_lion_logo.jpg")
ski.io.imshow(image)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 2000)

# this required downgrading requests library to urllib3-1.24.3 to avoid SSL cert error
ssl._create_default_https_context = ssl._create_unverified_context

# Creating a PoolManager instance for sending requests.
http = urllib3.PoolManager()

baseUrl = "https://qa1.marcuslion.com"


def ml_help():
    print("  .ml_providers() or .ml_search()")


def ml_search(key, providers):
    # $ curl 'https://qa1.marcuslion.com/core/datasets/search?providers=kaggle,usgov&title=bike'
    url = 'core/datasets/search'
    baseParams = "providers=" + providers + "&title=" + key
    fullUrl = baseUrl + "/" + url + "?" + baseParams

    # Sending a GET request and getting back response as HTTPResponse object.
    # this required downgrading requests library to urllib3-1.24.3 to avoid SSL cert error
    resp = http.request("GET", fullUrl)

    # converting
    allData = resp.data.decode()
    return pd.read_json(io.StringIO(allData))


def ml_providers():
    # $ curl 'https://qa1.marcuslion.com/core/datasets/search?providers=kaggle,usgov&title=bike'
    url = 'core/datasets/providers'
    fullUrl = baseUrl + "/" + url

    # Sending a GET request and getting back response as HTTPResponse object.
    resp = http.request("GET", fullUrl)

    # converting
    allData = resp.data.decode()
    return pd.read_json(io.StringIO(allData))
