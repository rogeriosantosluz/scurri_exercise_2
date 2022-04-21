from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
from .. import app
from ..modules.postcodes import *

validators = [verify_alphanumeric, verify_length, verify_space, verify_outward_code]

def validations(postcode, response_dict):
    for validator in validators:
        response = validator(postcode)
        if "error" in response:
            response_dict["error"] = {"validator": validator.__name__, "error": response["error"]}
            break
        else:
            response_dict["data"]["validations"].append({validator.__name__: response})
    
@app.route("/postcodes/<postcode>", methods=["GET"])
def postcodes(postcode):
    app.logger.info(f"Postcode: {postcode}")
    response_dict = {"data": {"postcode": postcode, "validations": []}}
    validations(postcode, response_dict)
    if "error" in response_dict:
        return jsonify(response_dict), 400
    return jsonify(response_dict), 200

@app.route("/verify_postcode", methods=["GET"])
def verify_postcode():
    if "postcode" not in request.args:
        return jsonify({"postcode not passed"}), 400
    postcode = request.args["postcode"]
    app.logger.info(f"Postcode: {postcode}")
    response_dict = {"data": {"postcode": postcode, "validations": []}}
    validations(postcode, response_dict)
    if "error" in response_dict:
        return jsonify(response_dict), 400
    return jsonify(response_dict), 200