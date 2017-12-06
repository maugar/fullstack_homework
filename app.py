from flask import Flask, request, send_from_directory
app = Flask(__name__)

@app.route('/<path:path>', methods=['GET'])
def getStaticFile(path):
    return send_from_directory('resources', path)

@app.route('/', methods=['GET'])
def getIndexFile():
    return send_from_directory('resources', 'index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
