import json
from openpyxl import Workbook
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
#This code is broken DONT USE!
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


# Define the file paths
JsonFilePath = "./SavedArea/t_test/data.json"
ExcelOutputPath = "./SavedArea/t_test/"

# Load the JSON data
with open(JsonFilePath, 'r') as json_file:
    data = json.load(json_file)

# Iterate through the bus stops
for bus_stop in data["05.011.2023"]["17:14"]:
    # Create a new Excel workbook
    workbook = Workbook()
    sheet = workbook.active

    # Add headers for the Excel file
    sheet['D1'] = "Bus Line"
    sheet['E1'] = "Date Created"

    # Get the bus stop name
    bus_stop_name = bus_stop

    # Add the bus stop name and date to the Excel file
    sheet['D2'] = bus_stop_name
    sheet['E2'] = "2023-11-05"  # You can replace this with the actual date

    # Add headers for the time, AimedDepartureTime, and ExpectedDepartureTime
    sheet['A3'] = "Time"
    sheet['B3'] = "AimedDepartureTime"
    sheet['C3'] = "ExpectedDepartureTime"

    # Get the departure data for the bus stop
    departures = data["05.011.2023"]["17:14"][bus_stop]

    # Populate the Excel file with data
    row = 4
    for time, departures_info in departures.items():
        sheet[f'A{row}'] = time
        try:
            aimed_departure_time = departures_info.get("AimedDepartureTime", "").split("T")[1][:8]
        except (AttributeError, IndexError):
            aimed_departure_time = ""
        
        try:
            expected_departure_time = departures_info.get("ExpectedDepartureTime", "").split("T")[1][:8]
        except (AttributeError, IndexError):
            expected_departure_time = ""
        
        sheet[f'B{row}'] = aimed_departure_time
        sheet[f'C{row}'] = expected_departure_time
        row += 1

    # Save the Excel file with a name based on the bus stop
    excel_filename = f'{ExcelOutputPath}{bus_stop_name}.xlsx'
    workbook.save(excel_filename)

    print(f"Excel file '{excel_filename}' created for bus stop '{bus_stop_name}'")
