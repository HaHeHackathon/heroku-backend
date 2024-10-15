import json

# Load the departure info data
with open('departure_info.json', 'r', encoding='utf-8') as dep_file:
    departure_info = json.load(dep_file)

# Load the filtered stop places data
with open('filtered_stop_places.json', 'r', encoding='utf-8') as stop_file:
    filtered_stop_places = json.load(stop_file)

# Create a mapping of evaNumber to name from filtered_stop_places
eva_to_name = {place['evaNumber']: place['name'] for place in filtered_stop_places}

# Update the names in departure_info based on the mapping
for departure in departure_info['departures']:
    eva_number = departure['station']['evaNumber']
    if eva_number in eva_to_name:
        departure['station']['name'] = eva_to_name[eva_number]

# Save the updated departure info back to the JSON file
with open('departure_info.json', 'w', encoding='utf-8') as dep_file:
    json.dump(departure_info, dep_file, ensure_ascii=False, indent=4)