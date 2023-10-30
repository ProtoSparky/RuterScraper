import json 
import requests
Bus = [
    #Platform A
    ["Buss nr", "Start stop",  "Slutt stop",  "Start stop Latitude",  "Start stop Longitude", "Slutt stop Latitude"  , "Slutt stop Longitude"],
    ["23",      "Simensbråten", "Økern T",     "59.89563191255283",     "10.786966276240348" ,  "59.928373823342426"   , "10.806618014503611"], 
    ["24",      "Brynseng T",  "Økern T",      "59.90939973882401",     "10.813734558568134",   "59.928373823342426"   , "10.806618014503611"], #Start stopp er permanent stengt. MÅ endres
    ["60",      "Tonsenhagen",  "Økern T",      "59.947959839458",     "10.825428167640519",   "59.928373823342426"    , "10.806618014503611"],

    #Platform B
    ["23",     "Lysakerlokket",  "Økern T",     "59.91299099325384",   "10.634388413944123",   "59.928373823342426"    , "10.806618014503611"],
    ["60",     "Vippetangen",  "Økern T",       "59.90320553580005",   "10.741213856155149",   "59.928373823342426"    , "10.806618014503611"],
    ["24",     "Radiumhospitalet",  "Økern T", "59.928834249492155",   "10.659799721473952",   "59.928373823342426"    , "10.806618014503611"],

]


apiURL = "https://api.entur.io/journey-planner/v3/graphql"
jcode = "{trip(to:{coordinates:{latitude:59.928373823342426 longitude:10.806618014503611}}numTripPatterns:2 from:{coordinates:{latitude:59.89563191255283 longitude:10.786966276240348}}){tripPatterns{startTime expectedEndTime walkDistance legs{mode distance line{publicCode authority{name}}fromEstimatedCall{quay{name}aimedDepartureTime expectedDepartureTime}toEstimatedCall{quay{name}aimedDepartureTime expectedDepartureTime}intermediateEstimatedCalls{aimedDepartureTime expectedDepartureTime quay{name}}}}}}"


response = requests.get(apiURL,jcode)
if response.status_code == 200:
    data = response.text
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")
