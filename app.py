import sys
import json
from flask import Flask, request, send_from_directory, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

app_downloads = [] # stores the app download information (to be moved to a database)

@app.route('/<path:path>', methods=['GET'])
def getStaticFile(path):
    return send_from_directory('resources', path)

@app.route('/', methods=['GET'])
def getIndexFile():
    return send_from_directory('resources', 'index.vulcanized.html')

@app.route('/index.html', methods=['GET'])
def getVulcanizedIndexFile():
    return send_from_directory('resources', 'index.vulcanized.html')

# receive new app download data
@app.route('/service/adddownloads', methods=['POST'])
def addDownloads():
    data = request.json
    app_downloads.extend(data)
    socketio.emit('message', data)
    return "", 201

# return all app downloads
@app.route('/service/getdownloads', methods=['GET'])
def getDownloads():
    return jsonify(app_downloads)

# testdata generation
countries = ["Spain", "Italy", "Germany", "Switzerland", "Australia", "Japan", "Singapore", "US", "Argentina", "Chile", "Colombia"]
appids = ["IOS_ALERT", "IOS_MATE", "ANDROID_ALERT", "ANDROID_MATE"]
def generateTestdata():
    ret = {}
    ret["country"] = countries[randint(0, len(countries) - 1)]
    ret["app_id"] = appids[randint(0, len(appids) - 1)]
    d = datetime.today() - timedelta(seconds=randint(0, 60*60*24*3*356)) # three years back until now
    ret["downloaded_at"] = d.isoformat(' ')
    ret["longitude"] = -180.0 + randint(0, 360000)/1000.0
    ret["latitude"] = -85.0 + randint(0, 170000)/1000.0
    return ret
     

if __name__ == '__main__':
    usage = """either provide no arguments to start the server or specify 'add-testdata' followed by an integer to add the amount of new testdata to the running server, e.g.:
python app.py
python app.py add-testdata 2
"""
    if len(sys.argv) == 3:
        amount = 0
        hasParsedAmount = False
        try: 
            amount = int(sys.argv[2])
            hasParsedAmount = True
        except ValueError:
            hasParsedAmount = False
        
        if sys.argv[1] == 'add-testdata' and hasParsedAmount:
            import urllib2
            from random import randint
            from datetime import datetime, timedelta
            
            data = []
            for i in range(0, amount):
                data.append(generateTestdata())
            
            req = urllib2.Request('http://localhost:5000/service/adddownloads')
            req.add_header('Content-Type', 'application/json')

            response = urllib2.urlopen(req, json.dumps(data))
            print response
        else:
            print usage
    elif len(sys.argv) == 1:
        socketio.run(app)
    else:
        print usage
