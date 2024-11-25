from .. import mongo

def get_user_id_by_username(username):
    user = mongo.db.users.find_one({"name":username})
    return user["_id"]