from datetime import datetime

from pymongo import ReturnDocument

from .. import mongo

def create_seed():
    return mongo.db.settings.find_one_and_update({"_id": "seed"}, {"$inc": {"value": 1}},
                                                 upsert=True, return_document=ReturnDocument.AFTER)['value']

class Link:
    def __init__(self,user_id,long_url):
        self._id = create_seed()
        self.user_id = user_id
        self.long_url = long_url
        self.created_at = datetime.utcnow()
        self.last_used = self.created_at
    def to_dict(self):
        return {
            "_id":self._id,
            "user_id": self.user_id,
            "long_url": self.long_url,
            "created_at": self.created_at,
            "last_used": self.last_used
        }

def create_link(user_id = None, long_url = None):
    # obj = {"user_id": user_id,
    #     "long_url": long_url,
    #     "created_at": link.created_at,
    #     "last_used": link.last_used}
    # # mongo.db.links.insert_one(obj)
    # return obj
    if not mongo.db.links.find_one({"long_url": long_url,"user_id":user_id}):
        link = Link(user_id, long_url)
        mongo.db.links.insert_one(link.to_dict())
    # return link.to_dict().get("_id")
    return mongo.db.links.find_one({"long_url": long_url})['_id']

def update_last_usage(link_id):
    mongo.db.links.update_one({"_id" : link_id}, {"$set" : {"last_used" : datetime.utcnow()}})
    return

def get_orginal_link_by_id(link_id):
    update_last_usage(int(link_id))
    link = mongo.db.links.find_one({'_id':int(link_id)})['long_url']
    # print(link['long_url'])
    return link

