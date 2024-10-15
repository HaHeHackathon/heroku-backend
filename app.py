"""
Application definition
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import requests
import json
import config
from datetime import datetime
from models import StationInfo, BusInfoModel
from database import SessionLocal, BusInfo
import random

app = FastAPI()

# Allow CORS for your localhost (or any other domain you trust)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "https://hahehackathon.github.io"],  # Can be a list of origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Base URLs for Deutsche Bahn's API
BASE_BOARD_DEPARTURE_URL = "https://apis.deutschebahn.com/db/apis/ris-boards/v1/public/departures"
BASE_BOARD_ARRIVAL_URL = "https://apis.deutschebahn.com/db/apis/ris-boards/v1/public/arrivals"

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():

    endpoints = {
        "/stop_places/": "Get list of stop places with their names and EVA numbers",
        "/departures/": "Get departure info for a station (query parameter: station_code)",
        "/arrivals/": "Get arrival info for a station with optional arrival_time (query parameter: station_code, arrival_time)"
    }
    return {"message": "Welcome to the Public Transport API!", "endpoints": endpoints}

@app.get("/stop_places/", response_model=list[StationInfo])
def get_stop_places():
    try:
        with open('filtered_stop_places.json', 'r', encoding='utf-8') as json_file:
            stop_places_data = json.load(json_file)
        return JSONResponse(content=stop_places_data, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading stop places: {str(e)}")

@app.get("/departures/")
def get_departures(station_code: str):
    try:
        board_departure_url = f"{BASE_BOARD_DEPARTURE_URL}/{station_code}"
        departure_response = requests.get(url=board_departure_url, headers=config.headers, params=config.params)

        if departure_response.status_code == 200:
            departure_data = departure_response.json()
            return JSONResponse(content=departure_data, media_type="application/json")
        else:
            raise HTTPException(status_code=departure_response.status_code, detail="Failed to fetch departure data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching departure data: {str(e)}")

@app.get("/arrivals/")
def get_arrivals(station_code: str, arrival_time: str = Query(None, description="Arrival time in format YYYY-MM-DDTHH:MM:SS")):
    try:
        board_arrival_url = f"{BASE_BOARD_ARRIVAL_URL}/{station_code}"
        params = config.params.copy()
        if arrival_time:
            try:
                datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%S")
                params["time"] = arrival_time
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid time format. Use 'YYYY-MM-DDTHH:MM:SS'.")

        arrival_response = requests.get(url=board_arrival_url, headers=config.headers, params=params)

        if arrival_response.status_code == 200:
            arrival_data = arrival_response.json()
            return JSONResponse(content=arrival_data, media_type="application/json")
        else:
            raise HTTPException(status_code=arrival_response.status_code, detail="Failed to fetch arrival data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching arrival data: {str(e)}")


@app.put("/update_passengers/")
def update_passengers(station_name: str, normal: int, wheelchair: int, elderly: int):
    db = next(get_db())
    bus_info = db.query(BusInfo).filter(BusInfo.stations['stationName'].astext == station_name).first()
    
    if not bus_info:
        raise HTTPException(status_code=404, detail="Bus info not found for the given station name.")
    
    for station in bus_info.stations:
        if station['stationName'] == station_name:
            station['checkedPassengers'] = {
                "normal": normal,
                "wheelchair": wheelchair,
                "elderly": elderly
            }
            break

    db.commit()
    return JSONResponse(content={"message": "Passenger counts updated successfully.", "stationName": station_name})

@app.get("/bus_info/")
def get_bus_info():
    db = next(get_db())
    bus_info = db.query(BusInfo).first()
    if not bus_info:
        raise HTTPException(status_code=404, detail="No bus info found.")
    
    # Constructing bus_info from the database entries
    bus_info_data = {
        "busLine": bus_info.bus_line,  # Using bus_line from the database
        "route": bus_info.route,        # Using route from the database
        "totalStations": bus_info.total_stations,  # Using total_stations from the database
        "stations": bus_info.stations    # Using stations from the database
    }

    print(bus_info)
    
    return JSONResponse(content=bus_info_data)  # Returning the constructed bus_info

@app.get("/404")
async def missing():
    return JSONResponse({"error": "That's gonna be a 'no' from me."}, status_code=404)

    db = next(get_db())
    existing_bus_info = db.query(BusInfo).first()
    
    # If bus info already exists, do not generate new dummy data
    if existing_bus_info:
        return JSONResponse(content={"message": "Dummy data already exists."})

    departure_info = load_departure_info()
    bus_info = {
        "busLine": "Bus 5",
        "route": "Hauptbahnhof - Altona",
        "totalStations": len(departure_info['departures']['station']),
        "stations": []
    }

    for departure in departure_info['departures']:
        station_name = departure['station']['name']
        estimated_arrival = departure['timeSchedule']  # Using timeSchedule as estimated arrival
        checked_passengers = {
            "normal": random.randint(10, 30),  # Random number between 10 and 30
            "wheelchair": random.randint(1, 5),  # Random number between 1 and 5
            "elderly": random.randint(1, 5)  # Random number between 1 and 5
        }
        bus_info['stations'].append({
            "stationName": station_name,
            "estimatedArrival": estimated_arrival,
            "checkedPassengers": checked_passengers
        })

    # Save the bus_info to the database
    db_bus_info = BusInfo(
        bus_line=bus_info['busLine'],
        route=bus_info['route'],
        total_stations=bus_info['totalStations'],
        stations=bus_info['stations']
    )
    db.add(db_bus_info)
    db.commit()
    db.refresh(db_bus_info)

    return JSONResponse(content={"message": "Dummy data generated and saved successfully.", "bus_info": bus_info})
