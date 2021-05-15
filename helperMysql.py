import json
import mysql.connector
import datetime
import traceback

def connectToDB():
    with open('config.json') as json_data_file:
        appConfig = json.load(json_data_file)
    try:
        mydb = mysql.connector.connect(
            host=appConfig['auth']['database']['host'],
            user=appConfig['auth']['database']['user'],
            passwd=appConfig['auth']['database']['password'],
            database=appConfig['auth']['database']['database']
        )
        return mydb
    except Exception as e:
        print("Error in function: connectToDB\nError Text: " + e)

def getDBresults(sql,val):
    # Returns JSON object of rows returned from SELECT statement
    try:
        dbConnection = connectToDB()
        dbCursor = dbConnection.cursor()
        dbCursor.execute(sql,val)
        print(dbCursor.statement)
        result = dbCursor.fetchall()
        fieldNames = [i[0] for i in dbCursor.description]
        dbConnection.close
    except Exception as e:
        print("Error in function: getDBresults-callDB\nError Text: " + e)
    jsonResult = []
    try:
        for item in result:
            jsonResult.append(dict(zip(fieldNames,item)))
        # Run jsonResult object through converter to standardise datetime format
        jsonResult = json.dumps(jsonResult,default=jsonConverter)
        # Convert back to a list
        jsonResult = json.loads(jsonResult)
        return jsonResult
    except Exception as e:
        print("Error in function: getDBresults-convertJSON\nError Text: " + e)
    return jsonResult

def writeDBrecord(sql,val):
    # Write data to DB
    try:
        dbConnection = connectToDB()
        dbCursor = dbConnection.cursor()
        try:
            dbCursor.execute(sql,val)
            print(dbCursor.statement)
        except:
            print("Error in function: writeDBrecord-execute")
            traceback.print_exc()
        try:
            dbConnection.commit()
        except:
            print("Error in function: writeDBrecord-commit")
        dbConnection.close
    except Exception as e:
        print("Error in function: writeDBrecord \nError Text: " + e)
    return

def convertDateTrelloToMysql(datestr):
    datestr = datestr.replace("T"," ").replace("Z","")
    return datestr

def convertDateMysqlToTrello(datestr):
    pass

def jsonConverter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def getDBresultsBasic(sql,val):
    # Returns JSON object of rows returned from SELECT statement
    try:
        dbConnection = connectToDB()
        dbCursor = dbConnection.cursor()
        dbCursor.execute(sql,val)
        print(dbCursor.statement)
        result = dbCursor.fetchall()
        dbConnection.close
        return result
    except Exception as e:
        print("Error in function: getDBresults-callDB\nError Text: " + e)