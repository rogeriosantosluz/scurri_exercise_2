from flask import Flask
import json
import pytest
from ..modules.postcodes import *
import os

from .. import app

simple_postcode = "BB10 2AL"
invalid_postcode = "BLA"
valid_outward_code = "BLA XPTO"
invalid_outward_code = "B XPTO"
valid_inward_code = "BLA XPT"
invalid_inward_code = "B X"
invalid_sector = "BB1 BBD"
invalid_unit = "BB1 999"
invalid_postcode_many_spaces = "BB1  1BD"
invalid_alphanumeric_postcode = "BLA%"
postcode_examples = ["SW1W 0NY", "PO16 7GZ", "GU16 7HF", "L1 8JQ"]
postcode_list = []
files = os.listdir("app/tests/postcodes/")
for file in files:
    for line in open("app/tests/postcodes/"+file):
        postcode_list.append((line.strip().split(",")[0].replace('"','')))

def test_status_code_200():
    client = app.test_client()
    url = f'/postcodes/{simple_postcode}'
    response = client.get(url)
    assert response.status_code == 200

def test_response_json_has_data():
    client = app.test_client()
    url = f'/postcodes/{simple_postcode}'
    response = client.get(url)
    resp_dict = json.loads(response.text)    
    assert "data" in resp_dict


def test_response_data_has_postcode():
    client = app.test_client()
    url = f'/postcodes/{simple_postcode}'
    response = client.get(url)
    resp_dict = json.loads(response.text)    
    assert "postcode" in resp_dict["data"]
    
def test_status_code_400():
    client = app.test_client()
    url = f'/postcodes/{invalid_alphanumeric_postcode}'
    response = client.get(url)
    assert response.status_code == 400
    
def test_verify_postcode_status_code_200():
    client = app.test_client()
    url = f'/verify_postcode?postcode={simple_postcode}'
    response = client.get(url)
    assert response.status_code == 200    

def test_verify_postcode_status_code_400():
    client = app.test_client()
    url = f'/verify_postcode?postcode={invalid_alphanumeric_postcode}'
    response = client.get(url) 
    assert response.status_code == 400
    
def test_verify_postcode_no_postcode_status_code_400():
    client = app.test_client()
    url = f'/verify_postcode'
    response = client.get(url) 
    assert response.status_code == 400
    
#The postcodes are alphanumeric, 
def test_postcode_alphanumeric():
    assert "error" not in verify_alphanumeric(simple_postcode)
    
def test_invalid_postcode_alphanumeric():
    assert "error" in verify_alphanumeric(invalid_alphanumeric_postcode)
    
# and are variable in length: ranging from six to eight characters (including a space).
def test_postcode_length():
    assert "error" not in verify_length(simple_postcode)
    
def test_invalid_postcode_length():
    assert "error" in verify_length(invalid_postcode)
    
#Each postcode is divided into two parts separated by a single space
def test_postcode_space():
    assert "error" not in verify_space(simple_postcode)
    
def test_invalid_postcode_space():
    assert "error" in verify_space(invalid_postcode)
    
def test_invalid_postcode_many_spaces():
    assert "error" in verify_space(invalid_postcode_many_spaces)
    
#The outward code is the part of the postcode before the single space in the middle. 
# It is between two and four characters long.
def test_valid_outward_code():
    assert "error" not in verify_outward_code(valid_outward_code)
    
def test_invalid_outward_code():
    assert "error" in verify_outward_code(invalid_outward_code)
    
#The postcode area is either one or two characters long and is alphabetical.
#The postcode district is one digit, two digits or a digit followed by a letter.
def test_verify_postcode_area_and_district():
    assert "error" not in verify_postcode_area_and_district(simple_postcode)

def test_verify_invalid_postcode_area_and_district():
    assert "error" in verify_postcode_area_and_district(valid_outward_code)
    
#The inward code is the part of the postcode after the single space in the middle. 
# It is three characters long. 
# The inward code assists in the delivery of post within a postal district. 
# Examples of inward codes are "0NY", "7GZ", "7HF", or "8JQ"
def test_valid_inward_code():
    assert "error" not in verify_inward_code(valid_inward_code)
    
def test_invalid_inward_code():
    assert "error" in verify_inward_code(invalid_inward_code)
    
#The postcode sector is made up of a single digit (the first character of the inward code).
#The postcode unit is two characters added to the end of the postcode sector. 
# A postcode unit generally represents a street, part of a street, a single address, a group of properties, 
# a single property, a sub-section of the property, an individual organisation or 
# (for instance Driver and Vehicle Licensing Agency) a subsection of the organisation. 
# The level of discrimination is often based on the amount of mail received by the premises or business.
def test_valid_postcode_sector_and_unit():
    assert "error" not in verify_postcode_sector_and_unit(simple_postcode)
    
def test_invalid_postcode_sector():
    assert "error" in verify_postcode_sector_and_unit(invalid_sector)
    
def test_invalid_postcode_unit():
    assert "error" in verify_postcode_sector_and_unit(invalid_unit)

#UNCOMMENT TO RUN MASSIVE TEST
"""
@pytest.mark.parametrize("postcode", postcode_list)
def test_massive_validation(postcode):
    client = app.test_client()
    app.logger.info(f"postcode: {postcode}")
    url = f'/verify_postcode?postcode={postcode}'
    response = client.get(url)
    assert response.status_code == 200    
"""

#Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE, LD, SM, SR, WC, WN, ZE (although WC is always subdivided by a further letter, e.g. WC1A)
@pytest.mark.parametrize("postcode", ["FY1 1AD"])
def test_areas_single_digit_district(postcode):
    assert "error" not in verify_areas_single_digit_district(postcode)
    
@pytest.mark.parametrize("postcode", ["FY10 1AD"])
def test_invalid_areas_single_digit_district(postcode):
    assert "error" in verify_areas_single_digit_district(postcode)

#Areas with only double-digit districts: AB, LL, SO
@pytest.mark.parametrize("postcode", ["LL71 8AJ"])
def test_areas_double_digit_district(postcode):
    assert "error" not in verify_areas_double_digit_district(postcode)
    
@pytest.mark.parametrize("postcode", ["LL7 8AJ"])
def test_invalid_areas_double_digit_district(postcode):
    assert "error" in verify_areas_double_digit_district(postcode)

#Areas with a district '0' (zero): BL, BS, CM, CR, FY, HA, PR, SL, SS (BS is the only area to have both a district 0 and a district 10)

#The following central London single-digit districts have been further divided by inserting a letter after the digit and before the space: EC1–EC4 (but not EC50), SW1, W1, WC1, WC2 and parts of E1 (E1W), N1 (N1C and N1P), NW1 (NW1W) and SE1 (SE1P).

#The letters Q, V and X are not used in the first position.

#The letters I, J and Z are not used in the second position.

#The only letters to appear in the third position are A, B, C, D, E, F, G, H, J, K, P, S, T, U and W when the structure starts with A9A.

#The only letters to appear in the fourth position are A, B, E, H, M, N, P, R, V, W, X and Y when the structure starts with AA9A.

#The final two letters do not use C, I, K, M, O or V, so as not to resemble digits or each other when hand-written.

#Postcode sectors are one of ten digits: 0 to 9, with 0 only used once 9 has been used in a post town, save for Croydon and Newport (see above).