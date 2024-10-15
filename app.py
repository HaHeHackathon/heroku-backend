"""
Application definition
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for your localhost (or any other domain you trust)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "https://hahehackathon.github.io"],  # Can be a list of origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def home():
    return JSONResponse({
  "busLine": "Bus 5",
  "route": "Hauptbahnhof - Altona",
  "totalStations": 5,
  "stations": [
    {
      "stationName": "Hauptbahnhof",
      "estimatedArrival": "12:05",
      "checkedPassengers": {
        "normal": 10,
        "wheelchair": 1,
        "elderly": 2
      }
    },
    {
      "stationName": "Jungfernstieg",
      "estimatedArrival": "12:12",
      "checkedPassengers": {
        "normal": 8,
        "wheelchair": 0,
        "elderly": 1
      }
    },
    {
      "stationName": "Sternschanze",
      "estimatedArrival": "12:20",
      "checkedPassengers": {
        "normal": 15,
        "wheelchair": 2,
        "elderly": 3
      }
    },
    {
      "stationName": "Holstenstraße",
      "estimatedArrival": "12:27",
      "checkedPassengers": {
        "normal": 7,
        "wheelchair": 0,
        "elderly": 4
      }
    },
    {
      "stationName": "Altona",
      "estimatedArrival": "12:35",
      "checkedPassengers": {
        "normal": 5,
        "wheelchair": 1,
        "elderly": 2
      }
    }
  ]
}
)


@app.get("/404")
async def missing():
    return JSONResponse({"error": "That's gonna be a 'no' from me."}, status_code=404)
