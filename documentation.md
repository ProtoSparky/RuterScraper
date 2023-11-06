################################################
################################################

Lateness by bus line
File loc = ./SavedArea/latest/data.json

Example of file "
################################################

{
    "23 - Simensbråten": [
        "0:00:00"
    ],
    "23 - Brynseng T": [
        "0:00:12.333333"
    ],
    "25 - Tonsenhagen": [
        "0:05:15"
    ],
    "23 - Lysaker bru": [
        "0:00:37"
    ],
    "60 - Vippetangen": [
        "0:00:00"
    ],
    "23 - Radiumhospitalet": [
        "0:00:58.666667"
    ],
    "31 - Tonsenhagen": [
        "0:01:51"
    ],
    "4 - Linderud": [
        "0:00:00"
    ]
}

note time format is HH:MM:SS
################################################
################################################



Average lateness regardless of bus lines in 24h timeframe
FIle loc = ./SavedArea/normalDist/day/data.json

Example of file
################################################
{
    "16": "0:00:41.666667",
    "17": "0:01:01",
    "18": "0:05:31.8",
    "19": "0:01:01",
}

note time format is HH:MM:SS
################################################
################################################



Average lateness from all bus lines captured on specific timeframe
File Loc = ./SavedArea/normalDist/WeekRaw/data.json

Example of file
################################################
{
    "Sun-2023-11-05": [
        "0:00:00",
        "0:00:00",
        "0:05:15",
        "0:00:43",
        "0:00:00",
        "0:00:43",
        "0:00:00",
        "0:00:05",
        "0:01:51",
        "0:00:00",
        "0:00:00",
        "0:01:05",
        "0:00:00",
        "0:00:32",
        "0:00:00",
        "0:01:08",
        "0:00:00",
        "0:01:08"
    ]
}

note time format is HH:MM:SS
################################################
################################################



Average lateness on all weekdays. Sorted by day 
File Loc = ./SavedArea/normalDist/week/data.json

Example of file
################################################
{
    "Mon": 0,
    "Tue": 0,
    "Wed": 0,
    "Thu": 0,
    "Fri": 0,
    "Sat": 0,
    "Sun": "0:00:41.666667"
}

note time format is HH:MM:SS | Didnt run on all days, thats why the rest is 0
################################################
################################################

