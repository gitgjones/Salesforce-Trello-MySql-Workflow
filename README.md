# Trello-Salesforce-MySql-Workflow

## Description
Workflow automation using Salesforce (via Zapier) as the resource request trigger, Trello as the daily workload management tool, Mysql backend for data collection, fronted with PowerBI for reporting.

This is something I created to improve a few things at work for a specific use case, the Trello tool is a great kanban based UI but I wanted control over reporting, and the ability to use various power ups in a more automated way to help reduce time spent on admin, and improve workload visibility. This tooling also meant zero manual workload reporting: the data was available and updated automatically in PowerBI.

## Dataflow

**For new requests** - Zapier is used to poll Salesforce every 5 minutes for new 'Salesforce Tasks' with a specific configuration - Zapier creates a card on Trello with some pertinent Salesforce object IDs, and the Zap then builds the card with information from those Salesforce Objects. Trello sends a webhook which is picked up by a python script, and the initial card creation information is added to the Mysql database.

**For card updates** - Trello webhooks are incredibly useful, the information is very detailed and there's plenty of scope for using the data in interesting ways (my use for this project is very basic) - as soon as a user does something to one of their cards, Trello fires a webhook which is picked up by a python script, and based on the action type the database (or Trello) will be updated.

![image](https://user-images.githubusercontent.com/84078914/118370837-7ad3e000-b5a1-11eb-935d-ea165bab4719.png)

**Daily reconcile/report tasks** - Using chron, a number of scripts run daily:

  1. Salesforce reconcile: This uses a csv report from Salesforce keep the database up to date with accurate opportunity data.
  2. Trello reconcile: This keeps Trello up to date with the latest Salesforce info via the database.
  3. Win/Loss reconcile: If a user doesn't move their card to the correct list, this script will automatically move the card, keeping reports accurate.
  4. Daily snapshot: Takes a snapshot of workload each day and stores in another database table, planning to use this for data trending.
  5. Daily update status: Checks when each card was last updated, and changes custom fields on each card to prompt users to update them.

## Architecture

<img width="919" alt="Workflow architecture" src="https://user-images.githubusercontent.com/84078914/118371749-e1f39380-b5a5-11eb-9c2e-dbdfccf45eb2.png">

## Status

**I am not actively working on this project anymore.** There were a number of items I wanted to implement to improve general usefulness and to develop new skills but never managed to get that far down the list:

  1. I wanted to use this project to travel the path of converting to a containerised solution, followed by full serverless conversion.
  2. Incorporate some autohealing for webhooks with trello, and also the service running on my webhook server.
  3. Implement proper logging and alerting.
  4. Create a UI to allow:
      - Updating credentials
      - Configuration of reports
      - Simple addition of new fields
      - Field configuration
  5. Robust authentication (rather than using creds in a config file)

If you've made it this far, thanks for reading, and I hope there may be something useful in here for you!

-Gareth
