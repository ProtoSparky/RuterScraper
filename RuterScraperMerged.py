#This is a merged version containing json2csv.  If things go wrong here, they go really wrong!
import json 
import requests
import os
import time
from datetime import date
from datetime import datetime
from collections import defaultdict
from datetime import datetime, timedelta
import platform
import csv
import unicodedata


dateNow = datetime.now()
currentDay = date.today()
currentTime = time.strftime("%H-%M-%S")
currentDayName = dateNow.strftime('%A')
shortDayName = currentDayName[0:3]
WeekArray = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
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
    "ET-Client-Name": "Kuben Videregående Skole - 3STT ruter forsøk",
    "Content-Type": "application/json"
}



##################################################################################
##################################################################################
##################################################################################
def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
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
        AimedArrivalTime = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["toEstimatedCall"]["aimedDepartureTime"] 
        ExpectedArrivalTime = savedData["data"]["trip"]["tripPatterns"][0]["legs"][1]["toEstimatedCall"]["expectedDepartureTime"] 
        #DeltaPredictedArrivalTime = str(datetime.fromisoformat(ExpectedArrivalTime) - datetime.fromisoformat(AimedArrivalTime))
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
            "AimedArrivalTime" : AimedArrivalTime,
            "ExpectedArrivalTime": ExpectedArrivalTime,
            "IsCancelled": IsCancelled,
            "TotalTravelTime":TotalTravelTime, 
            "Mode/Authority": Mode + " / " + Authority,
            "OriginalBusCode":CurrentBus[0], #This is the bus that's supposed to service the line
            "OriginalStop":CurrentBus[1]   #This is the originl bus line that's supposed to be serviced
        }
        DataExports.append(DataExport)
        clear_screen()
        print("Checking " + str(CurrentKey) + "/ " + str(Arr_len -1) + " | " + FromBusStop)
        CurrentKey += 1
    filepath  = "./SavedArea/raw/" + shortDayName + "-"+ str(currentDay)
    filenames =  "/" + shortDayName + "-" + time.strftime("%H-%M-%S") + ".json"
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    currentFileLoc = str(filepath + filenames)
    with open(currentFileLoc, "w", encoding="utf-8") as json_file:
        #json.dump(DataExports, json_file, ensure_ascii=False)
        json.dump(DataExports, json_file, ensure_ascii=False, indent=4) #This one makes text in json more readable
##################################################################################
##################################################################################
##################################################################################
#Converts data chunks to readable json
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
# converts readable json to average lateness for each day in week
def NormalDistWeek(): 
    rawDistDir = "./SavedArea/normalDist/WeekRaw/data.json"
    processedDistDir = "./SavedArea/normalDist/week/data.json"    
    target_weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Read from rawDistDir
    with open(rawDistDir, 'r') as raw_file:
        raw_data = json.load(raw_file)
    
    # Create average for weekdays
    weekday_averages = {weekday: 0 for weekday in target_weekdays}
    count = defaultdict(int)  # count amount of weekdays
    
    # go trough that, and create average
    for date, times in raw_data.items():
        weekday = date.split('-')[0]
        if weekday in target_weekdays:
            for time in times:
                # Parse as hours:minutes:seconds
                hours, minutes, seconds = map(int, time.split(':'))
                time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                weekday_averages[weekday] += time_delta.total_seconds()
                count[weekday] += 1
    
    for weekday in target_weekdays:
        if count[weekday] > 0:
            average_seconds = weekday_averages[weekday] / count[weekday]
            average_time = str(timedelta(seconds=average_seconds))
            weekday_averages[weekday] = average_time
    
    with open(processedDistDir, 'w') as processed_file:
        json.dump(weekday_averages, processed_file, indent=4)
##################################################################################
##################################################################################
##################################################################################
#convert all data to normal dist for all hours 0-24
def NormalDistHour():
    RawData = "./SavedArea/raw"
    SavedData = "./SavedArea/normalDist/day/data.json"
    hour_averages = {}
    # Loop trough RAW
    for root, _, files in os.walk(RawData):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                # get hour form fileName
                hour = file.split("-")[1]
                # Round
                hour = int(hour)
                # Load data json
                with open(file_path, 'r') as f:
                    data = json.load(f)
                # Create average based on time
                total_duration = timedelta(0)
                num_entries = len(data)                
                for entry in data:
                    delta_time_str = entry["DeltaPredictedDepartureTime"]
                    parts = delta_time_str.split(":")
                    if len(parts) == 3:
                        hours, minutes, seconds = map(int, parts)
                        total_duration += timedelta(hours=hours, minutes=minutes, seconds=seconds)                
                average_duration = total_duration / num_entries
                # add average to arr 
                if hour in hour_averages:
                    hour_averages[hour].append(average_duration)
                else:
                    hour_averages[hour] = [average_duration]
    # get whole hour average
    for hour, average_duration_list in hour_averages.items():
        total_duration = sum(average_duration_list, timedelta(0))
        average_duration = total_duration / len(average_duration_list)
        hour_averages[hour] = str(average_duration)

    # create file structure
    result_data = {str(hour).zfill(2): average for hour, average in hour_averages.items()}
    # Write to SavedData file
    with open(SavedData, 'w') as f:
        json.dump(result_data, f, indent=4)
##################################################################################
##################################################################################
##################################################################################
#Creates a list of the average delays for all the busses
def SlowestPublicBusCode():
    RawData = "./SavedArea/raw"
    SavedData = "./SavedArea/latest/data.json"
    # Initialize a dictionary to store the average DeltaPredictedDepartureTime for each PublicBusCode and FromBusStop
    bus_code_and_stop_averages = defaultdict(list)

    # Traverse the directories in RawData
    for root, _, files in os.walk(RawData):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)

                # Load the JSON data from the file
                with open(file_path, 'r') as f:
                    data = json.load(f)

                for entry in data:
                    public_bus_code = entry["OriginalBusCode"]
                    from_bus_stop = entry["OriginalStop"]
                    delta_time_str = entry["DeltaPredictedDepartureTime"]

                    # Calculate the average DeltaPredictedDepartureTime for the bus code and FromBusStop
                    parts = delta_time_str.split(":")
                    if len(parts) == 3:
                        hours, minutes, seconds = map(int, parts)
                        total_seconds = hours * 3600 + minutes * 60 + seconds
                        bus_code_and_stop_averages[(public_bus_code, from_bus_stop)].append(total_seconds)

    # Calculate the average for each bus code and FromBusStop
    result_data = {}
    for (public_bus_code, from_bus_stop), delta_times in bus_code_and_stop_averages.items():
        total_seconds = sum(delta_times)
        average_duration = str(timedelta(seconds=total_seconds / len(delta_times)))
        result_data[f"{public_bus_code} - {from_bus_stop}"] = [average_duration]

    # Write the result to the SavedData file with ensure_ascii=False to correctly represent special characters
    with open(SavedData, 'w') as f:
        json.dump(result_data, f, indent=4, ensure_ascii=False)
##################################################################################
##################################################################################
##################################################################################
#This trims down all the files generated in raw to one json file for the csv conversion
def process_data():
    RawData = "./SavedArea/raw"
    SavedData = "./SavedArea/t_test/data.json"
    result_data = {}
    for root, dirs, files in os.walk(RawData):
        for file in files:
            if file.endswith(".json"):
                file_parts = file.split("-")
                hour_str = file_parts[1]
                minute_str = file_parts[2]
                second_str = file_parts[3][:-5]
                dir_parts = root.split("\\")
                date_str = dir_parts[-1]

                date = datetime.strptime(date_str, "%a-%Y-%m-%d")
                time = datetime.strptime(f"{hour_str}:{minute_str}:{second_str}", "%H:%M:%S")
                with open(os.path.join(root, file), "r", encoding='utf-8') as json_file:
                    data = json.load(json_file)

                for entry in data:
                    bus_code = entry["OriginalBusCode"]
                    from_bus_stop = entry["OriginalStop"]
                    aimed_departure_time = entry["AimedDepartureTime"]
                    expected_departure_time = entry["ExpectedDepartureTime"]
                    Delta_departure_time = entry["DeltaPredictedDepartureTime"]

                    date_key = date.strftime("%d.%m.%Y")
                    time_key = time.strftime("%H:%M:%S")
                    bus_stop_key = f"{bus_code} {from_bus_stop}"

                    if date_key not in result_data:
                        result_data[date_key] = {}

                    if time_key not in result_data[date_key]:
                        result_data[date_key][time_key] = {}

                    result_data[date_key][time_key][bus_stop_key] = {
                        "AimedDepartureTime": aimed_departure_time,
                        "ExpectedDepartureTime": expected_departure_time,
                        "DeltaPredictedDepartureTime": Delta_departure_time
                    }

    # Step 3: Save the resulting data in a JSON file with UTF-8 encoding
    with open(SavedData, "w", encoding='utf-8') as output_file:
        json.dump(result_data, output_file, ensure_ascii=False, indent=4)

    print("Data saved to", SavedData)
##################################################################################
##################################################################################
##################################################################################

def process_data2csv():
    JsonFilePath = "./SavedArea/t_test/data.json"
    ExcelOutputPath = "./SavedArea/t_test/"
    HEADER = ["Dayname", "HourName", "AimedDepartureTime", "ExpectedDepartureTime", "DeltaPredictedDepartureTime"]

    # Opening JSON file
    with open(JsonFilePath) as f:
        data = json.load(f)

    for Dayname in data:
        for HourName in data[Dayname]:
            for BusLine in data[Dayname][HourName]:
                # Extract bus line name
                bus_line_name = BusLine
                normalized_bus_line_name = unicodedata.normalize('NFKD', bus_line_name).encode('ASCII', 'ignore').decode('utf-8')
                try:
                    print("file removed")
                    os.remove(ExcelOutputPath + normalized_bus_line_name + ".csv")
                except:
                    print("file not found")

    # Opening JSON file
    with open(JsonFilePath) as f:
        data = json.load(f)

    for Dayname in data:
        for HourName in data[Dayname]:
            for BusLine in data[Dayname][HourName]:
                # Extract bus line name
                bus_line_name = BusLine
                normalized_bus_line_name = unicodedata.normalize('NFKD', bus_line_name).encode('ASCII', 'ignore').decode('utf-8')

                BusCSVPath = ExcelOutputPath + normalized_bus_line_name + ".csv"
                is_new_file = not os.path.exists(BusCSVPath)

                with open(BusCSVPath, 'a', newline='', encoding='utf-8') as BusCSV:
                    writer = csv.writer(BusCSV)

                    # Add header to the CSV file only if it's a new file
                    if is_new_file:
                        writer.writerow(HEADER)

                    for DataPoint in data[Dayname][HourName][BusLine]:
                        if DataPoint == "AimedDepartureTime":
                            SplitData2AimedDepartureTime = data[Dayname][HourName][BusLine][DataPoint].split("T")[1].split("+")[0]
                        elif DataPoint == "ExpectedDepartureTime":
                            SplitData2ExpectedDepartureTime = data[Dayname][HourName][BusLine][DataPoint].split("T")[1].split("+")[0]
                        elif DataPoint == "DeltaPredictedDepartureTime":
                            SplitData2DeltaPredictedDepartureTime = data[Dayname][HourName][BusLine][DataPoint]

                    # Write data to the CSV file
                    CSVData = f"{Dayname},{HourName},{SplitData2AimedDepartureTime},{SplitData2ExpectedDepartureTime},{SplitData2DeltaPredictedDepartureTime}"
                    writer.writerow(CSVData.split(','))
##################################################################################
##################################################################################
##################################################################################
def calculate_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def bytes_to_mb(size_in_bytes):
    # Convert bytes to megabytes (MB)
    return size_in_bytes / (1024 * 1024)

def stats():
    StatsData = "./stats/stats.json"
    RawData = "./SavedArea/raw"

    # Load the existing data from the JSON file
    try:
        with open(StatsData, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize it with an empty dictionary
        data = {}

    # Update the "LastRun" field with the current date and time
    data["LastRun"] = datetime.now().strftime("%d.%m.%Y @ %H:%M")

    # Count the number of folders and total files in the RawData directory
    total_files = 0
    total_dirs = 0
    for root, dirs, files in os.walk(RawData):
        total_dirs += len(dirs)
        total_files += len(files)

    # Calculate the total size of the root directory in MB
    total_project_size_bytes = calculate_directory_size(os.getcwd())
    total_project_size_mb = bytes_to_mb(total_project_size_bytes)

    # Update the JSON data with the folder and file counts and the total project size in MB
    data["TotalFileAmount"] = total_files
    data["TotalDirAmount"] = total_dirs
    data["TotalProjectSize"] = f"{total_project_size_mb:.2f} MB"  # Format the size as "XX.XX MB"

    # Write the updated data back to the JSON file
    with open(StatsData, 'w') as file:
        json.dump(data, file, indent=4)
##################################################################################
##################################################################################
##################################################################################

#process_data()
#SlowestPublicBusCode()
#NormalDistHour()
#NormalDistWeekRaw()
#NormalDistWeek()


##################################################################################
##################################################################################
##################################################################################
#Timer chunk
days2run = 1
times2run = (((days2run * 60) * 24) * days2run)
CurrentRun = 0
while CurrentRun < times2run:
    clear_screen()
    WriteData()
    process_data()
    SlowestPublicBusCode()
    NormalDistHour()
    NormalDistWeekRaw()
    NormalDistWeek()
    process_data2csv()
    stats()
    clear_screen()
    print("sleep for 60s")
    print("current run: " + str(CurrentRun))
    time.sleep(60)  
    CurrentRun += 1 
##################################################################################
##################################################################################
##################################################################################


