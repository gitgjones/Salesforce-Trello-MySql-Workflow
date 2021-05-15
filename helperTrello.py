import requests
import json
import time
import traceback
import datetime

# Need to figure out abstraction of creds
#-----------------
with open('config.json') as json_data_file:
    appConfig = json.load(json_data_file)
keyTxt = "key=" + appConfig['auth']['trello']['key']
tokenTxt = "&token=" + appConfig['auth']['trello']['token']
#-----------------

def trelloCallAPI (callMethod, callString):
    if not callMethod or not callString: return "Arguments missing"
    if callMethod == "GET":
        returnResponse = callTypeGet(callString)
    elif callMethod == "POST":
        #requestResponse = callTypePost(callString)
        pass
    else: returnResponse =  "Invalid call method"
    try:
        return json.loads(returnResponse.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return returnResponse
    except:
        print("Error in function: trelloCallAPI")
        traceback.print_exc()

def callTypeGet (callString):
    fullURL = "https://api.trello.com/" + callString + keyTxt + tokenTxt

    for attemptCount in range(1,5):
        try:
            response = requests.get(fullURL)
            if response.status_code != 200:
                print ("Attempt number " + str(attemptCount) + " failed. (Response code " + str(response.status_code) + " received)\n Reattempting API call...\n")
                print("Waiting " + str(5**attemptCount) + " seconds before next attempt.\n\n")
                time.sleep(5**attemptCount)
            else:
                return response.content
        except requests.exceptions.ConnectionError:
            print ("Couldn't make a connection")
            print("Waiting " + str(5**attemptCount) + " seconds before next attempt.\n\n")
            time.sleep(5**attemptCount)
    return response.status_code

def putCustomFieldDetails (cardID,customFieldId,customFieldPayload):
    url = 'https://api.trello.com/1/card/' + cardID + '/customField/' + customFieldId + '/item?' + keyTxt + tokenTxt
    print("Trying to update custom field details: " + url + " with Payload: " + str(customFieldPayload))
    payload = json.dumps(customFieldPayload)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    for attemptCount in range(1,5):
        try:
            response = requests.put(url, data=payload, headers=headers)
            if response.status_code != 200:
                print ("Attempt number " + str(attemptCount) + " failed. (Response code " + str(response.status_code) + " received). Reattempting API call...\nWaiting " + str(5**attemptCount) + " seconds before next attempt.\n")
                time.sleep(5**attemptCount)
            else:
                print("Successfully updated CardID " + cardID + " with payload: " + str(customFieldPayload))
                return
        except requests.exceptions.ConnectionError:
            print ("Couldn't make a connection\n")
            print("Waiting " + str(5**attemptCount) + " seconds before next attempt.\n\n")
            time.sleep(5**attemptCount)

def putCommentOnCard(cardID,comment):
    url = 'https://api.trello.com/1/cards/' + cardID + '/actions/comments?text=' + comment + "&" + keyTxt + tokenTxt
    for attemptCount in range(1,5):
        try:
            response = requests.post(url)
            if response.status_code != 200:
                print ("Attempt number " + str(attemptCount) + " failed. (Response code " + str(response.status_code) + " received). Reattempting API call...\nWaiting " + str(5**attemptCount) + " seconds before next attempt.\n")
                time.sleep(5**attemptCount)
            else:
                print("Successfully updated CardID " + cardID)
                return
        except requests.exceptions.ConnectionError:
            print ("Couldn't make a connection\n")
            print("Waiting " + str(5**attemptCount) + " seconds before next attempt.\n\n")
            time.sleep(5**attemptCount)
    
def moveCardToList(cardID,listID):
    url = 'https://api.trello.com/1/cards/' + cardID + '?idList=' + listID + "&" + keyTxt + tokenTxt
    for attemptCount in range(1,5):
        try:
            response = requests.put(url)
            if response.status_code != 200:
                print ("Attempt number " + str(attemptCount) + " failed. (Response code " + str(response.status_code) + " received)\n Reattempting API call...\n")
                print("Waiting " + str(5**attemptCount) + " seconds before next attempt.\n\n")
                time.sleep(5**attemptCount)
            else:
                print("Successfully updated CardID " + cardID)
                return
        except requests.exceptions.ConnectionError:
            print ("Couldn't make a connection\n")
            print("Waiting " + str(5**attemptCount) + " seconds before next attempt.\n\n")
            time.sleep(5**attemptCount)

def getListIDs (trelloBoardID):
    apicallTxt = "1/boards/" + trelloBoardID + "/lists?fields=id,name&"
    json_data = trelloCallAPI("GET",apicallTxt)
    return json_data

def getCardIDsInList (trelloListID):
    apicallTxt = "1/lists/" + trelloListID + "?cards=open&card_fields=id&"
    json_data = trelloCallAPI("GET",apicallTxt)
    if json_data == "API call failed":
        return json_data
    else:
        json_data = json_data['cards']
        return json_data

def getCustomFieldConfig (trelloBoardID):
    print("getCustomFieldConfig")

def getCardUpdateStatus (cardID):
    print("getCardUpdateStatus")

def getCardDetails (cardID):
    print("Retrieving JSON for card ID " + str(cardID))
    apicallTxt = "1/cards/" + cardID + "?fields=all&customFieldItems=true&"
    json_data = trelloCallAPI("GET",apicallTxt)
    return json_data

def getCardListMoves (cardID):
    apicallTxt = "1/cards/" + cardID + "/actions?filter=updateCard:idList&"
    json_data = trelloCallAPI("GET", apicallTxt)
    json_data.sort(key=lambda x: x['date'],reverse=True)
    return json_data

def getCardListMovesOldestFirst (cardID):
    apicallTxt = "1/cards/" + cardID + "/actions?filter=updateCard:idList&"
    json_data = trelloCallAPI("GET", apicallTxt)
    json_data.sort(key=lambda x: x['date'],reverse=False)
    return json_data

def getCardComments (cardID):
    apicallTxt = "1/cards/" + cardID + "/actions?filter=commentCard&"
    json_data = trelloCallAPI("GET", apicallTxt)
    json_data.sort(key=lambda x: x['date'],reverse=True)
    return json_data

def getCardCreatedDate (cardID):
    apicallTxt = "1/cards/" + cardID + "/actions?filter=createCard,copyCard&"
    json_data = trelloCallAPI("GET", apicallTxt)
    createdDate = json_data[0]['date']
    return createdDate

def getCardCustomFieldValues(cardID):
    apicallTxt = "1/cards/" + cardID + "/customFieldItems?"
    json_data = trelloCallAPI("GET", apicallTxt)
    return json_data

def getCustomFieldListValue(customFieldID,customFieldValueID):
    apicallTxt = "1/customField/" + customFieldID + "/options/" + customFieldValueID + "?"
    json_data = trelloCallAPI("GET", apicallTxt)
    customFieldValue = json_data['value']['text']
    return customFieldValue

def getAllCardActions (cardID):
    apicallTxt = "1/cards/" + cardID + "/actions?filter=all&"
    json_data = trelloCallAPI("GET", apicallTxt)
    json_data.sort(key=lambda x: x['date'],reverse=True)
    return json_data

def getSecondsSinceLastAction(cardID):
    allActions = getAllCardActions(cardID)
    differenceInSeconds = (datetime.datetime.now() - datetime.datetime.strptime(allActions[0]['date'][:-1], "%Y-%m-%dT%H:%M:%S.%f")).total_seconds()
    return differenceInSeconds