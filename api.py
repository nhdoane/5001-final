# supposed to provide a route to the backend from RN but that got put on hold
from flask import Flask
import time

app = Flask(__name__)

@app.route('/day')
def test():
    return {'time': time.strftime('%a %d-%b-%Y', time.gmtime())}

if __name__ == '__main__':
    app.run()