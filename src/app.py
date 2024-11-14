"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is not None:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 400

@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.json
    required_fields = ["id", "first_name", "age", "lucky_numbers"]
    for field in required_fields:
        if field not in request_body or request_body[field] in [None, "", []]:
            return jsonify({"error": f"'{field}' field is required and cannot be empty"}), 400
    jackson_family.add_member(request_body)
    return jsonify("User created successfully"), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    jackson_family.delete_member(member_id)
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"message": "Member deleted successfully", "done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 400



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)