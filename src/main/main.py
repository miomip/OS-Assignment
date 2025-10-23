# Importing functions only for operationalization reasons
from os import getlogin, name, mkdir
from os.path import isdir
from platform import release, machine, version
from shutil import disk_usage
from socket import gethostbyname, gethostname
from subprocess import check_output, CalledProcessError, check_call
from json import dump
from sys import executable


def installPackage(package_name):
    try:
        check_call([executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}")
    except CalledProcessError as error:
        print(f"Error installing {package_name}: {error}")

installPackage("elevate")

from elevate import elevate


def main():
    elevate()
    osInfo = getOSInfo()
    storageSpace = getStorageAmount("C:")
    ipAddress =  getIPAddress()
    programs = getPrograms(osInfo["name"])

    data = {
        "name": osInfo["name"],
        "release": osInfo["release"],
        "version": osInfo["version"],
        "architecture": osInfo["architecture"],
        "user": osInfo["user"],
        "storageSpace": storageSpace,
        "ipAddress": ipAddress,
        "programs": programs
    }
    if not isdir("C:\\maskin"):
        mkdir("C:\\maskin")
    with open("C:\\maskin\\data.json", "w") as file:
        dump(data, file, indent=4)
    print("Done")


def getOSInfo():
    osName = None
    match name:
        case "posix":
            osName = "Linux"
        case "nt":
            osName = "Windows"
        case "Jython":
            osName = "Java"

    osRelease = release()
    osVersion = version()
    osArchitecture = machine()
    user = getlogin()
    return {"name": osName, "release": osRelease, "version": osVersion, "architecture": osArchitecture, "user": user}

def getStorageAmount(disk):
    uncalculatedStorageAmount = disk_usage(f"{disk}/").free
    return uncalculatedStorageAmount / (2 ** 30)

def getIPAddress():
    return gethostbyname(gethostname())

def getPrograms(operatingSystem):
    listOfPrograms = []

    if operatingSystem == "Windows":
        data = check_output(['wmic', 'product', 'get', 'name'])
        a = str(data)
        try:
            for i in range(len(a)):
                temp = a.split("\\r\\r\\n")[6:][i].strip()
                if temp not in ["", "'"]:
                    listOfPrograms.append(temp)
        except IndexError:
            print("Done")
    elif operatingSystem == "Linux":
        try:
            data = check_output(['dpkg', '-l'])
            packages = data.decode().split("\n")
            for i in packages:
                if i.startswith("ii"):
                    listOfPrograms.append(i.split()[1])
        except CalledProcessError as error:
            print(f"Error running dpkg: {error}")

    return listOfPrograms


if __name__ == '__main__':
    main()