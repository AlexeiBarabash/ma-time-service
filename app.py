from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def server_local_time():
    localtime = datetime.now()
    return "<p>Time on the Server: </p>" + localtime.strftime("%H:%M:%S")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)