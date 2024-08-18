import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import math

# Define your filters
filters = [
    'company_name in "Chesapeake Energy Corp.", "Exxon Mobil Corp.", "Shell plc", '
    '"BP plc", "Chevron Corp.", "TotalEnergies SE", "ConocoPhillips", '
    '"Occidental Petroleum Co.", "EOG Resources, Inc.", "Devon Energy Corp.", '
    '"Diamondback Energy Inc.", "Ovintiv Inc. (f.k.a EnCana Corp.)", '
    '"APA Corporation (f.k.a Apache Corp.)", "Marathon Oil Corp.", '
    '"Permian Resources Corp. (f.k.a Centennial Resources)", "Coterra Energy (f.k.a. Cabot Oil)"',
    'region in "Corporate Financial & Operational Data", "Global Operational Data (Consol. Only)", '
    '"U.S. (Consolidated only)"',
    'time > "2024 Q1 Actual"'
]

# ye username or password hai
username = '8a7d4d8b-59d9-4206-9510-3152f0265246'
password = 'vnS2GBNtLPRYMYZ4'

# Call the count API and calculate the total number of pages
params = {"filter": filters}
r = requests.get(
    "https://api.connect.ihsmarkit.com/energy/v2/company-metrics/count/cell-data-names",
    auth=HTTPBasicAuth(username, password),
    params=params
)
r.raise_for_status()
k = r.json()

# Calculate the number of pages
total_pages = math.ceil(k / 1000)
print(f"Total number of pages: {total_pages}")

# Initialize an empty DataFrame to store the data
df = pd.DataFrame()

# ye all pages ka data scrape kray ga
for current_page in range(1, total_pages + 1):
    params = {
        "pageIndex": current_page,
        "filter": filters
    }
    url = "https://api.connect.ihsmarkit.com/energy/v3/company-metrics/retrieve/cell-data-names"
    r = requests.get(url, auth=HTTPBasicAuth(username, password), params=params, verify=True)
    r.raise_for_status()
    j = r.json()

    # Print the progress
    print(f"{current_page}/{total_pages} : page/all_pages")

    # Normalize JSON data and append to the DataFrame
    new_df = pd.json_normalize(data=j)
    df = pd.concat([df, new_df], ignore_index=True)



# Save the final DataFrame to a CSV file (overwrite)
df.to_csv('ihsmarkit.csv', index=False)


