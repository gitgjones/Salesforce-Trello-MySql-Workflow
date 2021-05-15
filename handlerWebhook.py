from flask import request, Flask, jsonify
import os
import requests
import json
import logging
import handlerTrelloAction
import traceback
# Stuff for graph testing
import plotly
import plotly.graph_objs as go
# -------

logging.basicConfig(filename="WebhookHandler.log", level=logging.INFO,format="%(asctime)s:%(levelname)s:%(message)s")

app = Flask(__name__, static_url_path='')
print("CWD: " + str(os.getcwd()))

@app.route("/", methods = ['POST','GET'])
def hello():

    #print(json.dumps(request.json,sort_keys=True,indent=4))
    
    # Server should have firewall restrictions to prevent any access from
    # sources other than Trello endpoints, but this acts as backup
    #--------------------------
    # Open config file to retrieve allowed IP sources, and set trustedIP flag
    trustedIP = False
    try:
        logging.info("Attempting to open config file")
        with open('config.json') as json_data_file:
            appConfig = json.load(json_data_file)
            logging.info("Successfully opened config file")
        for allowedIP in appConfig['auth']['trello']['allowedIPs']:
            if allowedIP['ip'] == request.remote_addr:
                trustedIP = True
    except:
        logging.warning("Unable to open config file")

    # Respond to request if trusted source, reject if not
    if trustedIP == True:
        try:
            if request.json['action']['data']['board']['id'] == "56baff72d5044cf259efa0ac": # Update this to check against the boardID listed in the config file
                # Then check what the action is and go to the appropriate script
                actionType = request.json['action']['display']['translationKey']
                # Jump to action handler script
                handlerTrelloAction.handleAction(actionType,request.json)
                # Don't forget to respond to the webhook
                return "200"
            else:
                # Handle actions that are not the Team Workload board

                # Don't forget to respond to the webhook
                return "200"
        except KeyError:
            logging.warning("Unexpected JSON structure received. Check for changes from Trello.")
            # Don't forget to respond to the webhook
            return "200"
    else:
        logging.warning("Incoming request from unauthorised source IP: " + request.remote_addr + ". Ensure firewall is configured correctly")
        # Don't do anything because it's possibly from a naughty person/bot...
        return "403"
    #--------------------------

@app.route("/dashboard", methods = ['POST','GET'])
def showDashboard():
    #return "Hi this is a dashboard"
    labels = ['Monkey','Tiger','Numpty bollox','Foo']
    values = [4500,2500,1053,500]
    trace = go.Pie(labels=labels, values=values)
    plotly.offline.plot([trace], filename='/static/test_pie_chart.html')
    try:
        return app.send_static_file('test_pie_chart.html')
    except:
        print("Problem when returning file")
        traceback.print_exc()


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=80)