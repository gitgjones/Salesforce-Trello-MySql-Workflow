import helperMysql
import json

def testGetRecord(cardID):
    sql = "SELECT * FROM trello_actions.cards WHERE card_id=%s;"
    val = (cardID,)
    result = helperMysql.getDBresults(sql,val)
    print(json.dumps(result,indent=4,sort_keys=True))
    return

cardID = input("Enter Card ID:\n")
testGetRecord(cardID)