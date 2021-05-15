import helperSalesforce, helperMysql, helperTrello
import json

def findRecordPosition(listToSearch,keyToFind,valueToFind):
    for i, item in enumerate(listToSearch):
        if item[keyToFind] == valueToFind:
            return i
    return -1

with open('config.json') as json_data_file:
    appConfig = json.load(json_data_file)

salesforceData = helperSalesforce.getSalesforceReport(appConfig['params']['salesforceReportID'])
print(json.dumps(salesforceData,indent=4, sort_keys=True))

sql = "SELECT opp_full_sfid, card_id FROM trello_actions.cards;"
val = ''
databaseData = helperMysql.getDBresults(sql,val)
if len(databaseData) == 0:
    print("No records in database")
else:
    for databaseRecord in databaseData:
        if databaseRecord['opp_full_sfid'] == None:
            pass
        else:
            rowPosition = findRecordPosition(salesforceData,'Record ID (18)',databaseRecord['opp_full_sfid'])
            if rowPosition == -1:
                print("Opportunity not found in salesforce data")
            else:
                print("Found opp " + databaseRecord['opp_full_sfid'] + ". Comparing salesforce and database values...")
                sql = "SELECT * FROM trello_actions.cards WHERE card_id=%s;"
                val = (databaseRecord['card_id'],)
                databaseRecordData = helperMysql.getDBresults(sql,val)
                if len(databaseRecordData) == 0:
                    pass
                else:
                    print(json.dumps(salesforceData[rowPosition],indent=4,sort_keys=True))
                    print(json.dumps(databaseRecordData[0],indent=4,sort_keys=True))
                    for customField in appConfig['customFields']:
                        if customField['fieldDataSource'] == "salesforce":
                            
                            salesforceValue = salesforceData[rowPosition][customField['fieldnameSalesforce']]
                            databaseValue = databaseRecordData[0][customField['fieldnameDatabase']]
                            print("    Salesforce value : " + str(salesforceValue))
                            print("    Database value   : " + str(databaseValue))
                            if salesforceValue != databaseValue:
                                print("I need to update the value in the database!")
                                sql = "UPDATE trello_actions.cards SET %s=%%s WHERE card_id=%%s;" %(customField['fieldnameDatabase'])
                                val = (salesforceValue, databaseRecord['card_id'], )
                                helperMysql.writeDBrecord(sql,val)
                            pass

