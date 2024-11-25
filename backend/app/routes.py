from datetime import datetime
from functools import wraps
import base64

from flask import request, jsonify, Response, redirect

from . import app, mongo
from . import models


def require_oauth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.authorization:
            auth = request.authorization
            username = auth.username
            password = auth.password
            # print(username)
            if(username=="user2" and password == "111"):
                return f(*args, **kwargs)
        return Response(
            response ='{"status": "Unauthorized"}',
            status  = 401,
            headers = {"WWW-Authenticate": f'Basic realm="Login Required"'},
            mimetype = "application/json",
        )
    return decorated


@app.route("/short", methods=["GET", "POST"])
@require_oauth
def short():
    try:
        data = request.get_json()
        # print(data)
        long_link = data.get('url')
        if long_link:
            user_id = models.users.get_user_id_by_username(request.authorization.username)
            short_url = models.links.create_link(user_id, long_link)
            return jsonify({'short_url': f'http://localhost:5000/{short_url}',
                            'dfdf': str(base64.encodebytes(bytes([0x47, 0xa5, 0x7, 0x20])))})
        else:
            return jsonify({"Error": "long_link is required"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route("/<link_id>", methods=["GET"])
#@require_oauth()
def redirect_to_url(link_id):
    try:
        link_to = models.links.get_orginal_link_by_id(link_id)
        return redirect(link_to)
    except Exception as e:
        return jsonify({'Error': 'Link not found'},404)

# @app.route('/ping', methods=['GET'])
# def ping_pong():
#     return jsonify('pong!')
@app.route('/hello', methods=['POST'])
def ping_pong_post():
    data = request.get_json()
    long_link = data.get('url')
    print(request.authorization.username)
    return jsonify({'msg': "pong!!"})

# @app.route("/test", methods=[ "POST"])
# @require_oauth
# def startpost():
#     try:
#         data = request.get_json()
#         print(data.get('long_url'))
#         print(models.users.get_user_id_by_username(request.authorization.username))
#         return "Hello"
#     except Exception as e:
#         return jsonify({"error":str(e)})








#
# @app.route("/", methods=["GET", "POST"])
# def start():
#     # print(mongo.db.users.find_one({"_id":"user2@topomatic.local"}))
#     # mongo.db.users.find_one({"_id":"user2@topomatic.local"})
#     user = mongo.db.users.find_one({"name":"user2"})
#     print(user)
#     print(user["_id"])
#     # mongo.db.users.insert_one({"_id":"testuser@topomatic.local"})
#     return ("Hello")