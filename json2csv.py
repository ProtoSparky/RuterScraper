'''import json
import csv
import os

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
            try:
                print("file removed")
                os.remove(ExcelOutputPath + bus_line_name + ".csv")
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

            BusCSVPath = ExcelOutputPath + bus_line_name + ".csv"
            is_new_file = not os.path.exists(BusCSVPath)

            with open(BusCSVPath, 'a', newline='') as BusCSV:
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
import json
import csv
import os
import unicodedata

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