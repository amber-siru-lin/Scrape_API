import scrapy
import csv
from scrapy.http import HtmlResponse
from time import sleep
import random

class CompanySpider(scrapy.Spider):
    name = 'company_spider'

    def __init__(self, csv_file, *args, **kwargs):
        super(CompanySpider, self).__init__(*args, **kwargs)
        self.csv_file = csv_file  # Path to the CSV file with company name and country
        self.start_urls = []
        self.load_companies()

    def load_companies(self):
        # Read the CSV file and generate search queries for first 3 companies
        with open(self.csv_file, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            count = 0  # Counter to limit the number of companies
            for row in csv_reader:
                if count >= 3:  # Limit to first 3 companies for the test
                    break
                company_name = row[0]
                country = row[1]
                search_query = f"{company_name} {country} procurement contact"
                self.start_urls.append(f"https://www.google.com/search?q={search_query}")
                count += 1

    def parse(self, response):
        # Logging to show progress
        self.log(f"Processing page: {response.url}")

        # Extract links to company websites or details from search results
        links = response.css('.tF2Cxc a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_company_page)
        
        # Extract the company phone number from Google Knowledge Graph if possible
        phone_number = response.css('span.LrzXr::text').get()
        if phone_number:
            self.log(f"Found phone number: {phone_number}")
            yield {'phone_number': phone_number}

        self.log(f"Finished processing page: {response.url}")

    def parse_company_page(self, response):
        # Logging to show progress
        self.log(f"Processing company page: {response.url}")
        
        # Extract the company website
        company_website = response.url
        
        # Try to extract procurement contact from LinkedIn or similar
        procurement_contact = None
        linkedin_profile = None
        title = None
        
        # Look for LinkedIn profile link and title (simplified)
        linkedin_link = response.css('a[href*="linkedin.com"]::attr(href)').get()
        if linkedin_link:
            title = response.css('div.phhUmb::text').get()  # Adjust depending on page structure
            procurement_contact = linkedin_link
        
        # Extract the company's phone number from Google Knowledge Graph or the website
        phone_number = response.css('span.LrzXr::text').get()

        # Log the extracted data (for debugging)
        self.log(f"Found website: {company_website}")
        self.log(f"Found procurement contact: {procurement_contact} with title: {title}")

        # Introduce a random delay to avoid being blocked
        sleep(random.uniform(1, 3))

        # Yield the results
        yield {
            'company_website': company_website,
            'phone_number': phone_number,
            'procurement_contact': procurement_contact,
            'procurement_contact_title': title
        }