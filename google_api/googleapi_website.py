import requests
import csv
import time

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

# Function to extract company website
def extract_website(company_name, country):
    company_website = None

    # Search for Company Official Website
    query = f"{company_name} {country} official website"
    results = google_search(query, API_KEY, CX)
    if results:
        items = results.get("items", [])
        for item in items:
            link = item.get("link", "")
            company_website = link
            break  # Stop after finding the first valid website

    return company_website

# Main function to process the CSV input and output the results
def process_companies(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header for the new CSV
        writer.writerow(['Company Name', 'Country', 'Website Link'])

        for row in reader:
            company_name, country = row[0], row[1]
            
            # Fetch the company website from Google Search API
            company_website = extract_website(company_name, country)
            
            # Write the company name, country, and website link to the output CSV
            writer.writerow([company_name, country, company_website])
            
            # Print progress
            print(f"Processed {company_name} ({country})")
            
            # Add a delay to avoid rate-limiting issues (respectful scraping)
            time.sleep(1)

# Run the process
input_csv = 'manufacturers.csv'  # Path to your input CSV with company names and countries
output_csv = 'websites.csv'   # Path to save the results with website links
process_companies(input_csv, output_csv)