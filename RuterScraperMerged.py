#This is a merged version containing json2csv.  If things go wrong here, they go really wrong!
#If you think something in code is hacky, remember that humanity has somehow convinced a rock to think using lightning
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
from collections import OrderedDict
from statistics import median
from statistics import mean, median

WeekArray = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DataFails = 0
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
    "ET-Client-Name": "Kuben Videregående Skole - 3STT ruter forsøk | kakra038@osloskolen.no",
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
    dateNow = datetime.now()
    currentDay = date.today()
    currentTime = time.strftime("%H-%M-%S")
    currentDayName = dateNow.strftime('%A')
    shortDayName = currentDayName[0:3]
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
    # Define directories
    raw_directory = "./SavedArea/raw"
    data_directory = "./SavedArea/normalDist/WeekRaw/data.json"

    # Initialize a dictionary to store the data
    data = {}

    # List all directories in the raw_directory
    for dir_name in os.listdir(raw_directory):
        dir_path = os.path.join(raw_directory, dir_name)
        
        # Check if it's a directory
        if os.path.isdir(dir_path):
            delta_times = []
            
            # List all JSON files in the directory
            for file_name in os.listdir(dir_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(dir_path, file_name)
                    
                    with open(file_path, 'r') as file:
                        content = json.load(file)
                        for entry in content:
                            delta_times.append(entry.get("DeltaPredictedDepartureTime", "0:00:00"))
            
            # Calculate the average delta time for this directory
            if delta_times:
                total_seconds = sum(
                    int(x.split(':')[0]) * 3600 + int(x.split(':')[1]) * 60 + int(x.split(':')[2]) for x in delta_times
                )
                average_seconds = total_seconds // len(delta_times)
                hours, remainder = divmod(average_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                average_time = f"{hours:02}:{minutes:02}:{seconds:02}"
                data[dir_name] = delta_times
                data[dir_name].insert(0, average_time)

    # Save the data dictionary to data_directory
    with open(data_directory, 'w') as data_file:
        json.dump(data, data_file, indent=4)

    print("Data processing and saving completed.")
##################################################################################
##################################################################################
##################################################################################
'''
##This is the old code. If bad shit happens, use this
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
'''
def NormalDistWeek(): 
    rawDistDir = "./SavedArea/normalDist/WeekRaw/data.json"
    processedDistDir = "./SavedArea/normalDist/week/data.json"    
    target_weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Read from rawDistDir
    with open(rawDistDir, 'r') as raw_file:
        raw_data = json.load(raw_file)
    
    # Create average, median, and max for weekdays
    weekday_averages = {weekday: timedelta(seconds=0) for weekday in target_weekdays}
    weekday_medians = {weekday: [] for weekday in target_weekdays}
    weekday_maxs = {weekday: timedelta(seconds=0) for weekday in target_weekdays}
    count = defaultdict(int)  # count amount of weekdays
    
    # go through that, and create average, median, and max
    for date, times in raw_data.items():
        weekday = date.split('-')[0]
        if weekday in target_weekdays:
            for time in times:
                # Parse as hours:minutes:seconds
                hours, minutes, seconds = map(int, time.split(':'))
                time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                weekday_averages[weekday] += time_delta
                weekday_medians[weekday].append(time_delta.total_seconds())
                weekday_maxs[weekday] = max(weekday_maxs[weekday], time_delta)
                count[weekday] += 1
    
    result_data = {}
    
    for weekday in target_weekdays:
        if count[weekday] > 0:
            # Calculate median
            #median_seconds = sorted(weekday_medians[weekday])[len(weekday_medians[weekday]) // 2]
            sorted_medians = sorted(weekday_medians[weekday])
            median_seconds = sorted_medians[len(sorted_medians) // 2]
            median_time = str(timedelta(seconds=median_seconds))
            
            result_data[weekday] = {
                "AvgTime": str(weekday_averages[weekday] / count[weekday]),
                "AvgTimeSeconds": weekday_averages[weekday].total_seconds() / count[weekday],
                "MedianTime": median_time,
                "MedianTimeSeconds": median_seconds,
                "MaxTime": str(weekday_maxs[weekday]),
                "MaxTimeSeconds": weekday_maxs[weekday].total_seconds()
            }
        else:
            # If no data, set all values to 0
            result_data[weekday] = {
                "AvgTime": "0:00:00",
                "AvgTimeSeconds": 0,
                "MedianTime": "0:00:00",
                "MedianTimeSeconds": 0,
                "MaxTime": "0:00:00",
                "MaxTimeSeconds": 0
            }
    
    with open(processedDistDir, 'w') as processed_file:
        json.dump(result_data, processed_file, indent=4)
##################################################################################
##################################################################################
##################################################################################
#convert all data to normal dist for all hours 0-24
'''
##This is the old code. If bad shit happens, use this
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

    result_data = {str(hour).zfill(2): average for hour, average in sorted(hour_averages.items())} #Bugfix 
    # Write to SavedData file
    with open(SavedData, 'w') as f:
        json.dump(result_data, f, indent=4)
'''
def NormalDistHour():
    RawData = "./SavedArea/raw"
    SavedData = "./SavedArea/normalDist/day/data.json"
    hour_data = {}

    # Loop through RAW
    for root, _, files in os.walk(RawData):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                # Get hour from fileName
                hour = file.split("-")[1]
                hour = int(hour)
                # Load data json
                with open(file_path, 'r') as f:
                    data = json.load(f)
                # Create list to store DeltaPredictedDepartureTime values
                delta_times = []
                for entry in data:
                    delta_time_str = entry["DeltaPredictedDepartureTime"]
                    parts = delta_time_str.split(":")
                    if len(parts) == 3:
                        hours, minutes, seconds = map(int, parts)
                        total_seconds = hours * 3600 + minutes * 60 + seconds
                        delta_times.append(total_seconds)
                
                # Calculate average time in seconds
                avg_time_seconds = sum(delta_times) / len(delta_times)
                # Calculate maximum time in seconds
                max_time_seconds = max(delta_times)
                # Calculate median time in seconds
                median_time_seconds = median(delta_times)
                
                # Add data to hour_data dictionary with hour + 1
                hour_data[hour + 1] = {
                    "AvgTime": str(timedelta(seconds=avg_time_seconds)),
                    "AvgTimeSeconds": avg_time_seconds,
                    "MaxTime": str(timedelta(seconds=max_time_seconds)),
                    "MaxTimeSeconds": max_time_seconds,
                    "MedianTime": str(timedelta(seconds=median_time_seconds)),
                    "MedianTimeSeconds": median_time_seconds
                }

    # Write to SavedData file
    with open(SavedData, 'w') as f:
        json.dump(hour_data, f, indent=4)
##################################################################################
##################################################################################
##################################################################################
#Creates a list of the average delays for all the busses
'''
##This is the old code. If bad shit happens, use this
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
'''
def SlowestPublicBusCode():
    RawData = "./SavedArea/raw"
    SavedData = "./SavedArea/latest/data.json"
    # Initialize a dictionary to store the average, median, and max DeltaPredictedDepartureTime for each PublicBusCode and FromBusStop
    bus_code_and_stop_data = defaultdict(list)

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

                    # Calculate the DeltaPredictedDepartureTime for the bus code and FromBusStop
                    parts = delta_time_str.split(":")
                    if len(parts) == 3:
                        hours, minutes, seconds = map(int, parts)
                        total_seconds = hours * 3600 + minutes * 60 + seconds
                        bus_code_and_stop_data[(public_bus_code, from_bus_stop)].append(total_seconds)

    # Calculate the average, median, and max for each bus code and FromBusStop
    result_data = {}
    for (public_bus_code, from_bus_stop), delta_times in bus_code_and_stop_data.items():
        total_seconds_avg = sum(delta_times) / len(delta_times)
        average_duration = str(timedelta(seconds=total_seconds_avg))
        median_duration = str(timedelta(seconds=sorted(delta_times)[len(delta_times) // 2]))
        max_duration = str(timedelta(seconds=max(delta_times)))

        result_data[f"{public_bus_code} - {from_bus_stop}"] = {
            "AvgTime": average_duration,
            "MedianTime": median_duration,
            "MaxTime": max_duration,
            "AvgTimeSeconds": total_seconds_avg,
            "MedianTimeSeconds": sorted(delta_times)[len(delta_times) // 2],
            "MaxTimeSeconds": max(delta_times)
        }

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
    
    result_data = OrderedDict()
    
    for root, dirs, files in os.walk(RawData):
        for file in files:
            if file.endswith(".json"):
                file_parts = file.split("-")
                hour_str = file_parts[1]
                minute_str = file_parts[2]
                second_str = file_parts[3][:-5]
                dir_parts = root.split("\\")
                date_str = (dir_parts[-1])[4:] if platform.system() == 'Windows' else (dir_parts[-1])[20:]
                
                date = datetime.strptime(date_str, "%Y-%m-%d")
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
                        result_data[date_key] = OrderedDict()

                    if time_key not in result_data[date_key]:
                        result_data[date_key][time_key] = OrderedDict()

                    result_data[date_key][time_key][bus_stop_key] = {
                        "AimedDepartureTime": aimed_departure_time,
                        "ExpectedDepartureTime": expected_departure_time,
                        "DeltaPredictedDepartureTime": Delta_departure_time
                    }

    # Sort the result_data dictionary by date and time
    sorted_result_data = OrderedDict(sorted(result_data.items()))

    for date_key, date_value in sorted_result_data.items():
        sorted_result_data[date_key] = OrderedDict(sorted(date_value.items()))
        for time_key, time_value in sorted_result_data[date_key].items():
            sorted_result_data[date_key][time_key] = OrderedDict(sorted(time_value.items()))

    # Save the sorted data to a JSON file
    with open(SavedData, "w", encoding='utf-8') as output_file:
        json.dump(sorted_result_data, output_file, ensure_ascii=False, indent=4)

    print("Data saved to", SavedData)
##################################################################################
##################################################################################
##################################################################################
'''
##This is the old code. If bad shit happens, use this
def process_data2csv():
    JsonFilePath = "./SavedArea/t_test/data.json"
    ExcelOutputPath = "./SavedArea/t_test/"
    HEADER = ["Dayname", "HourName", "AimedDepartureTime", "ExpectedDepartureTime", "DeltaPredictedDepartureTime"]

    CSVARR = ["23 Brynseng T.csv", "23 Lysakerlokket.csv", "23 SimensbrAten.csv", "24 Radiumhospitalet.csv", "60 Tonsenhagen.csv", "60 Vippetangen.csv"]
    for CurrentCSV in CSVARR:
        try:
            os.remove(ExcelOutputPath + CurrentCSV)
            print("file removed")
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
'''
def process_data2csv():
    JsonFilePath = "./SavedArea/t_test/data.json"
    ExcelOutputPath = "./SavedArea/t_test/"
    HEADER = ["Dayname", "HourName", "AimedDepartureTime", "ExpectedDepartureTime", "DeltaPredictedDepartureTime", "DeltaPredictedDepartureTimeSeconds"]

    CSVARR = ["23 Brynseng T.csv", "23 Lysakerlokket.csv", "23 Simensbraten.csv", "24 Radiumhospitalet.csv", "60 Tonsenhagen.csv", "60 Vippetangen.csv"]
    for CurrentCSV in CSVARR:
        try:
            os.remove(ExcelOutputPath + CurrentCSV)
            print("file removed")
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
                            # Convert DeltaPredictedDepartureTime to seconds
                            time_parts = SplitData2DeltaPredictedDepartureTime.split(":")
                            delta_seconds = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
                            DeltaPredictedDepartureTimeSeconds = str(delta_seconds)

                    # Write data to the CSV file
                    CSVData = f"{Dayname},{HourName},{SplitData2AimedDepartureTime},{SplitData2ExpectedDepartureTime},{SplitData2DeltaPredictedDepartureTime},{DeltaPredictedDepartureTimeSeconds}"
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

def stats(TimeBeforeRun):
    TimeDuringRun = datetime.now()
    StatsData = "./stats/stats.json"
    RawData = "./SavedArea/raw"

    # Load the existing data from the JSON file
    try:
        with open(StatsData, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize it with an empty dictionary
        data = {}
    current_time = datetime.now()
    one_hour_later = current_time + timedelta(hours=1)
    formatted_time = one_hour_later.strftime("%d.%m.%Y @ %H:%M")
    data["LastRun"] = formatted_time

    time_difference = TimeDuringRun - TimeBeforeRun
    seconds = time_difference.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    TotalRunTime = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
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
    data["ProcessingTime"] = TotalRunTime
    data["FailedComponents"] = DataFails

    # Write the updated data back to the JSON file
    with open(StatsData, 'w') as file:
        json.dump(data, file, indent=4)
##################################################################################
##################################################################################
##################################################################################
##Reads from raw, and generates hourly data for each weekday
def parse_time(time_str):
    h, m, s = map(int, time_str.split(':'))
    return timedelta(hours=h, minutes=m, seconds=s)

def DayPerWeek():
    results = {"Mon": {}, "Tue": {}, "Wed": {}, "Thu": {}, "Fri": {}, "Sat": {}, "Sun": {}}
    
    def process_directory(directory):
        nonlocal results
        day_abbrev = directory.split(os.path.sep)[-1].split('-')[0]
        day_data = results.get(day_abbrev, OrderedDict())

        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    
                    delta_times = [time.total_seconds() for time in [parse_time(bus["DeltaPredictedDepartureTime"]) for bus in data]]
                    avg_delta_time = str(timedelta(seconds=mean(delta_times)))

                    # Modify this line to add 1 to the extracted hour
                    hour = str(int(filename.split('-')[1]) + 1)

                    hour_data = day_data.get(hour, {"AvgTime": "0:00:00", "MedianTime": "0:00:00", "MaxTime": "0:00:00"})
                    hour_data["AvgTime"] = avg_delta_time
                    hour_data["AvgTimeSeconds"] = int(mean(delta_times))
                    hour_data["MedianTime"] = str(timedelta(seconds=median(delta_times)))
                    hour_data["MedianTimeSeconds"] = int(median(delta_times))
                    hour_data["MaxTime"] = str(timedelta(seconds=max(delta_times, default=0)))
                    hour_data["MaxTimeSeconds"] = int(max(delta_times, default=0))
                    day_data[hour] = hour_data

        if day_data:
            if day_abbrev in results:
                existing_data = results[day_abbrev]
                for hour, data in day_data.items():
                    existing_data[hour] = data
            else:
                results[day_abbrev] = day_data

    for subdir in os.listdir("./SavedArea/raw"):
        subdir_path = os.path.join("./SavedArea/raw", subdir)
        if os.path.isdir(subdir_path):
            process_directory(subdir_path)

    output_path = "./SavedArea/normalDist/DayPerWeek/data.json"
    with open(output_path, 'w') as output_file:
        json.dump(results, output_file, indent=4)

##################################################################################
##################################################################################
##################################################################################

#Timer chunk
days2run = 30
times2run = (((days2run * 60) * 24) * days2run)
CurrentRun = 0
while CurrentRun < times2run:
    TimeBeforeRun = datetime.now()
    clear_screen()
    '''
    try: 
        WriteData()        
    except: 
        DataFails =+ 1
        print("WriteData failed! Good luck")
        time.sleep(3)    
    '''
    ################################################
    try: 
        process_data()        
    except: 
        DataFails =+ 1
        print("Process_Data() failed! Good luck")
        time.sleep(3)
    ################################################ 
    try: 
        SlowestPublicBusCode()
    except: 
        DataFails =+ 1    
        print("SlowestPublicBusCode failed! Good luck")
        time.sleep(3) 
    ################################################
    try: 
        NormalDistHour()
    except: 
        DataFails =+ 1
        print("NormalDistHour failed! Good luck")
        time.sleep(3) 
    ################################################
    try: 
        NormalDistWeekRaw()
    except: 
        DataFails =+ 1
        print("NormalDistWeekRaw failed! Good luck")
        time.sleep(3) 
    ################################################
    try: 
        NormalDistWeek()
    except: 
        DataFails =+ 1
        print("NormalDistWeek failed! Good luck")
        time.sleep(3) 
    ################################################
    try: 
        process_data2csv()
    except: 
        DataFails =+ 1
        print("Process_data2csv failed! Good luck")
        time.sleep(3) 
    ################################################
    try: 
        DayPerWeek()
    except: 
        DataFails =+ 1
        print("Process_DayPerWeek failed! Good luck")
        time.sleep(3) 
    ################################################
    
    stats(TimeBeforeRun)
    clear_screen()
    print("sleep for 60s")
    print("current run: " + str(CurrentRun))
    time.sleep(60)  
    CurrentRun += 1 
##################################################################################
##################################################################################
##################################################################################


