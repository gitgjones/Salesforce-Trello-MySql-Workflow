import helperMysql
import datetime

sql = "SELECT * FROM trello_actions.cards WHERE (card_status='Active' OR card_status='Waiting');"
val = ''
databaseData = helperMysql.getDBresults(sql,val)
if len(databaseData) == 0:
    print("No records in database")
else:
    for databaseRecord in databaseData:

        # Calculate weeks in current list (calc from date created if empty)
        cardWeeksInList = 0
        if databaseRecord['card_date_last_list_move'] == None:
            cardWeeksInList = (datetime.datetime.now() - datetime.datetime.strptime(databaseRecord['card_date_created'][:10], "%Y-%m-%d")).days // 7
        else:
            cardWeeksInList = (datetime.datetime.now() - datetime.datetime.strptime(databaseRecord['card_date_last_list_move'][:10], "%Y-%m-%d")).days // 7

        # Calculate days since comment (calc from date created if empty)
        cardDaysSinceComment = 0
        if databaseRecord['card_date_last_comment'] == None:
            cardDaysSinceComment = (datetime.datetime.now() - datetime.datetime.strptime(databaseRecord['card_date_created'][:10],"%Y-%m-%d")).days
        else:
            cardDaysSinceComment = (datetime.datetime.now() - datetime.datetime.strptime(databaseRecord['card_date_last_comment'][:10],"%Y-%m-%d")).days

        # Calculate Update Status
        cardUpdateStatus = ''
        if cardDaysSinceComment < 8:
            cardUpdateStatus = 'Up to date'
        elif cardDaysSinceComment < 15:
            cardUpdateStatus = 'Update due'
        elif cardDaysSinceComment >= 15:
            cardUpdateStatus = 'Overdue'

        # Write updated values to DB
        sql = ("UPDATE trello_actions.cards SET card_days_since_last_comment=%s, card_weeks_in_current_list=%s, card_update_status=%s WHERE card_id=%s")
        val = (cardDaysSinceComment,cardWeeksInList,cardUpdateStatus,databaseRecord['card_id'], )
        helperMysql.writeDBrecord(sql,val)

        
