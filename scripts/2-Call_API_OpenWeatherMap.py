from dotenv import load_dotenv
load_dotenv()

import os
import requests
import time
import pandas as pd

# Get the API key from the environment variable
appid = os.getenv('API_KEY')

# Exclude useless data
exclude = ['current', 'minutely', 'hourly', 'alerts']

# Read csv file with coordinates
city_df = pd.read_csv('results/destination_coordinates.csv')

# Initialize list to store the data
all_weather_data = []

# Loop through the dataframe
for index, row in city_df.iterrows():
    # Get the city name
    city = row['destination']
    # Get the latitude and longitude
    lat = row['lat']
    lon = row['lon']

    # Request parameters
    payload = {
        "lat": lat,
        "lon": lon,
        "exclude": ",".join(exclude),
        "appid": appid,
        "lang": "fr",
        "format": "json",
        "units": "metric"
    }

    # Make the request
    url_api = "https://api.openweathermap.org/data/3.0/onecall"
    response = requests.get(url_api, params=payload)

    # Check the status code
    if response.status_code == 200:
        
        # Get the data
        data = response.json()

        # Extract necessary data for each city
        if "daily" in data and len(data["daily"]) > 0:

            # Get the daily data
            daily_data = data["daily"][0]
            temp_day = daily_data["temp"]["day"]
            description = daily_data["weather"][0]["description"]

        # Extract the temperature for 7 next days
        if "daily" in data and len(data["daily"]) >= 7:
            
            # Initialize the list of temperatures
            temperatures = []

            # Loop through the next 7 days
            for day in data["daily"][:7]:
                # Get the temperature and add it to the list
                temperatures.append(day["temp"]["day"])
            
            # Get the average temperature for the next 7 days
            avg_temp = sum(temperatures) / len(temperatures)

            # Add the average temperature to the dataframe
            all_weather_data.append(
                {
                    "city": city,
                    "lat": lat,
                    "lon": lon,
                    "temp_day": temp_day,
                    "avg_temp": avg_temp,
                    "description": description
                }
            )
        else:
            print(f"No data available for {city} : {response.status_code}")
    
    time.sleep(0.5)

# Save the data to a CSV file
results_dir = os.path.join('results')
weather_df = pd.DataFrame(all_weather_data)
print("Saving weather data into a csv file ...")
filepath= os.path.join(results_dir, "weather_data.csv")
weather_df.to_csv(filepath, index=False)
print("Done !")
print(f"All weather data are stored into : {filepath}")