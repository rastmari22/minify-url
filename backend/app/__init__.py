# import CORS
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from app import config

cfg = config.Configuration()

app = Flask(__name__)
app.config.from_object(cfg)
tlsCAFile = app.config['MONGO_CA']
if tlsCAFile == '':
    tlsCAFile = None
mongo = PyMongo(app, tlsCAFile=tlsCAFile)
mongo.db = mongo.cx[app.config['MONGO_DB']]
link = mongo.db.links.find_one({'_id':19})['long_url']
print(link)
CORS(app,allow_headers={"Authorization", "Content-type"})
# cors = CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}},
#             allow_headers={"Authorization", "Content-type"})


from . import routes, config
