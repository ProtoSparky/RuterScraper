import json 
import requests
import os
import time
from datetime import date
from datetime import datetime
import csv
import re 


dateNow = datetime.now()
currentDay = date.today()
currentTime = time.strftime("%H-%M-%S")
currentDayName = dateNow.strftime('%A')
shortDayName = currentDayName[0:3]
WeekArray = ["Mon", "Tue", "Wed", "Thu", "Fri"]
WeekArrayLength = len(WeekArray)
Bus = [
    #Platform A
    ["Buss nr", "Start stop",  "End stop",      "Start stop Latitude",  "Start stop Longitude", "End stop Latitude"   , "End stop Longitude"],
    ["23",      "Simensbråten", "Økern T",     "59.89563191255283",     "10.786966276240348" , "59.928373823342426"   , "10.806618014503611"], 
    ["23",      "Brynseng T",  "Økern T",      "59.90939973882401",     "10.813734558568134",  "59.928373823342426"   , "10.806618014503611"], #Start stopp er permanent stengt. MÅ endres
    ["60",      "Tonsenhagen",  "Økern T",      "59.947959839458",     "10.825428167640519",   "59.928373823342426"   , "10.806618014503611"],

    #Platform B
    ["23",     "Lysakerlokket",  "Økern T",     "59.914499844808674",  "10.640352012098626",   "59.928373823342426"    , "10.806618014503611"],
    ["60",     "Vippetangen",  "Økern T",       "59.90320553580005",   "10.741213856155149",   "59.928373823342426"    , "10.806618014503611"],
    ["24",     "Radiumhospitalet",  "Økern T", "59.928834249492155",   "10.659799721473952",   "59.928373823342426"    , "10.806618014503611"],

]



URL = "https://api.entur.io/journey-planner/v3/graphql"
HEAD = {
    "ET-Client-Name": "ProtoSparky-RuterEkspirment",
    "Content-Type": "application/json"
}

##################################################################################
##################################################################################
##################################################################################
#Api get
def GetData(HEAD, BusArray):
    graphql_query = {
        "query": """
        {
        trip(
            to: {
            coordinates: {
                latitude: """ + BusArray[5] +  """
                longitude: """ + BusArray[6] + """
            }
            },
            numTripPatterns: 2,
            from: {
            coordinates: {
                latitude: """ + BusArray[3] + """
                longitude: """ + BusArray[4] + """
            }
            }
        ) {
            tripPatterns {
            startTime
            expectedEndTime
            walkDistance
            legs {
                mode
                distance
                line {
                    publicCode
                authority {
                    name
                }
                }
                fromEstimatedCall {
                    quay {
                        name
                    }
                    aimedDepartureTime
                    expectedDepartureTime
                }
                toEstimatedCall {
                    quay {
                        name
                    }
                    cancellation
                    aimedDepartureTime
                    expectedDepartureTime
                }

                intermediateEstimatedCalls {
                    aimedDepartureTime
                    expectedDepartureTime
                    quay {
                        name
                    }
                }
            }
            }
        }
        }
        """
    }
    query_json = json.dumps(graphql_query)
    try:
        response = requests.post(URL, headers=HEAD, data=query_json)

        if response.status_code == 200:            
            #print("Response:", response.json())
            return response.json()
        else:
            print("Request failed with status code:", response.status_code)
            

    except Exception as e:
        print("An error occurred:", str(e))
##################################################################################
##################################################################################
##################################################################################
#Write chunk. Gets data from api, writes to file

def WriteData():
    Arr_len = len(Bus)
    DataExports = []
    CurrentKey = 1
    while CurrentKey < Arr_len:
        CurrentBus = Bus[CurrentKey]
        time.sleep(2)   
        savedData = GetData(HEAD, CurrentBus) 
        PublicBusCode = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["line"]["publicCode"]                                       #23, 60
        FromBusStop = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["fromEstimatedCall"]["quay"]["name"]                          #Simsenbråten, Økern, ulven torg
        ToBusStop = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["toEstimatedCall"]["quay"]["name"]                              #Økern T
        AimedDepartureTime = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["fromEstimatedCall"]["aimedDepartureTime"]             #2023-10-30T17:50:00+01:00
        ExpectedDepartureTime = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["fromEstimatedCall"]["expectedDepartureTime"]       #2023-10-30T18:00:00+01:00
        DeltaPredictedDepartureTime = str(datetime.fromisoformat(ExpectedDepartureTime) - datetime.fromisoformat(AimedDepartureTime))       #Delta of Expected and Predicted times
        ActualDepartureTime = -1                                                                                                            #2023-10-30T18:15:00+01:00 or -1 if undefined
        DeltaActualDepartureTime = -1
        AimedArrivalTime = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["toEstimatedCall"]["aimedDepartureTime"] 
        ExpectedArrivalTime = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["toEstimatedCall"]["expectedDepartureTime"] 
        DeltaPredictedArrivalTime = str(datetime.fromisoformat(ExpectedArrivalTime) - datetime.fromisoformat(AimedArrivalTime))
        ActualArrivalTime = -1 
        DeltaActualArrivalTime = -1
        IsCancelled = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["toEstimatedCall"]["cancellation"]                            #Returns true if route was cancelled

        Mode = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["mode"]                                                              #metro, bus etc
        Authority = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["line"]["authority"]["name"]
        TotalTravelTime = str(datetime.fromisoformat(ExpectedArrivalTime) - datetime.fromisoformat(ExpectedDepartureTime))

        DataExport = {
            "PublicBusCode": PublicBusCode,
            "FromBusStop":FromBusStop,
            "ToBusStop": ToBusStop, 
            "AimedDepartureTime": AimedDepartureTime, 
            "ExpectedDepartureTime": ExpectedDepartureTime, 
            "DeltaPredictedDepartureTime" : DeltaPredictedDepartureTime,
            "ActualDepartureTime": ActualDepartureTime,
            "DeltaActualDepartureTime": DeltaActualDepartureTime,
            "AimedArrivalTime" : AimedArrivalTime,
            "ExpectedArrivalTime": ExpectedArrivalTime,
            "DeltaPredictedArrivalTime": DeltaPredictedArrivalTime,
            "ActualArrivalTime": ActualArrivalTime,
            "DeltaActualArrivalTime" : DeltaActualArrivalTime,
            "IsCancelled": IsCancelled,
            "TotalTravelTime":TotalTravelTime, 
            "Mode/Authority": Mode + " / " + Authority, 
            "Debug":CurrentBus[0] + " " +  CurrentBus[1]
        }
        DataExports.append(DataExport)
        os.system('cls')
        print("Checking " + str(CurrentKey) + "/ " + str(Arr_len -1) + " | " + FromBusStop)

        CurrentKey += 1






    filepath  = "./SavedArea/raw/" + shortDayName + "-"+ str(currentDay)
    filenames =  "/" + shortDayName + "-" + currentTime + ".json"
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    currentFileLoc = str(filepath + filenames)
    with open(currentFileLoc, "w", encoding="utf-8") as json_file:
        #json.dump(DataExports, json_file, ensure_ascii=False)
        json.dump(DataExports, json_file, ensure_ascii=False, indent=4) #This one makes text in json more readable
##################################################################################
##################################################################################
##################################################################################

def NormalDistWeekRaw():
    raw_directory = "./SavedArea/raw"
    data_directory = "./SavedArea/normalDist/WeekRaw/"
    file_index_file = os.path.join(data_directory, "FileIndex.json")
    data_json_file = os.path.join(data_directory, "data.json")
    data = {}

    if os.path.exists(file_index_file):
        with open(file_index_file, "r") as index_file:
            data = json.load(index_file)
    
    # Get all json files in RAW
    for root, _, files in os.walk(raw_directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                
                # Check if data was written before this
                if file_path in data.get("FileLocation", []):
                    continue
                
                day_name = os.path.basename(root)
                
                # Read json data form raw dir data
                with open(file_path, "r") as json_file:
                    json_data = json.load(json_file)
                    for bus_info in json_data:
                        delta_departure_time = bus_info.get("DeltaPredictedDepartureTime")
                        if delta_departure_time is not None:
                            data.setdefault(day_name, []).append(delta_departure_time)
                
                data.setdefault("FileLocation", []).append(file_path)
    
    # Keep track of data written 
    with open(file_index_file, "w") as index_file:
        json.dump(data, index_file, indent=4)
        
    # Save new data
    if "FileLocation" in data:
        data.pop("FileLocation")
    with open(data_json_file, "w") as json_file:
        json.dump(data, json_file, indent=4)    
##################################################################################
##################################################################################
##################################################################################
'''
#Timer chunk
days2run = 1
times2run = (((days2run * 60) * 24) * days2run)
CurrentRun = 0
while CurrentRun < times2run:
    os.system('cls')
    WriteData()
    CurrentRun += 1
    os.system('cls')
    print("sleep for 60s")
    print("current run: " + str(CurrentRun))
    time.sleep(60)   
'''
##################################################################################
##################################################################################
##################################################################################
NormalDistWeekRaw()