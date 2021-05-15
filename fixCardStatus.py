import helperMysql, helperTrello, json

with open('config.json') as json_data_file:
    appConfig = json.load(json_data_file)

sql = "SELECT * FROM trello_actions.cards;"
val = ''
databaseData = helperMysql.getDBresults(sql,val)
if len(databaseData) == 0:
    print("No records in database")
else:
    for databaseRecord in databaseData:
        for listDetail in appConfig['listConfig']:
            if listDetail['listName'] == databaseRecord['card_listname']:
                cardStatus = listDetail['listStatus']
                if cardStatus == databaseRecord['card_status']:
                    pass
                else:
                    print("Card status is " + databaseRecord['card_status'] + " but should be " + cardStatus)
                    sql = "UPDATE trello_actions.cards SET card_status=%s WHERE card_id=%s;"
                    val = (cardStatus, databaseRecord['card_id'], )
                    helperMysql.writeDBrecord(sql,val)