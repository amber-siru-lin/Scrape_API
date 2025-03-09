import requests
import csv
import time

# Your Google API Key and Custom Search Engine ID (CX)
CX = '6058d2d2b16294e2b'  # Replace with your Custom Search Engine ID
KG_API_KEY = 'AIzaSyC-YalX1ATLhbGPvcPLEhE5NThy9UHwo7Q'  # Replace with your Knowledge Graph API key


import requests
import csv
import time

# Your Google API Key for Knowledge Graph API
API_KEY = 'YOUR_API_KEY'  # Replace with your API key

# Function to query Google Knowledge Graph API
def knowledge_graph_search(query, api_key):
    search_url = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        'query': query,
        'key': api_key,
        'limit': 1,  # Limit to 1 result per query
        'languages': 'en'
    }
    
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to extract website and phone number from the Knowledge Graph result
def extract_info(company_name, country):
    website = None
    phone_number = None

    # Search for Company Information using Knowledge Graph API
    query = f"{company_name} {country}"
    result = knowledge_graph_search(query, API_KEY)
    
    if result and 'itemListElement' in result:
        elements = result['itemListElement']
        for element in elements:
            # Extract website
            if 'result' in element and 'url' in element['result']:
                website = element['result']['url']
            
            # Extract phone number (if available in the Knowledge Graph result)
            if 'result' in element and 'detailedDescription' in element['result']:
                description = element['result']['detailedDescription']
                if 'phoneNumber' in description:
                    phone_number = description['phoneNumber']
                
    return website, phone_number

# Main function to process the CSV input and output the results
def process_companies(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write headers
        writer.writerow(['Company Name', 'Country', 'Website', 'Phone Number'])

        for row in reader:
            company_name, country = row[0], row[1]
            
            # Fetch the company info from Knowledge Graph API
            website, phone_number = extract_info(company_name, country)
            
            # Write results to the output CSV
            writer.writerow([company_name, country, website, phone_number])
            
            # Print progress
            print(f"Processed {company_name} ({country})")
            
            # Add a delay to avoid rate-limiting issues (respectful scraping)
            time.sleep(1)

# Run the process
input_csv = 'companies.csv'  # Path to your input CSV with company names and countries
output_csv = 'output.csv'    # Path to save the results
process_companies(input_csv, output_csv)