import requests
import json
import os
import tarfile
import sys

def parseLibraries(jsonData: str) -> list:
    jsonObject = json.loads(jsonData)
    return jsonObject["ADDONS"]["libraries"]


def generateDownloadLink(fileName: str) -> str:
    return "https://github.com/elydre/libatron/releases/download/latest/" + fileName


def getFiles(lib: str, jsonData: dict) -> list:
    for library in jsonData["ADDONS"]["libraries"]:
        if library["name"] == lib:
            return library["files"]
    return []


def attemptDownload(file: str, folder: str):
    os.makedirs(folder, exist_ok=True)

    fileName = file
    if fileName.endswith("headers"):
        fileName += ".tar.gz"

    if file.endswith(".so"):
        fileName = file[:-3] + ".a"

        print("Attempting download:", fileName)

        request = requests.get(generateDownloadLink(fileName))

        if request.status_code != 200:
            fileName = file
            print("Fallback to:", fileName)
            request = requests.get(generateDownloadLink(fileName))
            fileName = fileName
    else:
        request = requests.get(generateDownloadLink(fileName))
    if request.status_code == 200:
        savePath = os.path.join(folder, fileName)

        with open(savePath, "wb") as f:
            f.write(request.content)

        print("Downloaded:", savePath)

        if "headers" in fileName and fileName.endswith(".tar.gz"):
            headersFolder = os.path.join(folder, "headers")
            os.makedirs(headersFolder, exist_ok=True)

            print("Extracting headers to:", headersFolder)

            with tarfile.open(savePath, "r:gz") as tar:
                tar.extractall(path=headersFolder)

    else:
        print("Failed to download:", fileName)


def downloadFiles(libs: list, jsonData: dict) -> None:
    for lib in libs:
        folder = "3rdParty/" + lib

        os.makedirs(folder, exist_ok=True)

        files = getFiles(lib, jsonData)

        for file in files:
            attemptDownload(file, folder)


def getDependencies(filePath: str, jsonData: dict) -> list:
    dependencies = []

    with open(filePath) as f:
        for line in f:
            dep = line.strip()
            if dep:
                dependencies.append(dep)

    libraries = jsonData["ADDONS"]["libraries"]

    result = list(dependencies)

    for dep in dependencies:
        for lib in libraries:
            if lib["name"] == dep and "dependencies" in lib:
                for sub in lib["dependencies"]:
                    if sub not in result:
                        result.append(sub)

    return result


def main():
    jsonVal = requests.get(
        'https://raw.githubusercontent.com/elydre/elydre.github.io/refs/heads/main/profan/addons.json'
    )

    jsonObject = json.loads(jsonVal.text)

    if len(sys.argv) >= 2:
        if sys.argv[1] == "list":
            print([lib["name"] for lib in jsonObject["ADDONS"]["libraries"]])
        elif sys.argv[1] == "help":
            print("dependencies.py [<list>]")
            print("dependencies.txt : Add each dependency per new line")
    else:
        libs = getDependencies("dependencies.txt", jsonObject)
        downloadFiles(libs, jsonObject)


if __name__ == "__main__":
    main()