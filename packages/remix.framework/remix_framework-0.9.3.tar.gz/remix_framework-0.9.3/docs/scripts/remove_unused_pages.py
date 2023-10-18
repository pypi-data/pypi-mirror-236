import os
import glob
import json
import shutil

PUBLIC_DIRECTORY = "public"
VERSIONS_JSON = "public/_static/versions.json"

with open(VERSIONS_JSON, "r") as vj:
    versions = json.load(vj)
keep = [os.path.join(*(v["name"].split("/"))) for v in versions] + ["_static"]

first_level = list(glob.glob(f"{PUBLIC_DIRECTORY}/*"))
pages_level = list(glob.glob(f"{PUBLIC_DIRECTORY}/pages/*"))
all_folders = [os.path.join(*(f.split(os.path.sep)[1:])) for f in first_level + pages_level if os.path.isdir(f)]

for f in all_folders:
    if all([f not in k for k in keep]):
        print(f"Removing {f}")
        shutil.rmtree(os.path.join(PUBLIC_DIRECTORY, f), ignore_errors=True)
    else:
        print(f"{f} was not removed")
