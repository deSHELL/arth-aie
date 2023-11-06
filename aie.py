#!/bin/env python
import os
import re
import json
import shutil
import requests

AIE_REPO_URL = "https://aie.deva.is-cool.dev"
PACKAGE_INDEX = "package_index.json"
PACKAGE_INDEX_TMP = "/tmp/aie/package_index.json"
PACKAGES_TMP = "/tmp/aie/packages"

def download_package_index():
    package_index_url = f"{AIE_REPO_URL}/{PACKAGE_INDEX}"
    response = requests.get(package_index_url)

    if response.status_code != 200:
        print(f"Failed to retrieve package index from {package_index_url}")
        return None

    if not os.path.exists("/tmp/aie"):
        os.mkdir("/tmp/aie")

    with open(PACKAGE_INDEX_TMP, "wb") as file:
        file.write(response.content)

def download_packages():
    package_index = json.load(open(PACKAGE_INDEX_TMP))

    if not os.path.exists(PACKAGES_TMP):
        os.mkdir(PACKAGES_TMP)

    for package_name, equations in package_index["packages"].items():
        package_dir = os.path.join(PACKAGES_TMP, package_name)

        if not os.path.exists(package_dir):
            os.mkdir(package_dir)

        for equation in equations["equations"]:
            equation_url = f"{AIE_REPO_URL}/{package_name}/{equation}"
            response = requests.get(equation_url)

            if response.status_code == 200:
                equation_path = os.path.join(package_dir, equation)
                with open(equation_path, "wb") as file:
                    file.write(response.content)
            else:
                print(f"Failed to download equation '{equation}' in package '{package_name}'")

def main():
    if not os.path.exists(PACKAGE_INDEX_TMP):
        download_package_index()
    download_packages()

if __name__ == "__main__":
    main()
