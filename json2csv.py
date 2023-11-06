'''JsonFilePath = "./SavedArea/t_test/data.json"
ExcelOutputPath = "./SavedArea/t_test/"

import json 
import csv
# Opening JSON file
f = open(JsonFilePath)
data = json.load(f)
for Dayname in data:
    for HourName in data[Dayname]:
        for BusLine in data[Dayname][HourName]:

            SplicedBusLine1 = BusLine.split(" ")[0]
            SplicedBusLine2 = BusLine.split(" ")[1]
            SplicedBusLine = SplicedBusLine1 + SplicedBusLine2
            BusCSV = open(ExcelOutputPath + SplicedBusLine + ".csv", 'w')
            writer = csv.writer(BusCSV)


            for DataPoint in data[Dayname][HourName][BusLine]:
                if DataPoint == "AimedDepartureTime":
                    Data = data[Dayname][HourName][BusLine][DataPoint]
                    SplitData = Data.split("T")[1]
                    SplitData2AimedDepartureTime = SplitData.split("+")[0]

                elif DataPoint == "ExpectedDepartureTime":
                    Data = data[Dayname][HourName][BusLine][DataPoint]
                    SplitData = Data.split("T")[1]
                    SplitData2ExpectedDepartureTime = SplitData.split("+")[0]
            

            CSVData = Dayname + "," + HourName + "," + SplitData2AimedDepartureTime + "," + SplitData2ExpectedDepartureTime
            print(CSVData)
        #writer.writerow(forArr)




f.close()
'''

import json
import csv
import os

JsonFilePath = "./SavedArea/t_test/data.json"
ExcelOutputPath = "./SavedArea/t_test/"

# Opening JSON file
with open(JsonFilePath) as f:
    data = json.load(f)

for Dayname in data:
    for HourName in data[Dayname]:
        for BusLine in data[Dayname][HourName]:
            # Extract bus line name
            bus_line_name = BusLine
            try:
                print("file rmeoved")
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

            BusCSV = open(ExcelOutputPath + bus_line_name + ".csv", 'a', newline='')  # Use 'newline=' parameter for Windows compatibility
            writer = csv.writer(BusCSV)

            for DataPoint in data[Dayname][HourName][BusLine]:
                if DataPoint == "AimedDepartureTime":
                    SplitData2AimedDepartureTime = data[Dayname][HourName][BusLine][DataPoint].split("T")[1].split("+")[0]
                elif DataPoint == "ExpectedDepartureTime":
                    SplitData2ExpectedDepartureTime = data[Dayname][HourName][BusLine][DataPoint].split("T")[1].split("+")[0]

            # Write data to the CSV file
            CSVData = f"{Dayname},{HourName},{SplitData2AimedDepartureTime},{SplitData2ExpectedDepartureTime}"
            writer.writerow(CSVData.split(','))

            BusCSV.close()