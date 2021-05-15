import helperMysql, helperTrello, json

sql = "SELECT * FROM trello_actions.cards;"
val = ''
databaseData = helperMysql.getDBresults(sql,val)
if len(databaseData) == 0:
    print("No records in database")
else:
    for databaseRecord in databaseData:
        if databaseRecord['opp_stage'] == 'Lost' and databaseRecord['card_listname'] != 'Closed/Lost':
            print("Opportunity is lost and is in wrong list - needs to move")
            helperTrello.moveCardToList(databaseRecord['card_id'],'58667a501d00714795c89694')
            helperTrello.putCommentOnCard(databaseRecord['card_id'],"Automated list move - Moving to lost due to Salesforce status")
        if databaseRecord['opp_stage'] == 'Won' and databaseRecord['card_listname'] != 'Booked/In Delivery':
            print("Opportunity is won and is in wrong list - needs to move")
            helperTrello.moveCardToList(databaseRecord['card_id'],'586679d5b2eaf381dd5dfdfa')
            helperTrello.putCommentOnCard(databaseRecord['card_id'],"Automated list move - Moving to won due to Salesforce status")