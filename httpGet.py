import requests
from datetime import datetime
now = datetime.now()
current_time = now.strftime("%H.%M.%S")
 
# api-endpoint
URL = "https://api.entur.io/realtime/v1/rest/et?datasetId=RUT"
urlSmall = "https://api.entur.io/realtime/v1/rest/et?datasetId=RUT?maxSize=1000"
response = requests.get(URL)
if response.status_code == 200:
    data = response.text
    #print(data)
    currentFileLoc = str('./httpGetOutput/' + current_time +'.xml')
    with open(currentFileLoc, 'w') as f:
        f.write(data)
else:
    print(f"Request failed with status code {response.status_code}")