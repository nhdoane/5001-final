"""
Was originally intended to be a true backend using flask but that got sidelined
just a relic, wont get tested and will probably be deleted by the end if i remember
"""
from flask import Flask
import time

app = Flask(__name__)

@app.route('/day')
def test():
    return {'time': time.strftime('%a %d-%b-%Y', time.gmtime())}

if __name__ == '__main__':
    app.run()