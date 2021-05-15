import json
import mysql.connector
import helperMysql
import datetime
import helperTrello
import traceback
import workdays

with open('config.json') as json_data_file:
    appConfig = json.load(json_data_file)

boardListIDs = helperTrello.getListIDs(appConfig['params']['trelloBoardID'])
databaseRecords = helperMysql.getDBresults("SELECT card_id, opp_full_sfid FROM trello_actions.cards;","")

for listName in boardListIDs:
    cardIDs = helperTrello.getCardIDsInList(listName['id'])
    for card in cardIDs:
        print("Looking for card ID: " + str(card['id']))
        if any(record['card_id'] == card['id'] for record in databaseRecords):
            print("Card already in database, moving on to next card")
            continue # Card already in database
        else:
            print()
            print("Card not found, adding to database")
            cardData = helperTrello.getCardDetails(card['id'])
            #print(json.dumps(cardData,indent=4,sort_keys=True))

            # Check card meets formatting to indicate it's for an opportunity
            if cardData['name'][:8].isdigit() and len(cardData['name'][:8]) == 8:
                # Salesforce Opp ID
                cardOppID = cardData['name'][:8]
                # Salesforce Opp Name
                cardOppName = cardData['name'][11:]
                # Date card created
                cardDateCreated = helperMysql.convertDateTrelloToMysql(helperTrello.getCardCreatedDate(card['id']))
                # Name of current list
                cardListName = listName['name']
                # Check listname
                if cardListName == 'Deferred' or cardListName == 'Complete - Waiting for Win/Loss' or cardListName == 'Closed/Lost' or cardListName == 'Booked/In Delivery':
                    cardStatus = 'Complete'
                elif cardListName == 'Waiting for - Cust Feedback' or cardListName == 'Waiting for Sales - Who/What':
                    cardStatus = 'Waiting'
                else:
                    cardStatus = 'Active'
                # URL of card
                cardUrl = cardData['shortUrl']
                cardListMoves = helperTrello.getCardListMoves(card['id'])
                # Date of last list move and weeks in current list
                if len(cardListMoves) == 0:
                    cardLastListMove = ""
                    cardWeeksInList = (datetime.datetime.now() - datetime.datetime.strptime(helperTrello.getCardCreatedDate(card['id']),"%Y-%m-%dT%H:%M:%S.%fZ")).days // 7
                else:
                    cardLastListMove = helperMysql.convertDateTrelloToMysql(cardListMoves[0]['date'])
                    latestMove = datetime.datetime.strptime(cardListMoves[0]['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    dateDifference = datetime.datetime.now() - latestMove
                    cardWeeksInList = dateDifference.days // 7
                # Initiate empty variables for comment data
                cardLastCommentDate = cardDateCreated
                cardLastCommentName = ""
                cardLastCommentText = ""
                cardLastCommentDaysSince = (datetime.datetime.now() - datetime.datetime.strptime(helperTrello.getCardCreatedDate(card['id']),"%Y-%m-%dT%H:%M:%S.%fZ")).days
                # Check if any comments on card, and update with last comment details
                cardComments = helperTrello.getCardComments(card['id'])
                if len(cardComments) != 0:
                    cardLastCommentDate = helperMysql.convertDateTrelloToMysql(cardComments[0]['date'])
                    cardLastCommentName = cardComments[0]['memberCreator']['fullName']
                    cardLastCommentText = helperMysql.deEmojify(cardComments[0]['data']['text'][:1999])
                    cardLastCommentDaysSince = (datetime.datetime.now() - datetime.datetime.strptime(cardComments[0]['date'],"%Y-%m-%dT%H:%M:%S.%fZ")).days
                # Calculate Update Status
                if cardLastCommentDaysSince < 8:
                    cardUpdateStatus = 'Up to date'
                elif cardLastCommentDaysSince < 15:
                    cardUpdateStatus = 'Update due'
                elif cardLastCommentDaysSince >= 15:
                    cardUpdateStatus = 'Overdue'
                #print("Card update status = " + cardUpdateStatus)

                #print("Card ID " + cardData['id'] + " created on " + str(cardDateCreated) + " in list \'" + cardListName + "\' needs to be added to the database (" + str(cardOppID) + " - " + cardOppName + " - " + cardUrl + ")")
                
                # Add new record to database
                sql = "INSERT INTO cards (opp_sfid, card_id, card_listname, card_status, card_url, opp_name, card_date_created, card_weeks_in_current_list, card_days_since_last_comment, card_date_last_comment, card_update_status, card_last_comment, card_last_comment_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (cardOppID,cardData['id'],cardListName,cardStatus,cardUrl,cardOppName,cardDateCreated,cardWeeksInList,cardLastCommentDaysSince,cardLastCommentDate,cardUpdateStatus,cardLastCommentText,cardLastCommentName, )
                helperMysql.writeDBrecord(sql,val)

                print("opp_sfid = " + str(cardOppID))
                print("card_id = " + str(card['id']))
                print("card_listname = " + str(cardListName))
                print("card_status = " + str(cardStatus))
                print("card_url = " + str(cardUrl))
                print("opp_name = " + str(cardOppName))
                print("card_date_created = " + str(cardDateCreated))
                print("card_weeks_in_current_list = " + str(cardWeeksInList))
                print("card_days_since_last_comment = " + str(cardLastCommentDaysSince))
                print("card_date_last_comment = " + str(cardLastCommentDate))
                print("card_update_status = " + str(cardUpdateStatus))
                print("card_last_comment = " + str(cardLastCommentText))
                print("card_last_comment_by = " + str(cardLastCommentName))
                print()