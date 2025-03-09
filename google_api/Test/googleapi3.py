

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

# Function to extract phone number, email, website, and procurement manager from the results
def extract_contact_info(company_name, country):
    company_phone = None
    company_email = None
    company_website = None
    procurement_linkedin = None
    procurement_title = None

    # Search for Company Official Website
    query = f"{company_name} {country} official website"
    results = google_search(query, API_KEY, CX)
    if results:
        items = results.get("items", [])
        for item in items:
            link = item.get("link", "")
            if link:
                company_website = link
                break  # Stop after finding the official website

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
                # Ensure the phone number has at least 8 digits
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

    # Additional Search for Company Phone using Email (phone often appears after email)
    if company_email:
        query = f"{company_email} phone number"
        results = google_search(query, API_KEY, CX)
        if results:
            items = results.get("items", [])
            for item in items:
                snippet = item.get("snippet", "")
                # Search for phone numbers in snippets
                phone_match = re.search(r'(\+?\d{1,2}\s?-?\(?\d{1,4}\)?\s?-?\d{1,4}\s?-?\d{1,4})', snippet)
                if phone_match:
                    phone_number = phone_match.group(0)
                    # Ensure phone number is valid (at least 8 digits)
                    digits_only = re.sub(r'\D', '', phone_number)
                    if len(digits_only) >= 8:
                        company_phone = phone_number
                        break  # Stop after finding the first valid phone number

    # Search for Procurement Manager LinkedIn (company_name + country + linkedin + procurement manager)
    query = f"{company_name} {country} procurement supply manager"
    results = google_search(query, API_KEY, CX)
    if results:
        items = results.get("items", [])
        for item in items:
            link = item.get("link", "")
            if "linkedin.com" in link:
                procurement_linkedin = link
                break  # Stop after finding the first valid procurement manager
  
    return company_website, company_phone, company_email, procurement_linkedin, procurement_title

# Main function to process the CSV input and output the results
def process_companies(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write headers
        writer.writerow(['Company Name', 'Country', 'Company Website', 'Phone Number', 'Email Address', 'Procurement Manager LinkedIn', 'Procurement Manager Title'])

        for row in reader:
            company_name, country = row[0], row[1]
            
            # Fetch the company details from Google Search API
            company_website, company_phone, company_email, procurement_linkedin, procurement_title = extract_contact_info(company_name, country)
            
            # Write results to the output CSV
            writer.writerow([company_name, country, company_website, company_phone, company_email, procurement_linkedin, procurement_title])
            
            # Print progress
            print(f"Processed {company_name} ({country})")
            
            # Add a delay to avoid rate-limiting issues (respectful scraping)
            time.sleep(1)

# Run the process
input_csv = 'manufacturers.csv'  # Path to your input CSV with company names and countries
output_csv = 'output.csv'    # Path to save the results
process_companies(input_csv, output_csv)