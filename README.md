# Best Travel Destinations in France — Data Pipeline Project

This project aims to build a comprehensive pipeline to identify the **best travel destinations in France** based on weather, enriching the data with information from **Booking.com** and then storing it in **AWS S3** and **PostgreSQL (RDS)**.

---

## 🧭 Project Objectives

1. **Data Collection**:
- List of the best cities in France
- GPS coordinates via [Nominatim API](https://nominatim.org/)
- Weather data via [OpenWeatherMap API](https://openweathermap.org/)
- Hotel scraping via Booking.com with Scrapy

2. **Data Processing**:
- Filter cities with **clear skies** and **average temperature > 11.5°C**
- Identify the **best destinations**
- Associate hotels with cities using reverse geocoding if needed

3. **Storage**:
- `.csv` and `.json` files saved in **AWS S3**
- Data loaded into a **PostgreSQL (AWS RDS)** database

4. **Visualization**:
- Interactive map with **Plotly** showing the best destinations

---

## 📁 Project structure

```

📦 project-root/
│
├── scripts/
│ ├── 0-destinations.py
│ ├── 1-Call\_API\_Nominatim.py
│ ├── 2-Call\_API\_OpenWeatherMap.py
│ └── 3-Scrapy\_on\_Booking.py
│
├── results/
│ ├── destination\_names.csv
│ ├── destination\_coordinates.csv
│ ├── weather\_data.csv
│ ├── best\_destinations.csv
│ ├── booking\_data.json
│ └── hotels\_data.csv
│
├── Data\_Collection.ipynb
├── Data\_Storage.ipynb
└── README.md

````

---

## ⚙️ Technologies used

- **Languages**: Python 3, SQL
- **Python libraries**: `pandas`, `plotly`, `sqlalchemy`, `requests`, `boto3`, `tqdm`, `dotenv`, `Scrapy`
- **API**: 
- [Nominatim](https://nominatim.org/) — geocoding
- [OpenWeatherMap](https://openweathermap.org/) — weather
- **Cloud**: AWS (S3 & RDS)
- **Database**: PostgreSQL

---

## 📝 Main Steps

### 1. Data Collection (`Data_Collection.ipynb`)
- Extract city names (via script)
- GPS coordinates via Nominatim API
- Weather data via OpenWeatherMap
- Filter destinations with "clear sky"
- Visualization on Plotly map
- Scraping hotels from Booking.com

### 2. Data Storage (`Data_Storage.ipynb`)
- Data cleaning (`NaN`, duplicates, etc.)
- Data enrichment (reverse geocoding of hotels)
- Upload `.csv` files and `.json` to AWS S3
- Creation of the `best_destinations` and `best_hotels` tables in PostgreSQL
- Inserting the data into the database
- SQL queries to display the top destinations and hotels

---

### 3. Configure the environment variables

Create an `.env` file with the AWS and PostgreSQL keys:

```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=eu-west-3
DBHOST=...
DBUSER=...
DBPASS=...
DBNAME=...
PORT=5432
```

---

## 📊 Visualizing the results

* Map of the best weather destinations with Plotly
* SQL queries for:

* Top 5 cities by temperature
* Top 20 hotels in these Cities

---

## 📦 Product Files

* `best_destinations.csv` — Optimal weather destinations
* `hotels_data.csv` — Hotels associated with destinations
* Stored in:

* 📁 `/results` (local)
* ☁️ AWS S3 (`block1-bucket`)
* 🛢️ PostgreSQL (AWS RDS)

---

## 🚀 Quick Run

1. Run all notebooks in order:

* `Data_Collection.ipynb`
* `Data_Storage.ipynb`

2. Observe the results (tables + map + SQL queries)

---

## 📌 Warning

* Some APIs have a **query quota** or require a key (OpenWeatherMap)
* Booking.com does not offer an official public API — scraping must comply with their usage policy.

---

## 👤 Author

Project by **Andriana**  
GitHub: [https://github.com/Andrianiniaina/0-DataCollection-and-Management-Project]
