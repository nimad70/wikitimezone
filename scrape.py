# Author: nima daryabar
# Get a url and return response
import requests

def webscraping(url):
    res = requests.get(url)
    print("response from url: ", res)
    return res