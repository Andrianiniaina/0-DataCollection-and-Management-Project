import requests
import time
import os
import pandas as pd

# Call API
url_api = "https://nominatim.openstreetmap.org/search"
headers = {
    "User-Agent" : "MyPythonScript/1.0",
    "Referer" : "https://mywebsite.com/page.html"
}

# Read cvs file to get destinations
destinations = pd.read_csv("results/destination_names.csv")

# Create a dataframe to store the results
columns = ["destination", "lat", "lon"]

# Initialize the dataframe
df = pd.DataFrame(columns=columns)

# Loop through the destinations
for i in range(len(destinations)):

    # Request parameters
    q = destinations.loc[i, 'destination']
    payload = {
        "q": q,
        "format": "json",
        "limit": 1,
        "accept_language": "fr-FR",
    }

    # Make the request
    try:

        # Send the request
        response = requests.get(url_api, headers=headers, params=payload)

        # Check the status code
        if response.status_code != 200:
            print(f"Error: {response.status_code} for {q}")
            continue

        # Try to decode the JSON response
        try:
            json_data = response.json()

            # Check if the response is empty
            if len(json_data) > 0 :

                # Get location data
                location_data = json_data[0]

                # Create a dictionary with the location data
                location_dict = {
                    "destination" : location_data.get("name", None),
                    "lat" : location_data.get("lat", None),
                    "lon" : location_data.get("lon", None)
                }

                # Append the location data to the dataframe
                df = pd.concat([df, pd.DataFrame([location_dict])], ignore_index=True)
            else :
                pass
        except ValueError:
            print(f"Error JSON : Invalid response for {q}, response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error : {e}")

""" Exxample of response :
[{
    'place_id': 277106181,
    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright',
    'osm_type': 'relation',
    'osm_id': 905534,
    'lat': '48.649518',
    'lon': '-2.0260409',
    'class': 'boundary',
    'type': 'administrative',
    'place_rank': 16,
    'importance': 0.6170333686756257,
    'addresstype': 'town',
    'name': 'Saint-Malo',
    'display_name': 'Saint-Malo, Ille-et-Vilaine, Bretagne, France métropolitaine, 35400, France',
    'boundingbox': ['48.5979853', '48.6949736', '-2.0765246', '-1.9367259']
}]
"""

# Wait for 1 second before making the next request
time.sleep(0.5)

# Save the dataframe to a csv file
results_dir = os.path.join('results')
print("Saving destinations into a csv file ...")
filepath= os.path.join(results_dir, "destination_coordinates.csv")
df.to_csv(filepath, index=False)
print("Done !")
print(f"All coordinates are stored into : {filepath}")