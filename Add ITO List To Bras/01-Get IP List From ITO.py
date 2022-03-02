import requests
import json
import sys
#///////////////////////////////////////
#Load From ITO
url = "https://Eservices.ito.gov.ir/api/g2b/GetIpList"
payload={}
headers = {
  'Authorization': 'Basic XXXXXX'#user and pass are in base64 format 
}
response = requests.request("POST", url, headers=headers, data=payload)
#///////////////////////////////////////
#Write Response To Json File
with open("g2b.json", "w") as file:
    file.write(response.text)
# Read JSON data from file
with open("g2b.json", "r") as read_file:
    # Convert JSON file to Python Dictionary
    obj = json.load(read_file)
    # Now We have Python Dictionary
    # Pretty print JSON data
    pretty_json = json.dumps(obj, indent=4)
# Write Pretty To File
with open("g2b.pretty.json", "w") as prettyhandler:
    prettyhandler.write(pretty_json)
