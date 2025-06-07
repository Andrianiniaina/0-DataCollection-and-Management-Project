import requests
import time
import os
import pandas as pd

url_api = "https://nominatim.openstreetmap.org/reverse"
headers = {
    "User-Agent" : "MyPythonScript/1.0",
    "Referer" : "https://mywebsite.com/page.html"
}