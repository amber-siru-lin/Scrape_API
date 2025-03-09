''' <script async src="https://cse.google.com/cse.js?cx=6058d2d2b16294e2b">
</script>
<div class="gcse-search"></div> '''

'''AIzaSyB8yLc6OweAQs3dSV90qPgQp1UibQD4vOY'''


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

# Function to extract relevant information from the search results
def extract_info(company_name, country):
    website = None
    company_number = None
    procurement_contact = None

    # Search for Official Website (focuses on avoiding news results)
    query = f"{company_name} {country} official site"
    results = google_search(query, API_KEY, CX)
    if results:
        items = results.get("items", [])
        for item in items:
            link = item.get("link", "")
            # Check if the link looks like an official company website
            if not website and "http" in link and "news" not in link:
                website = link

    # Search for Company Phone Number (using the Knowledge Panel context)
    query = f"{company_name} {country} phone number"
    results = google_search(query, API_KEY, CX)
    if results:
        items = results.get("items", [])
        for item in items:
            snippet = item.get("snippet", "")
            # Look for phone numbers by checking for numeric patterns (e.g., +123 or 123-456)
            if not company_number:
                possible_number = ''.join([c for c in snippet if c.isdigit() or c == '+'])
                if possible_number and len(possible_number) > 6:  # reasonable length for phone numbers
                    company_number = possible_number

    # Search for Procurement Contact (LinkedIn)
    query = f"{company_name} {country} procurement contact site:linkedin.com"
    results = google_search(query, API_KEY, CX)
    if results:
        items = results.get("items", [])
        for item in items:
            link = item.get("link", "")
            if "linkedin" in link.lower():
                procurement_contact = link

    return website, company_number, procurement_contact

# Main function to process the CSV input and output the results
def process_companies(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write headers
        writer.writerow(['Company Name', 'Country', 'Website', 'Company Number', 'Procurement Contact'])

        for row in reader:
            company_name, country = row[0], row[1]
            
            # Fetch the company info from Google Search API
            website, company_number, procurement_contact = extract_info(company_name, country)
            
            # Write results to the output CSV
            writer.writerow([company_name, country, website, company_number, procurement_contact])
            
            # Print progress
            print(f"Processed {company_name} ({country})")
            
            # Add a delay to avoid rate-limiting issues (respectful scraping)
            time.sleep(1)

# Run the process
input_csv = 'companies.csv'  # Path to your input CSV with company names and countries
output_csv = 'output.csv'    # Path to save the results
process_companies(input_csv, output_csv)