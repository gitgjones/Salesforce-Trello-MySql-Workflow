import helperMysql, helperTrello
import json
import datetime

#if listDetail['listName'] == jsonData['action']['data']['listAfter']['name']:
#                    cardStatus = listDetail['listStatus']


#cardLastCommentDate = helperMysql.convertDateTrelloToMysql(cardComments[0]['date'])
#cardLastCommentDaysSince = (datetime.datetime.now() - datetime.datetime.strptime(cardComments[0]['date'],"%Y-%m-%dT%H:%M:%S.%fZ")).days

# Loop through all cards in the database that are not deleted
databaseData = helperMysql.getDBresults("SELECT card_id, card_date_created FROM trello_actions.cards WHERE NOT card_status='Deleted';","")

for databaseRecord in databaseData:
    # For each card, pull the list of list moves
    print("\n\nList moves for Card ID: " + str(databaseRecord['card_id']) + "\n\n")
    listMoves = helperTrello.getCardListMovesOldestFirst(databaseRecord['card_id'])
    numberOfMoves = len(listMoves)
    print("Number of list moves: " + str(numberOfMoves))
    #print(json.dumps(listMoves,indent=4, sort_keys=True))
    #if numberOfMoves > 0:

    # Check each list move for the first instance of 'Complete'
    for i, item in enumerate(listMoves):
        # Build list move data
        listAfterMoveName = item['data']['listAfter']['name']
        listAfterMoveId = item['data']['listAfter']['id']
        listBeforeMoveName = item['data']['listBefore']['name']
        listBeforeMoveId = item['data']['listBefore']['id']
        moveNumber = i + 1
        moveDate = item['date']
        moveDateConverted = helperMysql.convertDateTrelloToMysql(moveDate)
        moveDateConvertedDatetime = datetime.datetime.strptime(moveDateConverted, "%Y-%m-%d %H:%M:%S.%f")
        dateCardCreatedDatetime = datetime.datetime.strptime(databaseRecord['card_date_created'], "%Y-%m-%dT%H:%M:%S.%f")
        listMoveFromCreated = (moveDateConvertedDatetime - dateCardCreatedDatetime).days
        moveUser = item['memberCreator']['fullName']


        # Calculate time in list

        print("List Move #: " + str(moveNumber) + "\nList Before: " + listBeforeMoveName + "\nList After: " + listAfterMoveName + "\nMove Date: " + str(moveDate) + "\nUser: " + moveUser + "\nDays between list move and created: " + str(listMoveFromCreated))

    #    if item[i]    

        

            # Set the 'Complete' date
            # Set the number of days in Presales (difference between database create date and complete date)
