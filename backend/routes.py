from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == id:
            return picture
    return {"message": "picture not found"}, 404
    



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    if picture['id'] in [pic['id'] for pic in data]:
        return {"Message": f"picture with id {picture['id']} already present"}, 302
    else:
        try:
            data.append(picture)
            return picture, 201
        except NameError:
            return {"Message": "data not defined"}, 500

    
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.json
    if picture['id'] not in [pic['id'] for pic in data]:
        return {"Message": f"picture not found"}, 404
    else:
        try:
            for idx, existing_picture in enumerate(data):
                if existing_picture['id'] == picture['id']:
                    data[idx] = picture
        except NameError:
            return {"Message": "data not defined"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return {"message": f"{id}"}, 204
    return {"message": "picture not found"}, 404