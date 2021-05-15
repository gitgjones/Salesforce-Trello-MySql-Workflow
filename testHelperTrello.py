import helperTrello
import json

with open('config.json') as json_data_file:
    appConfig = json.load(json_data_file)

listIDs = helperTrello.getListIDs(appConfig['params']['trelloBoardID'])
print("List IDs:\n" + json.dumps(listIDs,indent=4,sort_keys=True))

cardsInList = helperTrello.getCardIDsInList("5be997c8584ca087d25695e3")
print("Cards in List:\n" + json.dumps(cardsInList,indent=4, sort_keys=True))

cardDetails = helperTrello.getCardDetails("5c5449b4706fc6263707eb49")
print("Card Details:\n" + json.dumps(cardDetails,indent=4, sort_keys=True))

cardListMoves = helperTrello.getCardListMoves("5c5449b4706fc6263707eb49")
print("Card List Moves:\n" + json.dumps(cardListMoves,indent=4, sort_keys=True))

cardCreatedDate = helperTrello.getCardCreatedDate("5c5449b4706fc6263707eb49")
print("Card Created Date: " + cardCreatedDate)

customFieldValue = helperTrello.getCustomFieldListValue("5b3c86e399babaff86885e64","5b3c86f2f5e68df9d9eb2904")
print("Custom Field Value: " + str(customFieldValue))

cardActions = helperTrello.getAllCardActions("5c5449b4706fc6263707eb49")
print("Card Actions:\n" + json.dumps(cardActions,indent=4, sort_keys=True))

secondsSinceLastAction = helperTrello.getSecondsSinceLastAction("5c5449b4706fc6263707eb49")
print("Seconds since last action: " + str(secondsSinceLastAction))