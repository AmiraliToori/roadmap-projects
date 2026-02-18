#!/usr/bin/env python3
import html2text
import requests
import sys

from requests.exceptions import MissingSchema

url = input("Enter the Article URL:\n>")

if url.isspace():
    print("Invalid URL.")
    sys.exit(1)

try:
    html = requests.get(url.strip()).text
except MissingSchema:
    print("Invalid URL.")
    sys.exit(1)

converter = html2text.HTML2Text()
text = converter.handle(html)
print(text)
