
from flask import Flask

app = Flask(__name__)

from modules.reservations import *
from modules.centers import *

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
