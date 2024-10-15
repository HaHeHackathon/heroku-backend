import json
import random
from database import SessionLocal, BusInfo
from fastapi.responses import JSONResponse

# Load departure info from JSON file
def load_departure_info():
    with open('departure_info.json', 'r', encoding='utf-8') as dep_file:
        return json.load(dep_file)

def generate_dummy_data():
    db = SessionLocal()
    existing_bus_info = db.query(BusInfo).first()
    
    # If bus info already exists, do not generate new dummy data
    if existing_bus_info:
        return JSONResponse(content={"message": "Dummy data already exists."})

    departure_info = load_departure_info()
    print(departure_info['departures'])  # Changed to print the entire departures list

    # Accessing the first departure correctly
    first_departure = departure_info['departures'][0]  # Accessing the first departure
    print(first_departure['transport'])  # Accessing transport details

    # Using the 'via' list from the transport
    print(len(first_departure['transport']['via']))  # Correctly accessing via stops
    bus_info = {
        "busLine": "Bus 5",
        "route": "Luisenweg - Mühlenberg, Hamburg",
        "totalStations": len(first_departure['transport']['via']),
        "stations": []
    }

    for station in first_departure['transport']['via']:  # Iterating over the via stops
        station_name = station['name']  # Assuming each station has a 'name' key
        estimated_arrival = first_departure['timeSchedule']  # Using timeSchedule as estimated arrival
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

# Call the function to generate dummy data
if __name__ == "__main__":
    response = generate_dummy_data()
    print(response)
