'''API Key: 5b30188b6eb8cc340f45e3a9ba0ffe9f6184d9996521b7b27830358a8fdae467'''

import requests
import pandas as pd
import time

# Replace this with your actual SerpAPI key
SERPAPI_KEY = "5b30188b6eb8cc340f45e3a9ba0ffe9f6184d9996521b7b27830358a8fdae467"

def get_website(company_name, country):
    """Search Google for the official website of a manufacturer."""
    query = f"{company_name} {country} official site"
    url = f"https://serpapi.com/search.json?engine=google&q={query}&api_key={SERPAPI_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        for result in data.get("organic_results", []):
            if "www" in result.get("link", ""):
                return result["link"]  # Return the first website found
    except Exception as e:
        print(f"Error fetching website for {company_name}: {e}")
    
    return None




def find_procurement_contact(company_name, country):
    """Search Google for procurement contacts (LinkedIn or supplier pages)."""
    query = f'{company_name} {country} procurement OR sourcing OR supplier site:linkedin.com OR site:manufacturer.com'
    url = f"https://serpapi.com/search.json?engine=google&q={query}&api_key={SERPAPI_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        contacts = []
        for result in data.get("organic_results", []):
            contacts.append(result["link"])  # Save relevant links

        return "; ".join(contacts) if contacts else None
    except Exception as e:
        print(f"Error fetching procurement contact for {company_name}: {e}")
    
    return None



def get_company_phone_number(company_name, country):
    """Extract the company's phone number from Google's right-side panel."""
    query = f"{company_name} {country} contact number"
    url = f"https://serpapi.com/search.json?engine=google&q={query}&api_key={SERPAPI_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        # Look in the Knowledge Graph data
        if "knowledge_graph" in data:
            phone_numbers = data["knowledge_graph"].get("phone_numbers", [])
            return "; ".join(phone_numbers) if phone_numbers else None
    except Exception as e:
        print(f"Error fetching phone number for {company_name}: {e}")
    
    return None



# Load the CSV file
input_file = "manufacturers.csv"  # Change this to your file name
output_file = "manufacturers_with_contacts.csv"

df = pd.read_csv(input_file)




# Add new columns
df["Website"] = df.apply(lambda x: get_website(x["Manufacture Name"], x["Country"]), axis=1)
df["Procurement Contacts"] = df.apply(lambda x: find_procurement_contact(x["Manufacture Name"], x["Country"]), axis=1)
df["Company Phone"] = df.apply(lambda x: get_company_phone_number(x["Manufacture Name"], x["Country"]), axis=1)


# Save the updated CSV file
df.to_csv(output_file, index=False)

print(f"Updated CSV saved as {output_file}")
