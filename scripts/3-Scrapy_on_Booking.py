import os
import logging
import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess

# Setup logging
logging.basicConfig(level=logging.INFO)

class BookingSpider(scrapy.Spider):
    
    # Define the spider's name
    name = "booking"
    
    # Define the custom settings
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": False},  # Launch Playwright with a visible window (helpful for debugging)
        "FEED_URI": "results/booking_data.json",  # Path to store the output
        "FEED_FORMAT": "json",
    }

    # Define the allowed domains for the spider
    start_url = "https://www.booking.com/searchresults.html"

    # Define the URL to start scraping
    destinations = [
        "Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens", "Lille", "Strasbourg",
        "Chateau du Haut Koenigsbourg", "Colmar", "Eguisheim", "Besancon", "Dijon", "Annecy", "Grenoble", "Lyon",
        "Gorges du Verdon", "Bormes les Mimosas", "Cassis", "Marseille", "Aix en Provence", "Avignon", "Uzes", "Nimes",
        "Aigues Mortes", "Saintes Maries de la mer", "Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban",
        "Biarritz", "Bayonne", "La Rochelle"
    ]
    
    # Starting requests for each destination
    def start_requests(self):
        logging.info("Starting to parse via destinations...")
        for destination in self.destinations:
            yield scrapy.Request(
                url=f"{self.start_url}?ss={destination}",
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "div[data-testid='property-card']")  # Wait for results to load
                    ],
                },
                headers={"User-Agent": self.custom_settings["USER_AGENT"]}
            )
    
    # Function to parse the list of hotels for each destination
    async def parse(self, response):
        logging.info(f"Parsing page: {response.url}")
        hotels = response.css("div[data-testid='property-card']")
        for hotel in hotels:
            hotel_name = hotel.css("div[data-testid='title']::text").get()
            hotel_link = response.urljoin(hotel.css("a::attr(href)").get())
            logging.info(f"Found hotel: {hotel_name}, Link: {hotel_link}")

            # Yielding hotel data to be followed for detailed extraction
            yield response.follow(hotel_link, self.parse_hotel, meta={'hotel_name': hotel_name, 'url': hotel_link})

    # Function to parse the hotel detail page
    async def parse_hotel(self, response):
        logging.info(f"Entering hotel details page for {response.meta['hotel_name']}...")

        # Extract hotel details
        hotel_name = response.meta['hotel_name']
        hotel_url = response.meta['url']
        
        # Update the score and description extraction
        # score = " ".join(response.css("div[data-testid='review-score-right-component'] ::text").getall()).strip()
        score = self.extract_score(response)

        description = response.css("div.hp_desc_main_content p[data-testid='property-description']::text").get()
        
        # Extract latitude and longitude from the address
        latitude_longitude = response.css("a#map_trigger_header::attr(data-atlas-latlng)").get()
        
        if latitude_longitude:
            latitude, longitude = latitude_longitude.split(',')
        else:
            latitude = longitude = None

        # Log the information
        logging.info(f"Found details for {hotel_name}: Score={score}, Latitude={latitude}, Longitude={longitude}")

        # Yielding the hotel data including additional details
        yield {
            'name': hotel_name,
            'score': score,
            'description': description,
            'latitude': latitude,
            'longitude': longitude,
            'url': hotel_url
        }

    def extract_score(self, response):
        raw_score_text = " ".join(response.css("div[data-testid='review-score-right-component'] ::text").getall()).strip()
        parts = raw_score_text.split(" ")
        if len(parts) > 1:
            return parts[1]
        return None

# Main block to execute the spider
if __name__ == "__main__":
    # Create a CrawlerProcess instance with custom settings
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'LOG_LEVEL': logging.INFO,
        "FEEDS": {
            "results/booking_data.json": {"format": "json"},
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    })

    # Run the spider
    process.crawl(BookingSpider)
    process.start()