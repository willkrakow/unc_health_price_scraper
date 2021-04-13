import requests
import json
n=3
endpoint="https://portalapprev.com/ptapp/api/cdm/data?_dc=1617316077839&recno=8d086f6527295fbb6f6d253f3b5548b85ef9fcad8319564656464e552fff3d1e&start="
file="prices.json"

def get_api(page):
    tries = 0
    result = {}
    while tries < 5:
        data=requests.get(endpoint + str(page))
        if data.status_code ==  200:
            result=data.json()
            break
        print("Failed to GET.")
        tries += 1
        print("Retrying...")
    return result["data"]

def write_result(result):
    with open(file, 'a') as output:
        json.dump(result, output)

def main():
    print("Starting calls...")
    write_result("[")
    for page in range(n):
        result = get_api(page)
        print("Writing prices for procedure:" + " " + result[0]['Charge Description'])
        print(result)
        write_result(result[0])
        write_result(",")
    write_result("]")
    print("Done")
        

if __name__ == '__main__':
    main()
    