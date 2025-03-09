

import requests
import csv
import time
import re

# Your Google API Key and Custom Search Engine ID (CX)
API_KEY = 'AIzaSyB8yLc6OweAQs3dSV90qPgQp1UibQD4vOY'  # Replace with your API key
CX = '6058d2d2b16294e2b'  # Replace with your Custom Search Engine ID

# Function to search Google Custom Search API
def google_search(query, api_key, cx):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cx
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to extract phone number and email from the results
def extract_contact_info(company_name, country):
    company_phone = None
    company_email = None

    # Search for Company Phone Number (focusing on snippets and knowledge graph)
    query = f"{company_name} {country} phone number"
    results = google_search(query, API_KEY, CX)
    if results:
        items = results.get("items", [])
        for item in items:
            snippet = item.get("snippet", "")
            # Search for phone numbers in snippets or Knowledge Graph
            phone_match = re.search(r'(\+?\d{1,2}\s?-?\(?\d{1,4}\)?\s?-?\d{1,4}\s?-?\d{1,4})', snippet)
            if phone_match:
                phone_number = phone_match.group(0)
                # Ensure the phone number is not a year (4-digit number) or zip code
                if not re.match(r'^\d{4}$', phone_number):  # Excludes 4-digit years like "2017"
                    # Ensure phone number is at least 8 digits long
                    digits_only = re.sub(r'\D', '', phone_number)
                    if len(digits_only) >= 8:  # Only accept phone numbers with at least 8 digits
                        company_phone = phone_number
                        break  # Stop after finding the first valid phone number

    # Search for Company Email Address
    query = f"{company_name} {country} email address"
    results = google_search(query, API_KEY, CX)
    if results:
        items = results.get("items", [])
        for item in items:
            snippet = item.get("snippet", "")
            # Search for email addresses in snippets or Knowledge Graph
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', snippet)
            if email_match:
                company_email = email_match.group(0)
                break  # Stop after finding the first email address

    return company_phone, company_email

# Main function to process the CSV input and output the results
def process_companies(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write headers
        writer.writerow(['Company Name', 'Country', 'Phone Number', 'Email Address'])

        for row in reader:
            company_name, country = row[0], row[1]
            
            # Fetch the company phone number and email from Google Search API
            company_phone, company_email = extract_contact_info(company_name, country)
            
            # Write results to the output CSV
            writer.writerow([company_name, country, company_phone, company_email])
            
            # Print progress
            print(f"Processed {company_name} ({country})")
            
            # Add a delay to avoid rate-limiting issues (respectful scraping)
            time.sleep(1)

# Run the process
input_csv = 'companies.csv'  # Path to your input CSV with company names and countries
output_csv = 'output.csv'    # Path to save the results
process_companies(input_csv, output_csv)