from simple_salesforce import Salesforce
import requests
import json
import csv
import time

with open('config.json') as json_data_file:
    appConfig = json.load(json_data_file)

# Must pass the report ID and all 3 credentials
def getSalesforceReport(reportID):
    sf = Salesforce(username=appConfig['auth']['salesforce']['username']
                    ,password=appConfig['auth']['salesforce']['password']
                    ,security_token=appConfig['auth']['salesforce']['token'])
    sid = sf.session_id
    for attemptCount in range(1,5):
        print("Attempt number",str(attemptCount),"to retrieve Salesforce report")
        try:
            response = requests.get("https://ctl.my.salesforce.com/" + reportID + "?isdtp=p1&export=1&enc=UTF-8&xf=csv",
                            headers = sf.headers, cookies = {'sid' : sid})
            if response.status_code != 200:
                print ("Salesforce Report retrieval attempt number " + str(attemptCount) + " failed. (Response code " + str(response.status_code) + " received)\n Reattempting API call...\n")
                print ("Waiting " + str(5**attemptCount) + " seconds before next attempt.\n")
                time.sleep(5**attemptCount)
            else:
                f = open('csvfile.csv','wb')
                f.write(response.content) 
                f.close()
                build_json = '['
                with open('csvfile.csv') as csvfile:
                    reader = csv.DictReader(csvfile)
                    i = 1
                    for row in reader:
                        build_json = build_json + json.dumps(row) + ","
                        i += 1
                    jsonLoaded = json.loads(str(build_json)[:-1] + ']')
                    #--- Attempt to pull OppID - if JSON correct will return, if not will throw exception
                    try:
                        tempStr = jsonLoaded[0]['OppID']
                        print("Salesforce report " + reportID + " retrieved. " + str(i-6) + " record(s)")
                        return jsonLoaded
                    except TypeError:
                        print ("Malformed salesforce report returned... will retry...\n")
        except KeyError:
            print ("Possible Salesforce report timeout... will retry...\n")
            print("Waiting " + str(5**attemptCount) + " seconds before next attempt.\n\n")
            time.sleep(5**attemptCount)
    return ("\n*** CRITICAL ERROR *** Unable to retrieve Salesforce report\n\n")