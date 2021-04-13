# unc_health_price_scraper


I decided to write a Python script to scrape data from the UNC Rex price estimator. The API endpoint I discovered is at https://portalapprev.com/ptapp/api/cdm/data?_dc=1617216721840&recno=8d086f6527295fbb6f6d253f3b5548b85ef9fcad8319564656464e552fff3d1e. Hitting this endpoint returns the following:
```

import requests

endpoint='https://portalapprev.com/ptapp/.......'

def get_endpoint():
  result = requests.get(endpoint)
  if result.status_code == 200:
    print(result)

>>> {"total":3282,"data":[{"Facility Name":"Rex Hospital","Charge Description":"Cardiac valve and other major cardiothoracic procedures with cardiac catheterization with major complications or comorbidities ","CPT/HCPCS":"MS-DRG: 216","Price":"$197,625.03","Min":"$21,760.00","Max":"$149,680.06","Aetna":"$89,699.54","Aetna HMO":"$89,699.54","Aetna Medicare Advantage":"$68,043.14","BCBS":"$149,680.06","Blue Home":"$114,628.71","Blue Home UNC Health Alliance":"$77,495.80","Cash Discount":"$118,575.02","Cigna":"$84,347.33","Cigna Connect Network":"$71,523.81","Cigna SureFit":"$71,523.81","First Carolina Care":"$140,111.84","Galaxy":"$133,106.27","Health Payors":"$119,095.07","Humana":"$133,106.27","Humana Alignment Medicare Advanatge":"$21,760.00","Humana Medicare Advantage":"$68,975.87","Liberty Medicare Advantage":"$68,975.87","MedCost":"$116,867.91","MedCost Ultra":"$92,473.82","OneNet":"$86,869.34","TriCare":"$0.00","United Healthcare":"$140,111.84","United Healthcare Compass":"$140,111.84","United Healthcare Medicare Advantage":"$67,505.83","WellCare Medicare Advantage":"$67,005.13"}]}
```

`"total"` refers to the total number of procedures listed. I also discovered that by appending a `page` parameter to the endpoint, I could iterate over all 3282 procedures and write the response data to a JSON file:

```
import requests
n=3282
endpoint='https://portalapprev.com/ptapp......'

// GET the endpoint with the parameter 'start'=n
def get_api(page):
    tries = 0
    result = {}
    // Try the request up to 5 times
    while tries < 5:
        data=requests.get(endpoint + str(page))
        // If everything looks good, break from the loop.
        if data.status_code ==  200:
            result=data.json()
            break
        // Otherwise, print the failure and try again.
        print("Failed to GET.")
        tries += 1
        print("Retrying...")
    // Return the result dict
    return result
```

Then it was just a matter of looping over the pages and writing the result to a JSON file. Please excuse the hackiness. I'm not getting paid for this.

```
import requests
import json

output_file="prices.json"
n=3282
endpoint="https://..."

def get_api(page):
// ...
// Previous code
// ...

// Append new results to the JSON output file
def write_result(result):
    with open(file, 'a') as output:
        json.dump(result, output)

// Check if the total number of procedures changed
def update_total(new_total):
  if new_total !== n:
    n = new_total


def main():
    print("Starting calls...")
    // Nope, definitely no hacky code here
    write_result("[")
    // Iterate through all pages/procedures
    for page in range(n):
        // Hit that endpoint
        result = get_api(page)
        print("Writing prices for procedure:" + " " + result[0]['Charge Description'])
        // Write out the data dict to the JSON file.
        write_result(result["data"][0])
        // Hey it works, okay. Sort of. You have to find/replace all in the output JSON.
        write_result(",")
        update_total(result["total"])
    // ... I'm so embarassed by this.
    write_result("]")
    print("Done")
        

if __name__ == '__main__':
    main()
```

Once [I had all the data in hand](https://williamkrakow.dev/projects/scraping-pricing-data-from-a-bad-hospital-website), I had to clean it.

In my experience, cleaning datasets is to be expected. Any set of thousands of records from a large organization such as a hospital is bound to have its quirks and outliers. However, despite its relatively dimunitive size - 3-5k hospital procedures, depending on the insurer - this set was unusually bad. Fortunately I was able to standardize the price data with the find and replace regex tool in VSCODE.

For the backend, I built a NodeJS API with routes for insurers and procedures. I hooked this up to a MongoDB Atlas cloud database and used the standard Mongo client SDK. I've used Mongoose in the past and appreciate its polyfills and server side schemas, but for this project it would likely be overkill. I'm running the server on a Free tier Heroku Dyno, so I wanted to minimize my dependencies.

For the front end, I bootstrapped the project with create-react-app, and wrote some custom hooks to fetch data from the API. Fetch requests from the React app were proxied through the server port.

Initially I ran into trouble with the database structure. I was using the payers as the top-level document, but discovered that Mongo doesn't have a great way to query strings within documents within arrays. If there is a method, let me know. I spent a good few hours reading through dry database documentation and came up with nil.

Anyways, feel free to browse the source code and the MVP. I've only gotten through 3 of the payer datasets so far, but plan to finish cleaning the rest of the sets and uploading them to the database in the near future.
