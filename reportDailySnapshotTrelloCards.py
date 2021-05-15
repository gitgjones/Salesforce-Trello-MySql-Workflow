import helperMysql
import datetime


dateSnapshot = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f")

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (card_status='Active' OR card_status='Waiting');","")
totalCards = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE card_status='Active';","")
totalCardsActive = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE card_status='Waiting';","")
totalCardsWaiting = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (opp_customer_type='New Customer' AND (card_status='Active' OR card_status='Waiting'));","")
totalNewCustomer = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (opp_customer_type='Existing Customer' AND (card_status='Active' OR card_status='Waiting'));","")
totalExistingCustomer = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE DATE(card_date_created) = CURDATE();","")
totalNewCardsToday = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT CAST(AVG(card_weeks_in_current_list) AS UNSIGNED) AS 'Average' FROM trello_actions.cards WHERE card_listname='Assigned'","")
averageWeeksInAssigned = databaseData[0]['Average']

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (card_assignment_performance='Green' AND (card_status='Active' OR card_status='Waiting'));","")
totalAssignmentGreen = len(databaseData)
totalAssignmentGreenPercent = totalAssignmentGreen / totalCards

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (card_assignment_performance='Amber' AND (card_status='Active' OR card_status='Waiting'));","")
totalAssignmentAmber = len(databaseData)
totalAssignmentAmberPercent = totalAssignmentAmber / totalCards

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (card_assignment_performance='Red' AND (card_status='Active' OR card_status='Waiting'));","")
totalAssignmentRed = len(databaseData)
totalAssignmentRedPercent = totalAssignmentRed / totalCards

totalAssignmentUnassigned = totalCards - (totalAssignmentGreen + totalAssignmentAmber + totalAssignmentRed)
totalAssignmentUnassignedPercent = totalAssignmentUnassigned / totalCards

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (card_update_status='Up to date' AND (card_status='Active' OR card_status='Waiting'));","")
totalStatusUptodate = len(databaseData)
totalStatusUptodatePercent = totalStatusUptodate / totalCards

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (card_update_status='Update due' AND (card_status='Active' OR card_status='Waiting'));","")
totalStatusUpdatedue = len(databaseData)
totalStatusUpdateduePercent = totalStatusUpdatedue / totalCards

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (card_update_status='Overdue' AND (card_status='Active' OR card_status='Waiting'));","")
totalStatusOverdue = len(databaseData)
totalStatusOverduePercent = totalStatusOverdue / totalCards

totalStatusNodata = totalCards - (totalStatusUptodate + totalStatusUpdatedue + totalStatusOverdue)
totalStatusNodataPercent = totalStatusNodata / totalCards

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (opp_forecast='Omitted' AND (card_status='Active' OR card_status='Waiting'));","")
totalFunnelOmitted = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (opp_forecast='Pipeline' AND (card_status='Active' OR card_status='Waiting'));","")
totalFunnelPipeline = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (opp_forecast='Best Case' AND (card_status='Active' OR card_status='Waiting'));","")
totalFunnelBestCase = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (opp_forecast='Commit' AND (card_status='Active' OR card_status='Waiting'));","")
totalFunnelCommit = len(databaseData)

databaseData = helperMysql.getDBresults("SELECT card_id FROM trello_actions.cards WHERE (opp_forecast='Closed' AND (card_status='Active' OR card_status='Waiting'));","")
totalFunnelClosed = len(databaseData)

print("Timestamp of report = " + str(dateSnapshot))
print("Number of cards = " + str(totalCards))
print("Number of active cards = " + str(totalCardsActive))
print("Number of waiting cards = " + str(totalCardsWaiting))
print("Number of New Customer = " + str(totalNewCustomer))
print("Number of Existing Customer = " + str(totalExistingCustomer))
print("Total new cards today = " + str(totalNewCardsToday))
print("Average weeks in Assigned: " + str(averageWeeksInAssigned))
print("Total cards with assignment = green: " + str(totalAssignmentGreen))
print("Percent cards with assignment = green: " + str(totalAssignmentGreenPercent))
print("Total cards with assignment = amber: " + str(totalAssignmentAmber))
print("Percent cards with assignment = amber: " + str(totalAssignmentAmberPercent))
print("Total cards with assignment = red: " + str(totalAssignmentRed))
print("Percent cards with assignment = red: " + str(totalAssignmentRedPercent))
print("Total cards with assignment = unassigned: " + str(totalAssignmentUnassigned))
print("Percent cards with assignment = unassigned: " + str(totalAssignmentUnassignedPercent))
print("Total cards with update status = up to date: " + str(totalStatusUptodate))
print("Percent cards with update status = up to date: " + str(totalStatusUptodatePercent))
print("Total cards with update status = update due: " + str(totalStatusUpdatedue))
print("Percent cards with update status = update due: " + str(totalStatusUpdateduePercent))
print("Total cards with update status = overdue: " + str(totalStatusOverdue))
print("Percent cards with update status = overdue: " + str(totalStatusOverduePercent))
print("Total cards with update status = no data: " + str(totalStatusNodata))
print("Percent cards with update status = no data: " + str(totalStatusNodataPercent))
print("Funnel - Omitted: " + str(totalFunnelOmitted))
print("Funnel - Pipeline: " + str(totalFunnelPipeline))
print("Funnel - Best Case: " + str(totalFunnelBestCase))
print("Funnel - Commit: " + str(totalFunnelCommit))
print("Funnel - Closed: " + str(totalFunnelClosed))


sql = ("INSERT INTO daily_snapshot (date_snapshot,total_cards,total_cards_active,total_cards_waiting,total_cards_newcustomer,total_cards_existingcustomer,total_cards_newtoday,avg_weeks_in_assigned,cards_assignment_green,cards_assignment_green_percent,cards_assignment_amber,cards_assignment_amber_percent,cards_assignment_red,cards_assignment_red_percent,cards_update_uptodate,cards_update_uptodate_percent,cards_update_updatedue,cards_update_updatedue_percent,cards_update_overdue,cards_update_overdue_percent,funnel_omitted,funnel_pipeline,funnel_bestcase,funnel_commit,funnel_closed,cards_assignment_unassigned,cards_assignment_unassigned_percent,cards_update_nodata,cards_update_nodata_percent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
val = (dateSnapshot,totalCards,totalCardsActive,totalCardsWaiting,totalNewCustomer,totalExistingCustomer,totalNewCardsToday,averageWeeksInAssigned,totalAssignmentGreen,totalAssignmentGreenPercent,totalAssignmentAmber,totalAssignmentAmberPercent,totalAssignmentRed,totalAssignmentRedPercent,totalStatusUptodate,totalStatusUptodatePercent,totalStatusUpdatedue,totalStatusUpdateduePercent,totalStatusOverdue,totalStatusOverduePercent,totalFunnelOmitted,totalFunnelPipeline,totalFunnelBestCase,totalFunnelCommit,totalFunnelClosed,totalAssignmentUnassigned,totalAssignmentUnassignedPercent,totalStatusNodata,totalStatusNodataPercent,)
helperMysql.writeDBrecord(sql,val)