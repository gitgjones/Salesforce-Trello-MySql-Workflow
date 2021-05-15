import json
import mysql.connector
import helperMysql
import datetime
import helperTrello
import traceback
import workdays

def handleAction(actionType, jsonData):
    print(json.dumps(jsonData,indent=4,sort_keys=True))
    # Ascertain action type and jump to relevant function
    if actionType == "action_create_card" or actionType == "action_copy_card":
        # Check if card ID exists in the Database - definitely shouldn't as all cards unique...
        print ("Checking if card " + jsonData['action']['data']['card']['name']+ " ("+ jsonData['action']['data']['card']['id'] + ") exists")
        sql = "SELECT * FROM trello_actions.cards where (card_id=%s);"
        val = (jsonData['action']['data']['card']['id'],)
        result = helperMysql.getDBresults(sql,val)
        if len(result)>0:
            print("CardID already in database... this definitely shouldn't happen...")
            return
        else:
            print ("Create Card")
            val_card_date_created = helperMysql.convertDateTrelloToMysql(jsonData['action']['date'])
            val_card_id = jsonData['action']['data']['card']['id']
            val_card_listname = jsonData['action']['data']['list']['name']
            val_card_status = "Active"
            val_card_url = "https://trello.com/c/" + jsonData['action']['data']['card']['shortLink']
            if len(jsonData['action']['data']['card']['name']) == 18:
                val_opp_full_sfid = jsonData['action']['data']['card']['name']
            else:
                val_opp_full_sfid = None
            val_opp_name = jsonData['action']['data']['card']['name']
            val_opp_id = 0
            if jsonData['action']['data']['card']['name'][:8].isdigit() and len(jsonData['action']['data']['card']['name'][:8]) == 8:
                val_opp_id = jsonData['action']['data']['card']['name'][:8]
                val_opp_name = jsonData['action']['data']['card']['name'][11:]
            val_card_days_since_last_comment = 0
            val_card_date_last_comment = val_card_date_created
            val_card_update_status = "Up to date"
            sql = "INSERT INTO cards (opp_sfid, card_id, card_listname, card_status, card_url, opp_name, card_date_created, card_weeks_in_current_list, card_days_since_last_comment, card_date_last_comment, card_update_status, opp_full_sfid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (val_opp_id, val_card_id, val_card_listname, val_card_status, val_card_url, val_opp_name, val_card_date_created,0,val_card_days_since_last_comment,val_card_date_last_comment,val_card_update_status, val_opp_full_sfid, )
            helperMysql.writeDBrecord(sql,val)
            addLastAction(jsonData)
            print("Create card - complete")            
            return
        
    if actionType == "action_archived_card":
        try:
            print ("Archive Card")
            sql = "UPDATE trello_actions.cards SET card_status = 'Archived' WHERE card_id=%s;"
            val = (jsonData['action']['data']['card']['id'], )
            helperMysql.writeDBrecord(sql,val)
            addLastAction(jsonData)
            print ("Archive Card - complete")
        except Exception as e:
            print("Error while attempting: Archive\nError Text: " + e)
        return

    if actionType == "action_delete_card":
        try:
            print ("Delete Card")
            sql = "UPDATE trello_actions.cards SET card_status = 'Deleted' WHERE card_id=%s;"
            val = (jsonData['action']['data']['card']['id'], )
            helperMysql.writeDBrecord(sql,val)
            addLastAction(jsonData)
            print ("Delete Card - complete")
        except Exception as e:
            print("Error while attempting: Delete\nError Text: " + e)
        return

    if actionType == "action_comment_on_card":
        try:
            print ("Comment on card")
            commentDateCreatedForDB = helperMysql.convertDateTrelloToMysql(jsonData['action']['date'])
            commentTextForDB = jsonData['action']['data']['text'][:1999]
            sql = "UPDATE trello_actions.cards SET card_last_comment=%s, card_last_comment_by=%s, card_days_since_last_comment=%s, card_date_last_comment=%s, card_update_status=%s WHERE card_id=%s;"
            val = (commentTextForDB,jsonData['action']['display']['entities']['memberCreator']['text'],0,commentDateCreatedForDB,"Up to date",jsonData['action']['data']['card']['id'], )
            helperMysql.writeDBrecord(sql,val)
            # Make a call to set the Update Status custom field to "Up to date"
            payload = {'idValue': '5b62c28bc3a6c15527b011cb'}
            helperTrello.putCustomFieldDetails(jsonData['action']['data']['card']['id'],"5b62c28bc3a6c15527b011c8",payload)
            addLastAction(jsonData)
            print ("Comment on card - complete")
        except Exception as e:
            print("Error while attempting: Card comment\nError Text: " + e)
        return

    if actionType == "action_renamed_card":
        oppIDfromCard = jsonData['action']['data']['card']['name'][:8]
        oppNamefromCard = jsonData['action']['data']['card']['name'][11:]
        if len(oppNamefromCard)==0:
            oppNamefromCard = "Opp name missing - refer to Salesforce"
        if not oppIDfromCard.isdigit() or len(oppIDfromCard)<8:
            print("Not a salesforce ID - ignoring card rename action")
            return
        else:
            try:
                print ("Card Rename")
                sql = "UPDATE trello_actions.cards SET opp_sfid=%s, opp_name=%s WHERE card_id=%s;"
                val = (oppIDfromCard,oppNamefromCard,jsonData['action']['data']['card']['id'], )
                helperMysql.writeDBrecord(sql,val)
                addLastAction(jsonData)
                print ("Card Rename - complete")
            except Exception as e:
                print("Error while attempting: Rename card\nError Text: " + e)
            return

    if actionType == "action_sent_card_to_board":
        try:
            print ("Restore Card")
            sql = "UPDATE trello_actions.cards SET card_status = 'Active' WHERE card_id=%s;"
            val = (jsonData['action']['data']['card']['id'], )
            helperMysql.writeDBrecord(sql,val)
            addLastAction(jsonData)
            print ("Restore Card - complete")
        except Exception as e:
            print("Error while attempting: Restore\nError Text: " + e)
        return

    if actionType == "action_move_card_from_list_to_list":
        try:
            print ("Card List Move")
            cardStatus = ''
            with open('config.json') as json_data_file:
                appConfig = json.load(json_data_file)
            for listDetail in appConfig['listConfig']:
                if listDetail['listName'] == jsonData['action']['data']['listAfter']['name']:
                    cardStatus = listDetail['listStatus']
            
            card_date_last_list_move = helperMysql.convertDateTrelloToMysql(jsonData['action']['date'])
            sql = "UPDATE trello_actions.cards SET card_listname=%s, card_weeks_in_current_list=%s, card_date_last_list_move=%s, card_status=%s WHERE card_id=%s;"
            val = (jsonData['action']['data']['listAfter']['name'],0,card_date_last_list_move, cardStatus, jsonData['action']['data']['card']['id'], )
            helperMysql.writeDBrecord(sql,val)
            addLastAction(jsonData)
            print ("Card List Move - complete")
            


        except Exception as e:
            print("Error while attempting: Move List\nError Text: " + e)
        return
    
    if actionType == "action_update_custom_field_item":
        try:
            print ("Card update custom field: " + jsonData['action']['data']['customField']['name'])
            customFieldType = jsonData['action']['data']['customField']['type']
            customFieldID = jsonData['action']['data']['customField']['id']
            customFieldNewValue = ""
            try:
                if customFieldType == "text":
                    customFieldNewValue = jsonData['action']['data']['customFieldItem']['value']['text']
                elif customFieldType == "number":
                    customFieldNewValue = jsonData['action']['data']['customFieldItem']['value']['number']
                elif customFieldType == "list":
                    customFieldNewValue = helperTrello.getCustomFieldListValue(customFieldID,jsonData['action']['data']['customFieldItem']['idValue'])
            except TypeError:
                customFieldNewValue = None

            # Find customFieldID in config.json
            #--- Pull in config file as JSON object -----
            with open('config.json') as json_data_file:
                appConfig = json.load(json_data_file)
            for configCustomFieldEntry in appConfig['customFields']:
                if configCustomFieldEntry['id'] == customFieldID:
                    print("Found the field in config file")
                    if configCustomFieldEntry['fieldDataSource'] != "trello":
                        # Check if this field was updated by Gareth's account ** NEED BETTER SOLUTION **
                        # Get the database value for the field
                        sql = "SELECT %s FROM trello_actions.cards WHERE card_id=%%s;" %(configCustomFieldEntry['fieldnameDatabase'])
                        val = (jsonData['action']['data']['card']['id'],)
                        result = helperMysql.getDBresults(sql,val)
                        databaseValue = result[0][configCustomFieldEntry['fieldnameDatabase']]
                        if databaseValue == None and customFieldNewValue == None:
                            return
                        if databaseValue == None and customFieldNewValue != None:
                            payload = {'value': ''}
                            helperTrello.putCustomFieldDetails(jsonData['action']['data']['card']['id'],customFieldID,payload)
                            return
                        print("Database Value is: " + str(databaseValue) + " New Trello Value is: " + str(customFieldNewValue))
                        if configCustomFieldEntry['type'] == "text":
                            if databaseValue != customFieldNewValue:
                                print("Send old text value back")
                                payload = {'value': {'text': databaseValue}}
                                helperTrello.putCustomFieldDetails(jsonData['action']['data']['card']['id'],customFieldID,payload)
                                return
                        elif configCustomFieldEntry['type'] == "number":
                            if (customFieldNewValue == None) or (float(databaseValue) != float(customFieldNewValue)):
                                print("Send old number value back")
                                payload = {'value': {'number': str(databaseValue)}}
                                helperTrello.putCustomFieldDetails(jsonData['action']['data']['card']['id'],customFieldID,payload)
                                return
                        elif configCustomFieldEntry['type'] == "list":
                            if databaseValue != customFieldNewValue:
                                print("Send old dropdown value back")
                                # Need to search the config file for the customfieldvalueID that matches the text value
                                for option in configCustomFieldEntry['listOptions']:
                                    if option['listOptionValue'] == databaseValue:
                                        payload = {'idValue': option['listOptionID']}
                                        helperTrello.putCustomFieldDetails(jsonData['action']['data']['card']['id'],customFieldID,payload)
                                        return
                    else:
                        print("Trello is allowed to change this field!!")
                        sql = "SELECT %s FROM trello_actions.cards WHERE card_id=%%s;" %(configCustomFieldEntry['fieldnameDatabase'])
                        val = (jsonData['action']['data']['card']['id'],)
                        result = helperMysql.getDBresults(sql,val)
                        databaseValue = result[0][configCustomFieldEntry['fieldnameDatabase']]
                        print("Database value is: " + str(databaseValue))
                        if customFieldType == "text":
                            customFieldNewValue = jsonData['action']['data']['customFieldItem']['value']['text']
                        elif customFieldType == "number":
                            customFieldNewValue = jsonData['action']['data']['customFieldItem']['value']['number']
                        elif customFieldType == "list":
                            if customFieldNewValue == None:
                                customFieldNewValue = ''
                            else:
                                customFieldNewValue = helperTrello.getCustomFieldListValue(customFieldID,jsonData['action']['data']['customFieldItem']['idValue'])
                        sql = "UPDATE trello_actions.cards SET %s=%%s WHERE card_id=%%s;" %(configCustomFieldEntry['fieldnameDatabase'])
                        val = (customFieldNewValue, jsonData['action']['data']['card']['id'], )
                        helperMysql.writeDBrecord(sql,val)

                        # Check if this is the owner field and if it is the 1st time set:
                        if databaseValue == None and jsonData['action']['data']['customField']['name'] == "Owner":
                            sql = "SELECT card_date_created FROM trello_actions.cards WHERE card_id=%s;"
                            val = (jsonData['action']['data']['card']['id'],)
                            result = helperMysql.getDBresults(sql,val)
                            dateCardCreated = datetime.datetime.strptime(result[0]['card_date_created'][:10], "%Y-%m-%d")
                            dateCardAssigned = datetime.datetime.strptime(jsonData['action']['date'][:10], "%Y-%m-%d")
                            workingDaysDifference = (workdays.networkdays(dateCardCreated,dateCardAssigned)) - 1
                            assignmentPerformance = ""
                            if workingDaysDifference <= 1:
                                assignmentPerformance = "Green"
                            elif workingDaysDifference > 1 and workingDaysDifference <= 5:
                                assignmentPerformance = "Amber"
                            elif workingDaysDifference > 5:
                                assignmentPerformance = "Red"
                            sql = ("UPDATE trello_actions.cards SET card_date_assigned=%s, card_days_to_assign=%s, card_assignment_performance=%s WHERE card_id=%s")
                            val = (helperMysql.convertDateTrelloToMysql(jsonData['action']['date']),workingDaysDifference,assignmentPerformance,jsonData['action']['data']['card']['id'],)
                            helperMysql.writeDBrecord(sql,val)
                        return
        except Exception as e:
            print("Error while attempting: Update Custom Field\nError Text: " + str(e))
        return

def addLastAction(jsonData):
    try:
        jsonDataForDB = json.dumps(jsonData,indent=4,sort_keys=True,default=helperMysql.jsonConverter)
        sql = "UPDATE trello_actions.cards SET card_last_action_json=%s WHERE card_id=%s;"
        val = (jsonDataForDB, jsonData['action']['data']['card']['id'], )
        helperMysql.writeDBrecord(sql,val)
    except Exception as e:
        print("Error in Function: addLastAction\nError Text: " + e)
    return
