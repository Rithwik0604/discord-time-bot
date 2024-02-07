import time
from datetime import datetime
from pytz import timezone
from tabulate import tabulate
from table2ascii import table2ascii as t2a, PresetStyle, Alignment
import json
import os

# * GLOBAL VARIABLES
zones = {
    "canada": timezone("America/Regina"),
    "us": timezone("America/New_York"),
    "uk": timezone("Europe/London"),
    "kuwait": timezone("Asia/Kuwait"),
    "india": timezone("Asia/Kolkata"),
}

# MAIN TIME FORMAT
# time_format = "%Y-%m-%d | %I:%M:%S %p"
time_format = "%I:%M:%S %p"


# TO GET THE TIME OUT OF A TEXT
def textParser(text):

    text_split = text.split("^")
    time_from_text = text_split[1].split(":")
    parse_time = [int(x) for x in time_from_text]
    return parse_time


# TO DISPLAY THE CURRENT TIME IN ALL ZONES
def allTime():
    reply = t2a(
        header=["Region", "Time"],
        body=[
            ["Canada", datetime.now(zones["canada"]).strftime(time_format)],
            ["USA", datetime.now(zones["us"]).strftime(time_format)],
            ["UK", datetime.now(zones["uk"]).strftime(time_format)],
            ["Kuwait", datetime.now(zones["kuwait"]).strftime(time_format)],
            ["India", datetime.now(zones["india"]).strftime(time_format)],
        ],
        style=PresetStyle.thin_compact_rounded,
        alignments=[Alignment.LEFT, Alignment.CENTER],
    )
    return reply


# TO GET CURRENT TIME AND DAY/DATE
localTime = time.gmtime()


# TO CONVERT TIME GOTTEN FROM PARSE-TEXT
def timeConvert(time_list, author):
    # data from json file
    data: dict = {}

    # check if file is empty then return alt message
    if os.path.getsize("./data.json") == 0:
        return "Your region is not set. Please use | /change-region | to set a region"

    # read json file
    with open("./data.json", "r") as f:
        data = json.loads(f.read())

    # setup for table format
    body_list = [] # body of table formatter
    keys = list(zones.keys()) # keys to access zones
    regions = ["Canada", "US", "UK", "Kuwait", "India"] # regions to write as reply
    currentTime = f"{time_list[0]}:{time_list[1]}" # getting time_list as str
    timeObject = datetime.strptime(currentTime, "%H:%M") # converting string to datetime
    outputTime = timeObject.strftime("%I:%M %p") # converting datetime to custom format

    # making the table format
    for i in range(len(zones)):
        if data[author] == keys[i]:
            continue
        given_time = datetime(
            localTime.tm_year,
            localTime.tm_mon,
            localTime.tm_mday,
            time_list[0],
            time_list[1],
            0,
            tzinfo=zones[data[author]],
        )
        body_list.append(
            [
                f"{outputTime} in {regions[i]}",
                given_time.astimezone(zones[keys[i]]).strftime(time_format),
            ]
        )
    reply = t2a(
        header=["Region", "Time"],
        body=body_list,
        style=PresetStyle.thin_compact_rounded,
        alignments=[Alignment.LEFT, Alignment.CENTER],
    )
    return reply


# TO CHANGE/SET THE REGION OF USER
def changeRegion(author: str, region: str):
    # if file was empty, to pass error
    if os.path.getsize("./data.json") == 0:
        with open("./data.json", "w") as f:
            f.write(json.dumps({author: region}))

    # data from the json file
    data = {}

    # getting data
    with open("./data.json", "r") as f:
        data = json.loads(f.read())

    # updating data
    data[author] = region

    # writing data
    with open("./data.json", "w") as f:
        f.write(json.dumps(data))

    return f"Region changed to {region}"


# print(timeConvert(["17", "30"], "588071959267508237"))
