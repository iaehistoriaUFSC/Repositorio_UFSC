import os
import time
import re
from typing import Dict
import requests
from bs4 import BeautifulSoup        
# !pip install xmltodict
import xmltodict
# !pip install unidecode
from unidecode import unidecode
import joblib

os_name = os.name

def limparConsole():
    if os_name == 'posix':
        os.system('clear')
    elif os_name == 'nt':
        os.system('cls')
    