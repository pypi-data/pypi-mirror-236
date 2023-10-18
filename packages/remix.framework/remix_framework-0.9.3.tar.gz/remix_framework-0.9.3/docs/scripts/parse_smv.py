import os
import json
import urllib.parse

with open("docs/scripts/smv_versions.json") as f:
    svm_versions = json.load(f)

# Define the base_url for our version switcher.
##### for the open repo (starting 06.09.2023) #####
base_url = 'https://dlr-ve.gitlab.io/esy/remix/framework/'
# base_url = 'https://remix.pages.gitlab.dlr.de/framework/'

versions = [{'name': v, 'version': v, 'url': f"{base_url}{urllib.parse.quote(v)}/"} for v in svm_versions]

os.makedirs("public/_static", exist_ok=True)
with open("public/_static/versions.json", 'w') as f:
    json.dump(versions, f, indent=2)
