from flask import Flask, render_template, request, redirect, flash, url_for, session, jsonify
from .. import app
from ..modules.postcodes import *

validators = [verify_format,
              verify_alphanumeric, 
              verify_length, 
              verify_space, 
              verify_outward_code, 
              verify_postcode_area_and_district,
              verify_inward_code, 
              verify_postcode_sector_and_unit, 
              verify_areas_single_digit_district,
              verify_areas_double_digit_district,
              verify_areas_with_a_district_zero,
              verify_areas_single_digit_district_extra_letter,
              verify_first_position,
              verify_second_position,
              verify_third_position,
              verify_fourth_position,
              verify_unit]

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

@app.route("/verify_postcode", methods=["GET", "POST"])
def verify_postcode():
    if "postcode" not in request.args:
        return jsonify({"error": "postcode not passed"}), 400
    postcode = request.args["postcode"]
    app.logger.info(f"Postcode: {postcode}")
    response_dict = {"data": {"postcode": postcode, "validations": []}}
    validations(postcode, response_dict)
    if "error" in response_dict:
        return jsonify(response_dict), 400
    return jsonify(response_dict), 200