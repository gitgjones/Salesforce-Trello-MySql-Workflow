import helperMysql, helperTrello
import json

with open('config.json') as json_data_file:
    appConfig = json.load(json_data_file)

boardListIDs = helperTrello.getListIDs(appConfig['params']['trelloBoardID'])
databaseRecords = helperMysql.getDBresults("SELECT card_id, opp_full_sfid FROM trello_actions.cards;","")

for listName in boardListIDs:
    cardIDs = helperTrello.getCardIDsInList(listName['id'])
    for card in cardIDs:
        print("Looking for card ID: " + str(card['id']))
        if any(record['card_id'] == card['id'] for record in databaseRecords):
            cardData = helperTrello.getCardCustomFieldValues(card['id'])
            sql = "SELECT * FROM trello_actions.cards WHERE card_id=%s;"
            val = (card['id'],)
            databaseData = helperMysql.getDBresults(sql,val)[0]
            print(json.dumps(databaseData,indent=4,sort_keys=True))
            for configCustomField in appConfig['customFields']:
                foundField = False
                if configCustomField['fieldDataSource'] != "trello":
                    if databaseData[configCustomField['fieldnameDatabase']] == None:
                        databaseDataValue = ''
                    else:
                        databaseDataValue = databaseData[configCustomField['fieldnameDatabase']]
                    # Check if values in card are different to DB and update if needed...
                    for cardCustomField in cardData:
                        if cardCustomField['idCustomField'] == configCustomField['id']:
                            print("I found the field!")
                            foundField = True
                            if databaseDataValue == '':
                                payload = {'value': ''}
                                helperTrello.putCustomFieldDetails(card['id'],configCustomField['id'],payload)
                            else:
                                if configCustomField['type'] == "text":
                                    if cardCustomField['value']['text'] != databaseDataValue:
                                        payload = {'value':{'text': databaseDataValue}}
                                        helperTrello.putCustomFieldDetails(card['id'],configCustomField['id'],payload)
                                elif configCustomField['type'] == "number":
                                    if cardCustomField['value']['number'] != databaseDataValue:
                                        payload = {'value':{'number': str(databaseDataValue)}}
                                        helperTrello.putCustomFieldDetails(card['id'],configCustomField['id'],payload)
                                elif configCustomField['type'] == "list":
                                    for configCustomFieldOption in configCustomField['listOptions']:
                                        print(json.dumps(configCustomFieldOption,indent=4,sort_keys=True))
                                        print("Database value = " + str(databaseDataValue))
                                        print("Custom Field option = " + str(configCustomFieldOption['listOptionValue']))
                                        if databaseDataValue == configCustomFieldOption['listOptionValue']:
                                            print("MATCH")
                                            payload = {'idValue': configCustomFieldOption['listOptionID']}
                                            helperTrello.putCustomFieldDetails(card['id'],configCustomField['id'],payload)
                                        else:
                                            print("NO MATCH")
                                else:
                                    print("Field type not currently handled")
                                
                    # If field isn't populated...
                    if foundField == False:
                        print("I didn't find the field...")
                        if configCustomField['type'] == "text":
                            payload = {'value':{'text': databaseDataValue}}
                            helperTrello.putCustomFieldDetails(card['id'],configCustomField['id'],payload)
                        elif configCustomField['type'] == "number":
                            print("Field name: "+ configCustomField['fieldnameDatabase'])
                            print("DB Value: " + str(databaseDataValue))
                            if databaseDataValue == '':
                                print("Empty database value")
                                payload = {'value': ''}
                                helperTrello.putCustomFieldDetails(card['id'],configCustomField['id'],payload)    
                            else:
                                payload = {'value':{'number': str(databaseDataValue)}}
                                helperTrello.putCustomFieldDetails(card['id'],configCustomField['id'],payload)
                        elif configCustomField['type'] == "list":
                            for configCustomFieldOption in configCustomField['listOptions']:
                                print(json.dumps(configCustomFieldOption,indent=4,sort_keys=True))
                                print("Database value = " + str(databaseDataValue))
                                print("Custom Field option = " + str(configCustomFieldOption['listOptionValue']))
                                if databaseDataValue == configCustomFieldOption['listOptionValue']:
                                    print("MATCH")
                                    payload = {'idValue': configCustomFieldOption['listOptionID']}
                                    helperTrello.putCustomFieldDetails(card['id'],configCustomField['id'],payload)
                                else:
                                    print("NO MATCH")
                        else:
                            print("Field type not currently handled")