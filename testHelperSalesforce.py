import helperSalesforce
import json

salesforceReport = helperSalesforce.getSalesforceReport("00O1Y0000074rn2")
print(json.dumps(salesforceReport,indent=4, sort_keys=True))